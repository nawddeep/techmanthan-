"use client";

import { motion } from "framer-motion";
import { ReactNode } from "react";

interface KPICardProps {
  title: string;
  value: string | number;
  statusText?: string;
  statusLevel?: "Low" | "Medium" | "High" | "Normal" | "Overflow";
  icon?: ReactNode;
}

export default function KPICard({ title, value, statusText, statusLevel, icon }: KPICardProps) {
  const getStatusColor = () => {
    switch (statusLevel?.toLowerCase()) {
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

  return (
    <motion.div 
      className="glass-panel p-6 flex flex-col justify-between"
      initial={{ opacity: 0, y: 20 }}
      animate={{ opacity: 1, y: 0 }}
      transition={{ duration: 0.5 }}
    >
      <div className="flex justify-between items-center mb-4 text-slate-400">
        <h3 className="text-sm font-semibold uppercase tracking-wider">{title}</h3>
        {icon && <div className="text-blue-500 opacity-60">{icon}</div>}
      </div>
      
      <div className="flex items-end justify-between">
        <div className="text-4xl font-bold text-slate-100">{value}</div>
        {statusText && (
          <div className={`text-sm font-medium px-2 py-1 rounded-md bg-opacity-20 ${getStatusColor()} bg-current`}>
            {statusText}
          </div>
        )}
      </div>
    </motion.div>
  );
}
