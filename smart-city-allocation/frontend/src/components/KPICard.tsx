"use client";

import { motion } from "framer-motion";
import { useState, ReactNode } from "react";
import { BrainCircuit } from "lucide-react";
import {
  LineChart,
  Line,
  ResponsiveContainer,
  YAxis,
} from "recharts";
import api from "@/lib/api";
import ExplainModal from "./ExplainModal";

interface KPICardProps {
  title: string;
  value: string | number;
  subText?: string;
  statusText?: string;
  statusLevel?: "Low" | "Medium" | "High" | "Normal" | "Overflow" | string;
  icon?: ReactNode;
  explainPath?: string;
  features?: any;
  sparkline?: number[];
  thresholdPct?: number;
}

export default function KPICard({
  title,
  value,
  subText,
  statusText,
  statusLevel,
  icon,
  explainPath,
  features,
  sparkline,
  thresholdPct = 80,
}: KPICardProps) {
  const [showModal, setShowModal] = useState(false);
  const [showExpanded, setShowExpanded] = useState(false);
  const [loading, setLoading] = useState(false);
  const [explainData, setExplainData] = useState<any>(null);

  const numericVal =
    typeof value === "string" && value.endsWith("%")
      ? parseFloat(value.replace("%", ""))
      : typeof value === "number"
        ? value
        : NaN;
  const overThreshold =
    !Number.isNaN(numericVal) && numericVal >= thresholdPct;

  const handleExplain = async () => {
    if (!explainPath || !features) return;
    setShowModal(true);
    setLoading(true);
    try {
      const res = await api.post(explainPath, features);
      setExplainData(res.data);
    } catch (err) {
      console.error("Failed to fetch explanation:", err);
    } finally {
      setLoading(false);
    }
  };

  const getStatusColor = () => {
    switch (String(statusLevel || "").toLowerCase()) {
      case "low":
      case "normal":
        return "text-green-500";
      case "medium":
      case "warning":
        return "text-yellow-400";
      case "high":
      case "overflow":
      case "critical":
        return "text-red-500";
      default:
        return "text-blue-400";
    }
  };

  const chartData =
    sparkline?.length && sparkline.length > 0
      ? sparkline.map((v, i) => ({ i, v }))
      : [{ i: 0, v: 50 }];

  return (
    <>
      <motion.div
        className={`glass-panel p-6 flex flex-col justify-between cursor-pointer ${showExpanded ? "ring-2 ring-blue-500/50" : ""}`}
        initial={{ opacity: 0, y: 20 }}
        animate={{ opacity: 1, y: 0 }}
        transition={{ duration: 0.5 }}
        onClick={() => setShowExpanded((s) => !s)}
      >
        <div className="flex justify-between items-center mb-2 text-slate-400">
          <h3 className="text-sm font-semibold uppercase tracking-wider">{title}</h3>
          {icon && <div className="text-blue-500 opacity-60">{icon}</div>}
        </div>

        {sparkline && sparkline.length > 1 && (
          <div className="h-10 w-full mb-2 opacity-80">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chartData}>
                <YAxis hide domain={["dataMin - 5", "dataMax + 5"]} />
                <Line
                  type="monotone"
                  dataKey="v"
                  stroke={overThreshold ? "#f87171" : "#60a5fa"}
                  strokeWidth={2}
                  dot={false}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        )}

        <div className="flex items-end justify-between mt-1">
          <div className="flex flex-col items-start">
            <div
              className={`text-4xl font-bold text-slate-100 ${overThreshold ? "animate-pulse text-red-300" : ""}`}
            >
              {value}
            </div>
            {subText && (
              <div className="text-[11px] text-slate-400 font-medium tracking-wide mt-1">
                {subText}
              </div>
            )}
          </div>
          <div className="flex flex-col items-end gap-2">
            {explainPath && features && (
              <button
                type="button"
                onClick={(e) => {
                  e.stopPropagation();
                  handleExplain();
                }}
                className="group text-[10px] font-black px-3 py-1.5 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20 hover:bg-blue-500 hover:text-white transition-all flex items-center gap-1.5 uppercase tracking-widest"
              >
                <BrainCircuit className="w-3 h-3 group-hover:rotate-12 transition-transform" />{" "}
                Why?
              </button>
            )}
            {statusText && (
              <div
                className={`text-sm font-medium px-2 py-1 rounded-md bg-opacity-20 ${getStatusColor()} bg-current ${overThreshold ? "ring-2 ring-red-500/40" : ""}`}
              >
                {statusText}
              </div>
            )}
          </div>
        </div>

        {showExpanded && sparkline && sparkline.length > 1 && (
          <div className="mt-4 h-40 border border-slate-700/50 rounded-lg overflow-hidden p-2">
            <ResponsiveContainer width="100%" height="100%">
              <LineChart data={chartData}>
                <YAxis stroke="#64748b" fontSize={10} />
                <Line
                  type="monotone"
                  dataKey="v"
                  stroke="#38bdf8"
                  strokeWidth={2}
                  dot={false}
                />
              </LineChart>
            </ResponsiveContainer>
          </div>
        )}
      </motion.div>

      <ExplainModal
        isOpen={showModal}
        onClose={() => setShowModal(false)}
        data={explainData}
        loading={loading}
        title={title}
      />
    </>
  );
}
