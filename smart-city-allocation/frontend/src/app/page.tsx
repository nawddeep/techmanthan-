"use client";

import { useEffect, useState, useCallback, useRef } from "react";
import Link from "next/link";
import {
  Activity,
  AlertCircle,
  BarChart3,
  Clock,
  Flame,
  Loader2,
  Navigation,
  RefreshCw,
  ShieldAlert,
  Wifi,
  WifiOff,
} from "lucide-react";
import KPICard from "@/components/KPICard";
import AlertPanel from "@/components/AlertPanel";
import DecisionPanel from "@/components/DecisionPanel";
import MapComponent from "@/components/MapComponent";
import Charts from "@/components/Charts";
import ROICard from "@/components/ROICard";
import HealthScoreCard from "@/components/HealthScoreCard";
import ErrorBoundary from "@/components/ErrorBoundary";
import VoiceAssistant from "@/components/VoiceAssistant";
import PredictionPanel from "@/components/PredictionPanel";
import api from "@/lib/api";

interface SystemDecision {
  traffic: { value: number; status: string; features?: any };
  waste: { value: number; risk: string; features?: any; waste_overflow_eta?: string };
  emergency: {
    type: string;
    severity: string;
    worst_zone_id?: number;
    worst_zone_risk_score?: number;
  };
  alerts: string[];
  actions: string[];
  data_source?: string;
  roi?: {
    baseline_cost: number;
    optimized_cost: number;
    monthly_savings: number;
    savings_percentage: number;
    annual_projection: number;
    explanation: string;
  };
  city_health_score?: number;
}

const WS_URL =
  typeof process !== "undefined" && process.env.NEXT_PUBLIC_WS_URL
    ? process.env.NEXT_PUBLIC_WS_URL
    : "ws://127.0.0.1:8000/ws/city-updates";

