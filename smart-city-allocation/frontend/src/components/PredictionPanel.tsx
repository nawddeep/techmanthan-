"use client";

import { useState } from "react";
import api from "@/lib/api";

export default function PredictionPanel() {
  const [th, setTh] = useState(14);
  const [td, setTd] = useState(3);
  const [tj, setTj] = useState(2);
  const [tw, setTw] = useState(0);
  const [tv, setTv] = useState(250);
  const [tOut, setTOut] = useState<any>(null);

  const [wa, setWa] = useState(2);
  const [wd, setWd] = useState(3);
  const [wp, setWp] = useState(2);
  const [wl, setWl] = useState(4);
  const [wb, setWb] = useState(72);
  const [wOut, setWOut] = useState<any>(null);

  const runTraffic = async () => {
    const res = await api.post("/predict/traffic", {
      hour: th,
      day_enc: td,
      junction_enc: tj,
      weather_enc: tw,
      vehicles: tv,
    });
    setTOut(res.data);
    const ex = await api.post("/explain/traffic", {
      hour: th,
      day_enc: td,
      junction_enc: tj,
      weather_enc: tw,
      vehicles: tv,
    });
    setTOut((o: any) => ({ ...o, explain: ex.data }));
  };

  const runWaste = async () => {
    const res = await api.post("/predict/waste", {
      area: wa,
      day_of_week: wd,
      population_density: wp * 1000,
      last_collection_days: wl,
      bin_fill_pct: wb,
    });
    setWOut(res.data);
    const ex = await api.post("/explain/waste", {
      area: wa,
      day_of_week: wd,
      population_density: wp * 1000,
      last_collection_days: wl,
      bin_fill_pct: wb,
    });
    setWOut((o: any) => ({ ...o, explain: ex.data }));
  };

  return (
    <div className="glass-panel p-6 col-span-1 md:col-span-2 xl:col-span-5 border border-slate-700/60">
      <h3 className="text-sm font-bold uppercase tracking-wider text-slate-300 mb-4">
        Interactive ML predictions
      </h3>
      <div className="grid md:grid-cols-2 gap-8">
        <div>
          <p className="text-xs text-slate-500 mb-2">Traffic model</p>
          <div className="grid grid-cols-2 gap-2 text-xs">
            <label className="text-slate-400">
              Hour
              <input
                type="number"
                className="w-full bg-slate-800 border border-slate-600 rounded px-2 py-1 text-slate-100"
                value={th}
                onChange={(e) => setTh(+e.target.value)}
              />
            </label>
            <label className="text-slate-400">
              Day enc
              <input
                type="number"
                className="w-full bg-slate-800 border border-slate-600 rounded px-2 py-1"
                value={td}
                onChange={(e) => setTd(+e.target.value)}
              />
            </label>
            <label className="text-slate-400">
              Junction
              <input
                type="number"
                className="w-full bg-slate-800 border border-slate-600 rounded px-2 py-1"
                value={tj}
                onChange={(e) => setTj(+e.target.value)}
              />
            </label>
            <label className="text-slate-400">
              Weather
              <input
                type="number"
                className="w-full bg-slate-800 border border-slate-600 rounded px-2 py-1"
                value={tw}
                onChange={(e) => setTw(+e.target.value)}
              />
            </label>
            <label className="text-slate-400 col-span-2">
              Vehicles
              <input
                type="number"
                className="w-full bg-slate-800 border border-slate-600 rounded px-2 py-1"
                value={tv}
                onChange={(e) => setTv(+e.target.value)}
              />
            </label>
          </div>
          <button
            type="button"
            onClick={runTraffic}
            className="mt-3 px-4 py-2 bg-blue-600 hover:bg-blue-500 rounded-lg text-sm font-semibold text-white"
          >
            Predict + SHAP
          </button>
          {tOut && (
            <pre className="mt-3 text-[11px] text-slate-400 whitespace-pre-wrap bg-slate-900/50 p-2 rounded max-h-48 overflow-auto">
              {JSON.stringify(tOut, null, 2)}
            </pre>
          )}
        </div>
        <div>
          <p className="text-xs text-slate-500 mb-2">Waste model</p>
          <div className="grid grid-cols-2 gap-2 text-xs">
            <label className="text-slate-400">
              Area
              <input
                type="number"
                className="w-full bg-slate-800 border border-slate-600 rounded px-2 py-1"
                value={wa}
                onChange={(e) => setWa(+e.target.value)}
              />
            </label>
            <label className="text-slate-400">
              Day
              <input
                type="number"
                className="w-full bg-slate-800 border border-slate-600 rounded px-2 py-1"
                value={wd}
                onChange={(e) => setWd(+e.target.value)}
              />
            </label>
            <label className="text-slate-400">
              Pop. dens (k)
              <input
                type="number"
                className="w-full bg-slate-800 border border-slate-600 rounded px-2 py-1"
                value={wp}
                onChange={(e) => setWp(+e.target.value)}
              />
            </label>
            <label className="text-slate-400">
              Days since coll.
              <input
                type="number"
                className="w-full bg-slate-800 border border-slate-600 rounded px-2 py-1"
                value={wl}
                onChange={(e) => setWl(+e.target.value)}
              />
            </label>
            <label className="text-slate-400 col-span-2">
              Bin fill %
              <input
                type="number"
                className="w-full bg-slate-800 border border-slate-600 rounded px-2 py-1"
                value={wb}
                onChange={(e) => setWb(+e.target.value)}
              />
            </label>
          </div>
          <button
            type="button"
            onClick={runWaste}
            className="mt-3 px-4 py-2 bg-emerald-600 hover:bg-emerald-500 rounded-lg text-sm font-semibold text-white"
          >
            Predict + SHAP
          </button>
          {wOut && (
            <pre className="mt-3 text-[11px] text-slate-400 whitespace-pre-wrap bg-slate-900/50 p-2 rounded max-h-48 overflow-auto">
              {JSON.stringify(wOut, null, 2)}
            </pre>
          )}
        </div>
      </div>
    </div>
  );
}
