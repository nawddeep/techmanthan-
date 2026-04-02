"use client";
import React, { useMemo } from "react";
import "leaflet/dist/leaflet.css";
import { MapContainer, TileLayer, CircleMarker, Popup } from "react-leaflet";

interface Spot {
  location_id: number;
  coordinates: number[];
  traffic_intensity: string;
  waste_status: string;
  alerts_count: number;
  junction_name?: string;
  traffic_ml_label?: string;
  traffic_ml_probability?: number;
  waste_ml_label?: string;
  waste_ml_probability?: number;
  emergency_risk_score?: number;
}

export default function LiveLeafletMap({
  mapData,
  heatmapMode = false,
}: {
  mapData: Spot[];
  heatmapMode?: boolean;
}) {
  const colored = useMemo(() => {
    return mapData.map((spot) => {
      const tp = spot.traffic_ml_probability ?? 0;
      const wp = spot.waste_ml_probability ?? 0;
      const high =
        tp >= 0.5 ||
        wp >= 0.5 ||
        spot.traffic_ml_label === "high" ||
        spot.waste_ml_label === "high";
      const med =
        !high &&
        (tp >= 0.35 ||
          wp >= 0.35 ||
          spot.traffic_intensity === "medium" ||
          spot.waste_status === "medium");
      let color = "#22C55E";
      if (heatmapMode) {
        const r = spot.emergency_risk_score ?? 0;
        color = r > 3.5 ? "#EF4444" : r > 2 ? "#FACC15" : "#22C55E";
      } else if (high) color = "#EF4444";
      else if (med) color = "#FACC15";
      return { ...spot, color };
    });
  }, [mapData, heatmapMode]);

  return (
    <div className="flex-1 w-full h-full rounded-xl overflow-hidden relative z-0 shadow-inner">
      <MapContainer
        center={[24.5854, 73.7125]}
        zoom={13}
        style={{ height: "100%", width: "100%", backgroundColor: "#0f172a" }}
      >
        <TileLayer
          url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
          attribution='&copy; <a href="https://carto.com/">Carto</a>'
        />
        {colored.map((spot) => (
          <CircleMarker
            key={spot.location_id}
            center={[spot.coordinates[0], spot.coordinates[1]]}
            radius={heatmapMode ? 22 : 16}
            weight={2}
            pathOptions={{
              color: spot.color,
              fillColor: spot.color,
              fillOpacity: heatmapMode ? 0.65 : 0.5,
            }}
          >
            <Popup>
              <div className="text-slate-900 font-sans p-1 text-xs max-w-xs">
                <p className="font-bold mb-1 border-b pb-1">
                  {spot.junction_name || `Zone ${spot.location_id}`}
                </p>
                <p className="mt-1">
                  Traffic ML:{" "}
                  <span className="font-semibold">
                    {spot.traffic_ml_label} ({(spot.traffic_ml_probability ?? 0).toFixed(2)})
                  </span>
                </p>
                <p>
                  Waste ML:{" "}
                  <span className="font-semibold">
                    {spot.waste_ml_label} ({(spot.waste_ml_probability ?? 0).toFixed(2)})
                  </span>
                </p>
                <p>Emergency risk: {spot.emergency_risk_score?.toFixed(2)}</p>
                <p className="text-slate-500 mt-1">
                  Lat: {spot.coordinates[0]} | Lng: {spot.coordinates[1]}
                </p>
              </div>
            </Popup>
          </CircleMarker>
        ))}
      </MapContainer>
    </div>
  );
}
