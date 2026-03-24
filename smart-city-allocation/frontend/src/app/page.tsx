"use client";

import { useEffect, useState } from "react";
import axios from "axios";
import { Activity, AlertCircle, BarChart3, Clock, Flame, Loader2, Navigation, RefreshCw, ShieldAlert } from "lucide-react";
import KPICard from "@/components/KPICard";
import AlertPanel from "@/components/AlertPanel";
import DecisionPanel from "@/components/DecisionPanel";
import MapComponent from "@/components/MapComponent";
import Charts from "@/components/Charts";

interface SystemDecision {
  traffic: { value: number; status: string };
  waste: { value: number; risk: string };
  emergency: { type: string; severity: string };
  alerts: string[];
  actions: string[];
}

export default function Dashboard() {
  const [data, setData] = useState<SystemDecision | null>(null);
  const [mapData, setMapData] = useState<any[]>([]);
  const [error, setError] = useState(false);
  const [history, setHistory] = useState<{time: string, traffic: number, waste: number}[]>([]);
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date());

  useEffect(() => {
    const fetchDecision = async () => {
      try {
        const [res, mapRes] = await Promise.all([
          axios.get("/api/system/decision"),
          axios.get("/api/map-data")
        ]);
        
        setData(res.data);
        setMapData(mapRes.data);
        setError(false);
        setLastUpdate(new Date());

        const now = new Date();
        const timeStr = `${now.getHours()}:${now.getMinutes()}:${now.getSeconds()}`;
        
        setHistory(prev => {
          const newHistory = [...prev, {
            time: timeStr,
            traffic: res.data.traffic.value,
            waste: res.data.waste.value
          }];
          if (newHistory.length > 15) newHistory.shift();
          return newHistory;
        });

      } catch (err) {
        console.error("API Fetch Error:", err);
        setError(true);
      }
    };

    fetchDecision();
    const interval = setInterval(fetchDecision, 3000); // Poll every 3 seconds
    return () => clearInterval(interval);
  }, []);

  if (!data && !error) {
    return (
      <div className="min-h-screen bg-[#0B0F19] flex items-center justify-center text-blue-500">
        <Loader2 className="w-12 h-12 animate-spin" />
      </div>
    );
  }

  return (
    <main className="min-h-screen p-4 md:p-8 flex flex-col gap-6">
      {/* Top Navbar */}
      <header className="flex justify-between items-center bg-slate-900/40 p-4 rounded-2xl border border-slate-800 backdrop-blur-md">
        <div className="flex items-center gap-3">
          <div className="bg-blue-600 p-2 rounded-lg">
            <Activity className="text-white w-6 h-6" />
          </div>
          <h1 className="text-2xl font-bold text-slate-100 tracking-tight">Smart City <span className="text-blue-500">Command Center</span></h1>
        </div>
        <div className="flex items-center gap-4 text-sm font-medium text-slate-400">
          <div className="flex items-center gap-2">
            <Clock className="w-4 h-4" />
            <span>{lastUpdate.toLocaleTimeString()}</span>
          </div>
          <div className={`flex items-center gap-2 px-3 py-1.5 rounded-full ${error ? "bg-red-500/20 text-red-400" : "bg-green-500/20 text-green-400"}`}>
            <RefreshCw className={`w-4 h-4 ${!error && "animate-spin-slow duration-[3000ms]"}`} />
            <span>{error ? "CONNECTION LOST" : "SYSTEM LIVE"}</span>
          </div>
        </div>
      </header>

      {error ? (
        <div className="glass-panel text-red-400 p-8 flex flex-col items-center justify-center h-64 text-center">
          <ShieldAlert className="w-12 h-12 mb-4 animate-bounce" />
          <h2 className="text-xl font-bold">Backend Communication Failure</h2>
          <p className="mt-2 text-slate-400">Ensure the backend server is running.</p>
        </div>
      ) : (
        <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4 gap-6">
          
          {/* Top Row: KPIs */}
          <KPICard 
            title="Traffic Density" 
            value={`${data?.traffic.value.toFixed(1)}%`}
            statusText={data?.traffic.status}
            statusLevel={data?.traffic.status as any}
            icon={<Navigation />}
          />
          <KPICard 
            title="Waste Overflow" 
            value={`${data?.waste.value.toFixed(1)}%`}
            statusText={data?.waste.risk}
            statusLevel={data?.waste.risk as any}
            icon={<BarChart3 />}
          />
          <KPICard 
            title="Active Emergency" 
            value={data?.emergency.type || "None"}
            statusText={data?.emergency.severity}
            statusLevel={data?.emergency.severity as any}
            icon={<Flame />}
          />
          <div className="glass-panel p-6 flex flex-col justify-between border-slate-700/50">
            <div className="flex justify-between items-center mb-4 text-slate-400">
              <h3 className="text-sm font-semibold uppercase tracking-wider">Total Alerts</h3>
              <AlertCircle className="w-5 h-5 opacity-60 text-yellow-500" />
            </div>
            <div className="text-4xl font-bold text-slate-100">{data?.alerts.length || 0}</div>
          </div>

          {/* Core Feature: Decision Panel (spans wide) */}
          <div className="col-span-1 md:col-span-2 xl:col-span-3">
             <DecisionPanel actions={data?.actions || []} />
          </div>

          {/* Right Column: Alerts */}
          <div className="col-span-1 md:col-span-2 lg:col-span-1 xl:col-span-1 row-span-2">
            <AlertPanel alerts={data?.alerts || []} />
          </div>

          {/* Map Component */}
          <div className="col-span-1 md:col-span-2 lg:col-span-1 border-r border-slate-800 pr-0">
            <MapComponent mapData={mapData} />
          </div>

          {/* Charts Component */}
          <div className="col-span-1 md:col-span-2 lg:col-span-2 xl:col-span-2">
            <Charts history={history} />
          </div>
        </div>
      )}
    </main>
  );
}
