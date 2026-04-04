"use client";

import dynamic from "next/dynamic";
import { Loader2, MapPin, Maximize2, Minimize2, Layers } from "lucide-react";
import { useState } from "react";

const Map = dynamic(() => import("./LiveLeafletMap"), {
  ssr: false,
  loading: () => (
    <div className="flex-1 w-full h-full flex items-center justify-center rounded-xl bg-slate-900/50">
      <Loader2 className="w-8 h-8 animate-spin text-blue-500" />
    </div>
  ),
});

interface MapDataLocation {
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

export default function MapComponent({
  mapData,
}: {
  mapData: MapDataLocation[];
}) {
  const [heatmap, setHeatmap] = useState(false);
  const [isFullscreen, setIsFullscreen] = useState(false);

  const isLoading = mapData.length === 0;

  return (
    <div 
      className={`glass-panel flex flex-col relative overflow-hidden transition-all duration-300 ${
        isFullscreen 
          ? 'fixed inset-4 z-[9999] h-[calc(100vh-2rem)]' 
          : 'p-6 h-[600px]'
      }`}
    >
      {/* Header with controls */}
      <div className="flex justify-between items-center mb-4 z-10 px-6 pt-6">
        <div className="flex items-center gap-3">
          <div className="bg-blue-600/20 p-2 rounded-lg border border-blue-500/30">
            <MapPin className="w-5 h-5 text-blue-400" />
          </div>
          <div>
            <h2 className="text-lg font-bold tracking-wide text-slate-100">
              Live City Map
            </h2>
            <p className="text-xs text-slate-500">
              {isLoading ? 'Connecting...' : `${mapData.length} zones monitored`}
            </p>
          </div>
        </div>
        
        <div className="flex items-center gap-3">
          {/* Heatmap toggle */}
          <button
            onClick={() => setHeatmap(!heatmap)}
            disabled={isLoading}
            className={`flex items-center gap-2 px-3 py-2 rounded-lg text-xs font-medium transition-all ${
              heatmap
                ? 'bg-orange-500/20 text-orange-400 border border-orange-500/30'
                : 'bg-slate-800/50 text-slate-400 border border-slate-700 hover:border-slate-600'
            } disabled:opacity-50 disabled:cursor-not-allowed`}
          >
            <Layers className="w-4 h-4" />
            {heatmap ? 'Emergency Heat' : 'Normal View'}
          </button>

          {/* Fullscreen toggle */}
          <button
            onClick={() => setIsFullscreen(!isFullscreen)}
            className="flex items-center gap-2 px-3 py-2 rounded-lg text-xs font-medium bg-slate-800/50 text-slate-400 border border-slate-700 hover:border-blue-500/50 hover:text-blue-400 transition-all"
          >
            {isFullscreen ? (
              <>
                <Minimize2 className="w-4 h-4" />
                Exit
              </>
            ) : (
              <>
                <Maximize2 className="w-4 h-4" />
                Fullscreen
              </>
            )}
          </button>
        </div>
      </div>

      {/* Map container */}
      {isLoading ? (
        <div className="flex-1 w-full h-full flex flex-col items-center justify-center rounded-xl bg-slate-900/50 gap-3 mx-6 mb-6">
          <MapPin className="w-12 h-12 text-blue-500/60 animate-bounce" />
          <p className="text-slate-300 text-base font-semibold animate-pulse">
            Loading city data…
          </p>
          <p className="text-slate-500 text-sm">
            Fetching real-time data from backend
          </p>
        </div>
      ) : (
        <div className="flex-1 px-6 pb-6">
          <Map mapData={mapData} heatmapMode={heatmap} />
        </div>
      )}

      {/* Enhanced Legend */}
      {!isLoading && (
        <div className="absolute bottom-8 left-8 bg-slate-900/95 p-4 rounded-xl border border-slate-700/80 backdrop-blur-xl z-[1000] shadow-2xl">
          <div className="text-xs font-bold text-slate-300 mb-3 uppercase tracking-wider border-b border-slate-700 pb-2">
            Map Legend
          </div>
          <div className="space-y-2.5">
            <div className="flex items-center gap-3">
              <div className="w-3 h-3 rounded-full bg-green-500 shadow-[0_0_12px_rgba(34,197,94,0.7)]" />
              <span className="text-slate-300 text-xs font-medium">Low Risk / Normal</span>
            </div>
            <div className="flex items-center gap-3">
              <div className="w-3 h-3 rounded-full bg-yellow-400 shadow-[0_0_12px_rgba(250,204,21,0.7)]" />
              <span className="text-slate-300 text-xs font-medium">Medium Risk</span>
            </div>
            <div className="flex items-center gap-3">
              <div className="w-3 h-3 rounded-full bg-red-500 shadow-[0_0_12px_rgba(239,68,68,0.7)]" />
              <span className="text-slate-300 text-xs font-medium">High Risk / Critical</span>
            </div>
          </div>
          {heatmap && (
            <div className="mt-3 pt-3 border-t border-slate-700">
              <p className="text-[10px] text-slate-500 uppercase tracking-wide">
                Emergency heat mode active
              </p>
            </div>
          )}
        </div>
      )}

      {/* Data source indicator */}
      {!isLoading && (
        <div className="absolute top-8 right-8 bg-emerald-500/10 border border-emerald-500/30 px-3 py-1.5 rounded-full z-[1000]">
          <span className="text-emerald-400 text-[10px] font-bold uppercase tracking-widest">
            ● Live Data
          </span>
        </div>
      )}
    </div>
  );
}
