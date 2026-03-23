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
    </div>
  );
}
