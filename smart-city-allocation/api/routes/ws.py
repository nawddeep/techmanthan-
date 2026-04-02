"""WebSocket broadcast for city state updates."""
from __future__ import annotations

import asyncio
import json
from typing import Any, Dict, List, Set

from fastapi import APIRouter, WebSocket, WebSocketDisconnect

from api.services.simulation_service import get_current_state

router = APIRouter(tags=["WebSocket"])

_connections: Set[WebSocket] = set()
_lock = asyncio.Lock()


def _serialize_state(state: Dict[str, Any]) -> Dict[str, Any]:
    out = dict(state)
    em = out.get("emergencies") or []
    serial_em = []
    for e in em:
        if hasattr(e, "model_dump"):
            d = e.model_dump()
        elif hasattr(e, "dict"):
            d = e.dict()
        else:
            d = e
        if isinstance(d.get("timestamp"), object) and hasattr(d.get("timestamp"), "isoformat"):
            d["timestamp"] = d["timestamp"].isoformat()
        if "event_type" in d and hasattr(d["event_type"], "value"):
            d["event_type"] = d["event_type"].value
        if "severity" in d and hasattr(d["severity"], "value"):
            d["severity"] = d["severity"].value
        serial_em.append(d)
    out["emergencies"] = serial_em
    return out


async def broadcast_state(state: Dict[str, Any]) -> None:
    if not _connections:
        return
    payload = json.dumps(_serialize_state(state), default=str)
    dead: List[WebSocket] = []
    async with _lock:
        conns = list(_connections)
    for ws in conns:
        try:
            await ws.send_text(payload)
        except Exception:
            dead.append(ws)
    async with _lock:
        for ws in dead:
            _connections.discard(ws)


@router.websocket("/ws/city-updates")
async def city_updates_ws(websocket: WebSocket):
    await websocket.accept()
    async with _lock:
        _connections.add(websocket)
    try:
        await websocket.send_json(_serialize_state(get_current_state()))
        while True:
            try:
                await asyncio.wait_for(websocket.receive_text(), timeout=60.0)
            except asyncio.TimeoutError:
                await websocket.send_json({"type": "ping"})
    except WebSocketDisconnect:
        pass
    finally:
        async with _lock:
            _connections.discard(websocket)
