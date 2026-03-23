"use client";
import React from 'react';
import "leaflet/dist/leaflet.css";
import { MapContainer, TileLayer, CircleMarker, Popup } from 'react-leaflet';

export default function LiveLeafletMap({ mapData }: { mapData: any[] }) {
  return (
    <div className="flex-1 w-full h-full rounded-xl overflow-hidden relative z-0 shadow-inner">
      <MapContainer center={[24.5854, 73.7125]} zoom={13} style={{ height: "100%", width: "100%", backgroundColor: "#0f172a" }}>
        <TileLayer
          url="https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}{r}.png"
          attribution='&copy; <a href="https://carto.com/">Carto</a>'
        />
        {mapData.map((spot: any) => {
           let color = "#22C55E"; // Green
           if (spot.traffic_intensity === "high" || spot.waste_status === "high") color = "#EF4444"; // Red
           else if (spot.traffic_intensity === "medium" || spot.waste_status === "medium") color = "#FACC15"; // Yellow
           
           return (
             <CircleMarker 
               key={spot.location_id}
               center={[spot.coordinates[0], spot.coordinates[1]]}
               radius={16}
               weight={2}
               pathOptions={{ color, fillColor: color, fillOpacity: 0.5 }}
             >
               <Popup>
                 <div className="text-slate-900 font-sans p-1">
                   <p className="font-bold mb-1 border-b pb-1">Location ID: {spot.location_id}</p>
                   <p className="text-sm mt-1">Traffic: <span className="font-semibold">{spot.traffic_intensity.toUpperCase()}</span></p>
                   <p className="text-sm">Waste: <span className="font-semibold">{spot.waste_status.toUpperCase()}</span></p>
                   <p className="text-sm text-slate-500 mt-2 text-xs">Lat: {spot.coordinates[0]} | Lng: {spot.coordinates[1]}</p>
                 </div>
               </Popup>
             </CircleMarker>
           )
        })}
      </MapContainer>
    </div>
  )
}
