"use client";

import { useEffect, useState } from "react";
import Link from "next/link";
import {
  BarChart,
  Bar,
  XAxis,
  YAxis,
  Tooltip,
  ResponsiveContainer,
  CartesianGrid,
} from "recharts";
import api from "@/lib/api";

export default function ModelStatsPage() {
  const [data, setData] = useState<any>(null);
  const [err, setErr] = useState("");

  useEffect(() => {
    api
      .get("/models/stats")
      .then((r) => setData(r.data))
      .catch((e) => setErr(e?.message || "Failed to load"));
  }, []);

  if (err) return <div className="p-8 text-red-400">{err}</div>;
  if (!data) return <div className="p-8 text-slate-400">Loading metrics…</div>;

  const sections = ["traffic", "waste", "emergency"] as const;

  return (
    <div className="min-h-screen bg-slate-950 text-slate-100 p-6 md:p-10">
      <div className="max-w-6xl mx-auto">
        <Link href="/" className="text-blue-400 text-sm hover:underline mb-6 inline-block">
          ← Dashboard
        </Link>
        <h1 className="text-3xl font-bold mb-8">Model performance</h1>
        <div className="space-y-12">
          {sections.map((key) => {
            const m = data[key];
            if (!m || m.error) {
              return (
                <div key={key} className="bg-slate-900/60 border border-slate-800 rounded-xl p-6">
                  <h2 className="text-lg font-semibold capitalize mb-2">{key}</h2>
                  <p className="text-red-400 text-sm">{m?.error || "Unavailable"}</p>
                </div>
              );
            }
            const fi = Object.entries(m.feature_importance || {}).map(([name, v]) => ({
              name,
              v: Number(v),
            }));
            return (
              <div key={key} className="bg-slate-900/60 border border-slate-800 rounded-xl p-6">
                <h2 className="text-xl font-semibold capitalize mb-4">{key}</h2>
                <div className="grid md:grid-cols-2 gap-8">
                  <div>
                    <p className="text-sm text-slate-400 mb-2">
                      Accuracy {m.accuracy?.toFixed(3)} · Precision {m.precision?.toFixed(3)} · Recall{" "}
                      {m.recall?.toFixed(3)} · F1 {m.f1?.toFixed(3)}
                      {m.roc_auc != null && ` · AUC ${m.roc_auc.toFixed(3)}`}
                    </p>
                    <div className="h-48 bg-slate-900/50 rounded-lg p-2">
                      <ResponsiveContainer width="100%" height="100%">
                        <BarChart data={fi}>
                          <CartesianGrid strokeDasharray="3 3" stroke="#334155" />
                          <XAxis dataKey="name" tick={{ fontSize: 10 }} stroke="#94a3b8" />
                          <YAxis stroke="#94a3b8" />
                          <Tooltip />
                          <Bar dataKey="v" fill="#38bdf8" />
                        </BarChart>
                      </ResponsiveContainer>
                    </div>
                  </div>
                  <div>
                    <p className="text-sm text-slate-400 mb-2">Confusion matrix</p>
                    <pre className="text-xs bg-slate-900 p-4 rounded-lg overflow-auto text-emerald-300">
                      {JSON.stringify(m.confusion_matrix, null, 2)}
                    </pre>
                  </div>
                </div>
              </div>
            );
          })}
        </div>
      </div>
    </div>
  );
}
