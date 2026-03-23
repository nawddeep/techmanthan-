"use client";

import { motion, AnimatePresence } from "framer-motion";
import { AlertTriangle, Info, AlertOctagon } from "lucide-react";

interface AlertPanelProps {
  alerts: string[];
}

export default function AlertPanel({ alerts }: AlertPanelProps) {
  return (
    <div className="glass-panel p-6 h-full flex flex-col">
      <div className="flex items-center gap-2 mb-6">
        <AlertTriangle className="text-yellow-400 w-5 h-5" />
        <h2 className="text-lg font-semibold tracking-wide text-slate-200 uppercase">Active Alerts</h2>
      </div>

      <div className="flex-1 overflow-y-auto pr-2 space-y-3">
        {alerts.length === 0 ? (
          <div className="text-slate-500 text-sm flex items-center gap-2">
            <Info className="w-4 h-4" /> No active alerts in the city.
          </div>
        ) : (
          <AnimatePresence>
            {alerts.map((alert, idx) => {
              // Extremely rough heuristic for severity based on text
              const isCritical = alert.toLowerCase().includes("overflow") || alert.toLowerCase().includes("critical");
              
              return (
                <motion.div
                  key={idx + alert}
                  initial={{ opacity: 0, x: -20 }}
                  animate={{ opacity: 1, x: 0 }}
                  exit={{ opacity: 0, scale: 0.95 }}
                  className={`p-4 rounded-lg border flex items-start gap-3 ${
                    isCritical 
                      ? "bg-red-500/10 border-red-500/30 text-red-200 animate-pulse" 
                      : "bg-yellow-400/10 border-yellow-400/30 text-yellow-200"
                  }`}
                >
                  <div className="mt-0.5">
                    {isCritical ? <AlertOctagon className="w-4 h-4 text-red-400" /> : <AlertTriangle className="w-4 h-4 text-yellow-400" />}
                  </div>
                  <p className="text-sm">{alert}</p>
                </motion.div>
              );
            })}
          </AnimatePresence>
        )}
      </div>
    </div>
  );
}