export default function Dashboard() {
  const [data, setData] = useState<SystemDecision | null>(null);
  const [mapData, setMapData] = useState<any[]>([]);
  const [error, setError] = useState(false);
  const [history, setHistory] = useState<
    { time: string; traffic: number; waste: number }[]
  >([]);
  const [lastUpdate, setLastUpdate] = useState<Date>(new Date());
  const [user, setUser] = useState<{ username: string; role: string } | null>(null);
  const [wsStatus, setWsStatus] = useState<"connected" | "disconnected" | "connecting">(
    "connecting"
  );
  const wsRef = useRef<WebSocket | null>(null);

  const fetchDecision = useCallback(async () => {
    try {
      const [res, mapRes, historyRes, me] = await Promise.all([
        api.get<SystemDecision>("/system/decision"),
        api.get("/map-data"),
        api.get("/history/trends"),
        api.get("/auth/me").catch(() => null),
      ]);
      setData(res.data);
      setMapData(mapRes.data);
      setError(false);
      setLastUpdate(new Date());
      if (me?.data) setUser(me.data);

      const hData = historyRes.data;
      if (hData && Array.isArray(hData.timestamps)) {
        setHistory(
          hData.timestamps.map((t: string, i: number) => ({
            time: t,
            traffic: hData.traffic[i],
            waste: hData.waste[i],
          }))
        );
      }
    } catch (err: any) {
      if (err.response?.status === 401) {
        // Interceptor handles the redirect; don't show the error panel.
        return;
      }
      setError(true);
    }
  }, []);

  useEffect(() => {
    fetchDecision();
  }, [fetchDecision]);

  useEffect(() => {
    let ws: WebSocket | null = null;
    try {
      ws = new WebSocket(WS_URL);
      wsRef.current = ws;
      setWsStatus("connecting");
      ws.onopen = () => setWsStatus("connected");
      ws.onclose = () => setWsStatus("disconnected");
      ws.onerror = () => setWsStatus("disconnected");
      ws.onmessage = () => {
        fetchDecision();
      };
    } catch {
      setWsStatus("disconnected");
    }
    const poll = setInterval(() => fetchDecision(), 5000);
    return () => {
      clearInterval(poll);
      ws?.close();
    };
  }, [fetchDecision]);

  const trafficSpark = history.slice(-10).map((h) => h.traffic);
  const wasteSpark = history.slice(-10).map((h) => h.waste);

  const ds = data?.data_source || "";
  const dsLabel =
    ds === "real_data"
      ? "REAL DATA"
      : ds === "statistical_sim"
        ? "STAT SIM"
        : ds === "live"
          ? "LIVE"
          : ds === "cached"
            ? "CACHED"
            : "SIM";

  return (
    <main className="min-h-screen p-4 md:p-8 flex flex-col gap-6">
      <header className="flex flex-wrap justify-between items-center bg-slate-900/40 p-4 rounded-2xl border border-slate-800 backdrop-blur-md gap-4">
        <div className="flex items-center gap-3">
          <div className="bg-blue-600 p-2 rounded-lg">
            <Activity className="text-white w-6 h-6" />
          </div>
          <div>
            <h1 className="text-2xl font-bold text-slate-100 tracking-tight">
              Smart City <span className="text-blue-500">Command Center</span>
            </h1>
            <div className="flex gap-3 text-xs text-slate-500 mt-1">
              <Link href="/model-stats" className="hover:text-blue-400">
                Model stats
              </Link>
              {user && (
                <span className="text-slate-400">
                  {user.username} ({user.role})
                </span>
              )}
            </div>
          </div>
        </div>
        <div className="flex items-center gap-4 text-sm font-medium text-slate-400 flex-wrap">
          {data?.data_source && (
            <div
              className={`flex items-center gap-2 px-3 py-1.5 rounded-full border ${
                ds === "real_data"
                  ? "bg-emerald-500/10 text-emerald-400 border-emerald-500/20"
                  : "bg-rose-500/10 text-rose-400 border-rose-500/20"
              }`}
            >
              <span className="font-bold tracking-widest text-[11px] uppercase">{dsLabel}</span>
            </div>
          )}
          <div className="flex items-center gap-1 text-[11px] uppercase text-slate-500">
            {wsStatus === "connected" ? (
              <Wifi className="w-4 h-4 text-emerald-400" />
            ) : (
              <WifiOff className="w-4 h-4 text-amber-400" />
            )}
            {wsStatus === "connected" ? "WS live" : "WS fallback"}
          </div>
          <div className="flex items-center gap-2">
            <Clock className="w-4 h-4" />
            <span>{lastUpdate.toLocaleTimeString()}</span>
          </div>
          <div
            className={`flex items-center gap-2 px-3 py-1.5 rounded-full ${
              error ? "bg-red-500/20 text-red-400" : "bg-green-500/20 text-green-400"
            }`}
          >
            <RefreshCw className={`w-4 h-4 ${!error && "animate-spin-slow duration-[3000ms]"}`} />
            <span>{error ? "CONNECTION LOST" : "SYSTEM ONLINE"}</span>
          </div>
        </div>
      </header>

      <div className="bg-slate-800/80 border border-slate-700 p-4 rounded-xl flex flex-col md:flex-row items-center gap-4 text-sm text-slate-300 shadow-md">
        <div className="bg-blue-500/20 p-2 rounded-full hidden md:block">
          <Activity className="w-5 h-5 text-blue-400" />
        </div>
        <div className="text-center md:text-left">
          <p className="font-semibold mb-1 text-slate-200">System Architecture</p>
          <p>
            Live weather integration, CSV-backed simulation, SQLite history, JWT auth, and ML
            pipelines (traffic, waste, emergency) with SHAP explainability.
          </p>
        </div>
      </div>

      {error ? (
        <div className="glass-panel text-red-400 p-8 flex flex-col items-center justify-center h-64 text-center">
          <ShieldAlert className="w-12 h-12 mb-4 animate-bounce" />
          <h2 className="text-xl font-bold">Backend Communication Failure</h2>
          <p className="mt-2 text-slate-400">Ensure the API is running.</p>
        </div>
      ) : (
        <ErrorBoundary fallbackText="Something went wrong">
          <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-5 gap-6">
            {!data ? (
              <div className="glass-panel h-32 flex flex-col justify-between animate-pulse bg-slate-800/40 p-6">
                <div className="h-3 bg-slate-700/50 rounded w-1/3" />
                <Loader2 className="animate-spin text-blue-500 w-8 h-8" />
              </div>
            ) : (
              <div id="health-section" className="h-full">
                <HealthScoreCard score={data?.city_health_score || 100} />
              </div>
            )}

            {!data ? (
              <div className="glass-panel h-32 animate-pulse bg-slate-800/40 p-6" />
            ) : (
              <div id="traffic-section" className="h-full">
                <KPICard
                  title="Traffic Density"
                  value={`${data?.traffic.value.toFixed(1)}%`}
                  statusText={data?.traffic.status}
                  statusLevel={data?.traffic.status as any}
                  icon={<Navigation />}
                  explainPath="/explain/traffic"
                  features={data?.traffic.features}
                  sparkline={trafficSpark.length > 1 ? trafficSpark : undefined}
                  thresholdPct={80}
                />
              </div>
            )}

            {!data ? (
              <div className="glass-panel h-32 animate-pulse bg-slate-800/40 p-6" />
            ) : (
              <div id="waste-section" className="h-full">
                <KPICard
                  title="Waste Overflow"
                  value={`${data?.waste.value.toFixed(1)}%`}
                  subText={
                    data?.waste.waste_overflow_eta
                      ? `ETA: ${data?.waste.waste_overflow_eta}`
                      : undefined
                  }
                  statusText={data?.waste.risk}
                  statusLevel={data?.waste.risk as any}
                  icon={<BarChart3 />}
                  explainPath="/explain/waste"
                  features={data?.waste.features}
                  sparkline={wasteSpark.length > 1 ? wasteSpark : undefined}
                  thresholdPct={80}
                />
              </div>
            )}

            {!data ? (
              <div className="glass-panel h-32 animate-pulse bg-slate-800/40 p-6" />
            ) : (
              <KPICard
                title="Emergency"
                value={
                  data?.emergency.worst_zone_id != null
                    ? `Z${data.emergency.worst_zone_id}`
                    : data?.emergency.type || "None"
                }
                subText={
                  data?.emergency.worst_zone_risk_score != null
                    ? `Risk ${data.emergency.worst_zone_risk_score.toFixed(1)}`
                    : undefined
                }
                statusText={data?.emergency.severity}
                statusLevel={data?.emergency.severity as any}
                icon={<Flame />}
              />
            )}

            {!data ? (
              <div className="glass-panel h-32 animate-pulse bg-slate-800/40 p-6" />
            ) : data?.roi ? (
              <ROICard roiData={data.roi} />
            ) : (
              <div className="glass-panel p-6 flex flex-col justify-between border-slate-700/50">
                <div className="flex justify-between items-center mb-4 text-slate-400">
                  <h3 className="text-sm font-semibold uppercase tracking-wider">Total Alerts</h3>
                  <AlertCircle className="w-5 h-5 opacity-60 text-yellow-500" />
                </div>
                <div className="text-4xl font-bold text-slate-100">{data?.alerts.length || 0}</div>
              </div>
            )}

            <div id="decision-section" className="col-span-1 md:col-span-2 xl:col-span-3">
              <ErrorBoundary fallbackText="Decision Panel Error">
                <DecisionPanel actions={data?.actions || []} />
              </ErrorBoundary>
            </div>

            <div
              id="alert-section"
              className="col-span-1 md:col-span-2 lg:col-span-1 xl:col-span-1 row-span-2"
            >
              <ErrorBoundary fallbackText="Alerts Panel Error">
                <AlertPanel alerts={data?.alerts || []} />
              </ErrorBoundary>
            </div>

            <div className="col-span-1 md:col-span-2 lg:col-span-1 border-r border-slate-800 pr-0">
              <ErrorBoundary fallbackText="Map Render Error">
                {!data ? (
                  <div className="glass-panel h-[400px] animate-pulse bg-slate-800/40 rounded-xl" />
                ) : (
                  <MapComponent mapData={mapData} />
                )}
              </ErrorBoundary>
            </div>

            <div className="col-span-1 md:col-span-2 lg:col-span-2 xl:col-span-2">
              <ErrorBoundary fallbackText="Chart Render Error">
                {!data ? (
                  <div className="glass-panel h-[400px] animate-pulse bg-slate-800/40 rounded-xl" />
                ) : (
                  <Charts history={history} />
                )}
              </ErrorBoundary>
            </div>

            <PredictionPanel />
          </div>
        </ErrorBoundary>
      )}
      <VoiceAssistant />
    </main>
  );
}
