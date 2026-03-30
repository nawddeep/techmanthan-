"use client";

import dynamic from 'next/dynamic';
import { Loader2 } from 'lucide-react';

const Map = dynamic(
  () => import('./LiveLeafletMap'),
  { 
    ssr: false, 
    loading: () => <div className="flex-1 w-full h-full flex items-center justify-center rounded-xl bg-slate-900/50"><Loader2 className="w-8 h-8 animate-spin text-blue-500" /></div>
  }
);

interface MapDataLocation {
  location_id: number;
  coordinates: number[];
  traffic_intensity: string;
  waste_status: string;
  alerts_count: number;
}

export default function MapComponent({ mapData }: { mapData: MapDataLocation[] }) {
  return (
    <div className="glass-panel p-6 h-[400px] flex flex-col relative overflow-hidden">
      <h2 className="text-lg font-semibold tracking-wide text-slate-200 uppercase mb-4 z-10">Live Geographical Map</h2>
      <Map mapData={mapData} />
      
      {/* Legend Box */}
      <div className="absolute bottom-6 left-6 bg-slate-900/90 p-3 rounded-lg border border-slate-700 backdrop-blur-md z-[1000] text-[10px] font-bold tracking-wider uppercase shadow-xl">
        <div className="flex items-center gap-2 mb-2"><div className="w-2.5 h-2.5 rounded-full bg-green-500 shadow-[0_0_8px_rgba(34,197,94,0.6)]"></div><span className="text-slate-300">Low Risk</span></div>
        <div className="flex items-center gap-2 mb-2"><div className="w-2.5 h-2.5 rounded-full bg-yellow-400 shadow-[0_0_8px_rgba(250,204,21,0.6)]"></div><span className="text-slate-300">Medium Risk</span></div>
        <div className="flex items-center gap-2"><div className="w-2.5 h-2.5 rounded-full bg-red-500 shadow-[0_0_8px_rgba(239,68,68,0.6)]"></div><span className="text-slate-300">High Risk</span></div>
      </div>
    </div>
  );
}
