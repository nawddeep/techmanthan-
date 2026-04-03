"use client";

import {
  LineChart,
  Line,
  XAxis,
  YAxis,
  CartesianGrid,
  Tooltip,
  ResponsiveContainer,
  Legend,
} from "recharts";
import { Activity } from "lucide-react";
import { useEffect, useState } from "react";

interface ChartsProps {
  history: {
    time: string;
    traffic: number;
    waste: number;
  }[];
}

export default function Charts({ history }: ChartsProps) {
  // Give the system 30 seconds before showing the "no data" placeholder —
  // this prevents a flash of the empty state on initial page load.
  const [pastGracePeriod, setPastGracePeriod] = useState(false);

  useEffect(() => {
    const timer = setTimeout(() => setPastGracePeriod(true), 30_000);
    return () => clearTimeout(timer);
  }, []);

  const isEmpty = history.length === 0;

  return (
    <div className="glass-panel p-6 h-[400px] flex flex-col">
      <h2 className="text-lg font-semibold tracking-wide text-slate-200 uppercase mb-6">
        Real-Time Metrics Trend
      </h2>

      {isEmpty ? (
        // Empty state — shown after 30 s grace period, or immediately on is_fallback
        <div className="flex-1 flex flex-col items-center justify-center gap-3">
          <Activity
            className={`w-10 h-10 text-blue-500/50 ${
              !pastGracePeriod ? "animate-pulse" : ""
            }`}
          />
          <p className="text-slate-400 text-sm font-medium">
            {pastGracePeriod
              ? "No historical data available"
              : "Collecting data, please wait…"}
          </p>
          <p className="text-slate-600 text-xs text-center max-w-xs">
            {pastGracePeriod
              ? "Data will appear here once the simulation has run for a few cycles."
              : "The system is warming up. Live metrics will appear shortly."}
          </p>
        </div>
      ) : (
        <div className="flex-1 w-full -ml-4">
          <ResponsiveContainer width="100%" height="100%">
            <LineChart data={history}>
              <CartesianGrid
                strokeDasharray="3 3"
                stroke="#1e293b"
                vertical={false}
              />
              <XAxis
                dataKey="time"
                stroke="#64748b"
                fontSize={12}
                tickLine={false}
                axisLine={false}
              />
              <YAxis
                stroke="#64748b"
                fontSize={12}
                tickLine={false}
                axisLine={false}
                domain={[0, 100]}
              />
              <Tooltip
                contentStyle={{
                  backgroundColor: "#0f172a",
                  border: "1px solid #1e293b",
                  borderRadius: "8px",
                }}
                itemStyle={{ color: "#e2e8f0" }}
              />
              <Legend
                verticalAlign="top"
                height={36}
                wrapperStyle={{ fontSize: "12px", color: "#94a3b8" }}
                iconType="circle"
              />
              <Line
                type="monotone"
                dataKey="traffic"
                stroke="#3B82F6"
                strokeWidth={3}
                dot={false}
                activeDot={{ r: 6 }}
                name="Traffic Level"
              />
              <Line
                type="monotone"
                dataKey="waste"
                stroke="#22C55E"
                strokeWidth={3}
                dot={false}
                activeDot={{ r: 6 }}
                name="Waste Fill %"
              />
            </LineChart>
          </ResponsiveContainer>
        </div>
      )}
    </div>
  );
}
