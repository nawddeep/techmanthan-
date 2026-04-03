"use client";

import { useState } from "react";
import api from "@/lib/api";
import { Loader2 } from "lucide-react";

interface PredState {
  isLoading: boolean;
  error: string | null;
  data: any;
}

const initialState: PredState = { isLoading: false, error: null, data: null };

export default function PredictionPanel() {
  // Traffic inputs
  const [th, setTh] = useState(14);
  const [td, setTd] = useState(3);
  const [tj, setTj] = useState(2);
  const [tw, setTw] = useState(0);
  const [tv, setTv] = useState(250);
  const [tState, setTState] = useState<PredState>(initialState);

  // Waste inputs
  const [wa, setWa] = useState(2);
  const [wd, setWd] = useState(3);
  const [wp, setWp] = useState(2);
  const [wl, setWl] = useState(4);
  const [wb, setWb] = useState(72);
  const [wState, setWState] = useState<PredState>(initialState);

  const runTraffic = async () => {
    if (tState.isLoading) return; // prevent double-fires
    setTState({ isLoading: true, error: null, data: null });
    try {
      const res = await api.post("/predict/traffic", {
        hour: th,
        day_enc: td,
        junction_enc: tj,
        weather_enc: tw,
        vehicles: tv,
      });
      const ex = await api.post("/explain/traffic", {
        hour: th,
        day_enc: td,
        junction_enc: tj,
        weather_enc: tw,
        vehicles: tv,
      });
      setTState({ isLoading: false, error: null, data: { ...res.data, explain: ex.data } });
    } catch (err: any) {
      const msg =
        err?.response?.data?.detail ||
        err?.message ||
        "Prediction failed. Ensure the backend is running.";
      setTState({ isLoading: false, error: msg, data: null });
    }
  };

  const runWaste = async () => {
    if (wState.isLoading) return; // prevent double-fires
    setWState({ isLoading: true, error: null, data: null });
    try {
      const res = await api.post("/predict/waste", {
        area: wa,
        day_of_week: wd,
        population_density: wp * 1000,
        last_collection_days: wl,
        bin_fill_pct: wb,
      });
      const ex = await api.post("/explain/waste", {
        area: wa,
        day_of_week: wd,
        population_density: wp * 1000,
        last_collection_days: wl,
        bin_fill_pct: wb,
      });
      setWState({ isLoading: false, error: null, data: { ...res.data, explain: ex.data } });
    } catch (err: any) {
      const msg =
        err?.response?.data?.detail ||
        err?.message ||
        "Prediction failed. Ensure the backend is running.";
      setWState({ isLoading: false, error: msg, data: null });
    }
  };

  return (
    <div className="glass-panel p-6 col-span-1 md:col-span-2 xl:col-span-5 border border-slate-700/60">
      <h3 className="text-sm font-bold uppercase tracking-wider text-slate-300 mb-4">
        Interactive ML Predictions
      </h3>
      <div className="grid md:grid-cols-2 gap-8">
        {/* ── Traffic Model ── */}
        <div>
          <p className="text-xs text-slate-500 mb-2">Traffic model</p>
          <div className="grid grid-cols-2 gap-2 text-xs">
            <label className="text-slate-400">
              Hour
              <input
                type="number"
                className="w-full bg-slate-800 border border-slate-600 rounded px-2 py-1 text-slate-100 mt-1"
                value={th}
                onChange={(e) => setTh(+e.target.value)}
              />
            </label>
            <label className="text-slate-400">
              Day enc
              <input
                type="number"
                className="w-full bg-slate-800 border border-slate-600 rounded px-2 py-1 mt-1"
                value={td}
                onChange={(e) => setTd(+e.target.value)}
              />
            </label>
            <label className="text-slate-400">
              Junction
              <input
                type="number"
                className="w-full bg-slate-800 border border-slate-600 rounded px-2 py-1 mt-1"
                value={tj}
                onChange={(e) => setTj(+e.target.value)}
              />
            </label>
            <label className="text-slate-400">
              Weather
              <input
                type="number"
                className="w-full bg-slate-800 border border-slate-600 rounded px-2 py-1 mt-1"
                value={tw}
                onChange={(e) => setTw(+e.target.value)}
              />
            </label>
            <label className="text-slate-400 col-span-2">
              Vehicles
              <input
                type="number"
                className="w-full bg-slate-800 border border-slate-600 rounded px-2 py-1 mt-1"
                value={tv}
                onChange={(e) => setTv(+e.target.value)}
              />
            </label>
          </div>
          <button
            type="button"
            onClick={runTraffic}
            disabled={tState.isLoading}
            className="mt-3 px-4 py-2 bg-blue-600 hover:bg-blue-500 disabled:opacity-50 disabled:cursor-not-allowed rounded-lg text-sm font-semibold text-white flex items-center gap-2 transition-all"
          >
            {tState.isLoading && <Loader2 className="w-4 h-4 animate-spin" />}
            {tState.isLoading ? "Running…" : "Predict + SHAP"}
          </button>
          {tState.error && (
            <p className="mt-2 text-xs text-red-400 bg-red-900/20 border border-red-500/30 rounded px-3 py-2">
              {tState.error}
            </p>
          )}
          {tState.data && (
            <pre className="mt-3 text-[11px] text-slate-400 whitespace-pre-wrap bg-slate-900/50 p-2 rounded max-h-48 overflow-auto">
              {JSON.stringify(tState.data, null, 2)}
            </pre>
          )}
        </div>

        {/* ── Waste Model ── */}
        <div>
          <p className="text-xs text-slate-500 mb-2">Waste model</p>
          <div className="grid grid-cols-2 gap-2 text-xs">
            <label className="text-slate-400">
              Area
              <input
                type="number"
                className="w-full bg-slate-800 border border-slate-600 rounded px-2 py-1 mt-1"
                value={wa}
                onChange={(e) => setWa(+e.target.value)}
              />
            </label>
            <label className="text-slate-400">
              Day
              <input
                type="number"
                className="w-full bg-slate-800 border border-slate-600 rounded px-2 py-1 mt-1"
                value={wd}
                onChange={(e) => setWd(+e.target.value)}
              />
            </label>
            <label className="text-slate-400">
              Pop. dens (k)
              <input
                type="number"
                className="w-full bg-slate-800 border border-slate-600 rounded px-2 py-1 mt-1"
                value={wp}
                onChange={(e) => setWp(+e.target.value)}
              />
            </label>
            <label className="text-slate-400">
              Days since coll.
              <input
                type="number"
                className="w-full bg-slate-800 border border-slate-600 rounded px-2 py-1 mt-1"
                value={wl}
                onChange={(e) => setWl(+e.target.value)}
              />
            </label>
            <label className="text-slate-400 col-span-2">
              Bin fill %
              <input
                type="number"
                className="w-full bg-slate-800 border border-slate-600 rounded px-2 py-1 mt-1"
                value={wb}
                onChange={(e) => setWb(+e.target.value)}
              />
            </label>
          </div>
          <button
            type="button"
            onClick={runWaste}
            disabled={wState.isLoading}
            className="mt-3 px-4 py-2 bg-emerald-600 hover:bg-emerald-500 disabled:opacity-50 disabled:cursor-not-allowed rounded-lg text-sm font-semibold text-white flex items-center gap-2 transition-all"
          >
            {wState.isLoading && <Loader2 className="w-4 h-4 animate-spin" />}
            {wState.isLoading ? "Running…" : "Predict + SHAP"}
          </button>
          {wState.error && (
            <p className="mt-2 text-xs text-red-400 bg-red-900/20 border border-red-500/30 rounded px-3 py-2">
              {wState.error}
            </p>
          )}
          {wState.data && (
            <pre className="mt-3 text-[11px] text-slate-400 whitespace-pre-wrap bg-slate-900/50 p-2 rounded max-h-48 overflow-auto">
              {JSON.stringify(wState.data, null, 2)}
            </pre>
          )}
        </div>
      </div>
    </div>
  );
}
