"use client";

import { motion } from "framer-motion";
import { IndianRupee, TrendingUp, PiggyBank } from "lucide-react";

interface ROICardProps {
  roiData: {
    baseline_cost: number;
    optimized_cost: number;
    monthly_savings: number;
    savings_percentage: number;
    annual_projection: number;
    explanation: string;
  };
}

export default function ROICard({ roiData }: ROICardProps) {
  if (!roiData) return null;

  return (
    <motion.div 
      className="glass-panel p-6 flex flex-col justify-between border-emerald-500/20 bg-gradient-to-br from-emerald-500/10 to-transparent relative overflow-hidden"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5, delay: 0.2 }}
    >
      {/* Decorative background element */}
      <div className="absolute -right-4 -bottom-4 opacity-10 blur-xl">
        <PiggyBank className="w-32 h-32 text-emerald-500" />
      </div>

      <div className="flex justify-between items-center mb-4 text-emerald-400 z-10">
        <h3 className="text-sm font-semibold uppercase tracking-wider flex items-center gap-2">
          <TrendingUp className="w-4 h-4" /> AI Financial Impact
        </h3>
        <span className="text-xs px-2 py-1 bg-emerald-500/20 rounded-full font-medium">Monthly Savings</span>
      </div>
      
      <div className="z-10 mt-2">
        <div className="flex items-center text-4xl font-bold text-white mb-1">
          <IndianRupee className="w-8 h-8 mr-1 text-emerald-400" />
          {roiData.monthly_savings.toLocaleString('en-IN')}
        </div>
        <div className="flex items-center justify-between text-sm">
          <div className="flex items-center gap-2">
            <span className="text-emerald-400 font-medium">+{roiData.savings_percentage}% Efficiency</span>
            <span className="text-slate-400 text-xs">vs Manual (₹{roiData.baseline_cost.toLocaleString('en-IN')})</span>
          </div>
          <span className="text-emerald-500/70 text-xs font-bold uppercase tracking-wider">
             ₹{roiData.annual_projection.toLocaleString('en-IN')} / Yr
          </span>
        </div>
      </div>
      
      {/* Mini cost comparison bar */}
      <div className="mt-5 z-10">
        <div className="flex justify-between text-[10px] text-slate-400 mb-1 uppercase tracking-wider">
          <span>AI Process Cost</span>
          <span>Base Cost</span>
        </div>
        <div className="w-full h-2 bg-slate-700 rounded-full overflow-hidden flex">
          <div 
            className="h-full bg-emerald-500 rounded-l-full" 
            style={{ width: `${100 - roiData.savings_percentage}%` }}
            title={`AI Optimized Cost: ₹${roiData.optimized_cost}`}
          ></div>
          <div 
            className="h-full bg-slate-500 rounded-r-full"
            style={{ width: `${roiData.savings_percentage}%` }}
            title={`Savings: ₹${roiData.monthly_savings}`}
          ></div>
        </div>
      </div>
      
      {/* Explanation text */}
      <div className="z-10 mt-3 text-[10px] text-slate-400 italic border-t border-emerald-500/20 pt-2 tracking-wide font-medium leading-relaxed">
        {roiData.explanation}
      </div>
    </motion.div>
  );
}
