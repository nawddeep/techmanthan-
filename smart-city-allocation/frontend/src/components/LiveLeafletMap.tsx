"use client";

import { useEffect } from "react";
import { MapContainer, TileLayer, CircleMarker, Popup, useMap, ZoomControl } from "react-leaflet";
import { LatLngBounds, LatLng } from "leaflet";
import "leaflet/dist/leaflet.css";
import React, { useMemo } from "react";

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

/** Auto-fits the map viewport to show all markers. */
function FitBounds({ spots }: { spots: Spot[] }) {
  const map = useMap();
  useEffect(() => {
    if (!spots.length) return;
    const bounds = new LatLngBounds(
      spots.map((s) => new LatLng(s.coordinates[0], s.coordinates[1]))
    );
    map.fitBounds(bounds, { padding: [50, 50], maxZoom: 13 });
  }, [spots, map]);
  return null;
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
    <div className="flex-1 w-full h-full rounded-xl overflow-hidden relative z-0 shadow-2xl border border-slate-700/50">
      <MapContainer
        center={[24.5854, 73.7125]}
        zoom={12}
        zoomControl={false}
        style={{ height: "100%", width: "100%", backgroundColor: "#0f172a" }}
      >
        <TileLayer
          url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
          attribution='&copy; <a href="https://carto.com/">Carto</a>'
        />
        <ZoomControl position="topright" />
        <FitBounds spots={mapData} />
        {colored.map((spot) => (
          <CircleMarker
            key={spot.location_id}
            center={[spot.coordinates[0], spot.coordinates[1]]}
            radius={heatmapMode ? 24 : 18}
            weight={3}
            pathOptions={{
              color: spot.color,
              fillColor: spot.color,
              fillOpacity: heatmapMode ? 0.7 : 0.6,
            }}
          >
            <Popup maxWidth={300} className="custom-popup">
              <div className="text-slate-900 font-sans p-2 text-sm">
                <p className="font-bold text-base mb-2 border-b pb-2 text-slate-800">
                  {spot.junction_name || `Zone ${spot.location_id}`}
                </p>
                <div className="space-y-1.5">
                  <div className="flex justify-between items-center">
                    <span className="text-slate-600 font-medium">Traffic ML:</span>
                    <span className={`font-bold px-2 py-0.5 rounded text-xs ${
                      spot.traffic_ml_label === 'high' 
                        ? 'bg-red-100 text-red-700' 
                        : spot.traffic_ml_label === 'medium'
                        ? 'bg-yellow-100 text-yellow-700'
                        : 'bg-green-100 text-green-700'
                    }`}>
                      {spot.traffic_ml_label} ({(spot.traffic_ml_probability ?? 0).toFixed(2)})
                    </span>
                  </div>
                  <div className="flex justify-between items-center">
                    <span className="text-slate-600 font-medium">Waste ML:</span>
                    <span className={`font-bold px-2 py-0.5 rounded text-xs ${
                      spot.waste_ml_label === 'high' 
                        ? 'bg-red-100 text-red-700' 
                        : spot.waste_ml_label === 'medium'
                        ? 'bg-yellow-100 text-yellow-700'
                        : 'bg-green-100 text-green-700'
                    }`}>
                      {spot.waste_ml_label} ({(spot.waste_ml_probability ?? 0).toFixed(2)})
                    </span>
                  </div>
                  <div className="flex justify-between items-center pt-1 border-t">
                    <span className="text-slate-600 font-medium">Emergency Risk:</span>
                    <span className="font-bold text-slate-800">
                      {spot.emergency_risk_score?.toFixed(2) || 'N/A'}
                    </span>
                  </div>
                </div>
                <p className="text-slate-500 text-xs mt-2 pt-2 border-t">
                  📍 {spot.coordinates[0].toFixed(4)}, {spot.coordinates[1].toFixed(4)}
                </p>
              </div>
            </Popup>
          </CircleMarker>
        ))}
      </MapContainer>
    </div>
  );
}
