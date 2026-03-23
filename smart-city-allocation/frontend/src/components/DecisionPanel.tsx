"use client";

import { motion } from "framer-motion";
import { Zap, ShieldAlert, Navigation } from "lucide-react";

interface DecisionPanelProps {
  actions: string[];
}

export default function DecisionPanel({ actions }: DecisionPanelProps) {
  // Map some basic icons based on keyword
  const getActionIcon = (text: string) => {
    const lower = text.toLowerCase();
    if (lower.includes("police") || lower.includes("control")) return <Navigation className="w-5 h-5 text-blue-400" />;
    if (lower.includes("emergency") || lower.includes("critical")) return <ShieldAlert className="w-5 h-5 text-red-500" />;
    return <Zap className="w-5 h-5 text-green-400" />;
  };

  return (
    <div className="glass-panel p-6 border-blue-500/30 bg-blue-900/10 shadow-[0_0_15px_rgba(59,130,246,0.1)] col-span-1 md:col-span-2 lg:col-span-3">
      <div className="flex items-center gap-2 mb-6 border-b border-slate-700/50 pb-4">
        <div className="bg-blue-500/20 p-2 rounded-lg">
          <Zap className="text-blue-400 w-6 h-6 animate-pulse" />
        </div>
        <div>
          <h2 className="text-xl font-bold tracking-wide text-slate-100 uppercase">AI Decision Engine</h2>
          <p className="text-xs text-blue-400">Real-time system recommendations</p>
        </div>
      </div>

      <div className="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
        {actions.length === 0 ? (
          <div className="text-slate-400 col-span-full">Standing by for actionable events...</div>
        ) : (
          actions.map((action, idx) => (
            <motion.div
              key={idx + action}
              initial={{ opacity: 0, y: 15 }}
              animate={{ opacity: 1, y: 0 }}
              transition={{ delay: idx * 0.1, duration: 0.4 }}
              className="p-5 rounded-xl bg-slate-800/50 border border-slate-700 shadow-inner flex flex-col gap-3"
            >
              <div className="w-10 h-10 rounded-full bg-slate-900 flex items-center justify-center shadow-lg border border-slate-700/50">
                {getActionIcon(action)}
              </div>
              <p className="text-slate-200 font-medium leading-snug">{action}</p>
              
              <div className="mt-auto pt-4 flex items-center gap-2">
                <span className="relative flex h-2 w-2">
                  <span className="animate-ping absolute inline-flex h-full w-full rounded-full bg-blue-400 opacity-75"></span>
                  <span className="relative inline-flex rounded-full h-2 w-2 bg-blue-500"></span>
                </span>
                <span className="text-xs text-slate-500 font-mono">EXECUTING</span>
              </div>
            </motion.div>
          ))
        )}
      </div>
    </div>
  );
}
