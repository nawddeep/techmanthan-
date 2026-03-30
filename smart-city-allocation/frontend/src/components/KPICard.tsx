import { motion } from "framer-motion";
import { useState, ReactNode } from "react";
import { BrainCircuit } from "lucide-react";
import axios from "axios";
import ExplainModal from "./ExplainModal";

interface KPICardProps {
  title: string;
  value: string | number;
  statusText?: string;
  statusLevel?: "Low" | "Medium" | "High" | "Normal" | "Overflow";
  icon?: ReactNode;
  apiPath?: string;
  features?: any;
}

export default function KPICard({ title, value, statusText, statusLevel, icon, apiPath, features }: KPICardProps) {
  const [showModal, setShowModal] = useState(false);
  const [loading, setLoading] = useState(false);
  const [explainData, setExplainData] = useState<any>(null);

  const handleExplain = async () => {
    if (!apiPath || !features) return;
    
    setShowModal(true);
    setLoading(true);
    try {
      const res = await axios.post(apiPath, features);
      setExplainData(res.data);
    } catch (err) {
      console.error("Failed to fetch explanation:", err);
    } finally {
      setLoading(false);
    }
  };

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
    <>
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
          <div className="flex items-center gap-2">
            {apiPath && features && (
              <button 
                onClick={handleExplain}
                className="group text-[10px] font-black px-3 py-1.5 rounded-full bg-blue-500/10 text-blue-400 border border-blue-500/20 hover:bg-blue-500 hover:text-white transition-all flex items-center gap-1.5 active:scale-90 cursor-pointer shadow-[0_0_15px_rgba(59,130,246,0.1)] hover:shadow-[0_0_20px_rgba(59,130,246,0.3)] uppercase tracking-widest"
              >
                <BrainCircuit className="w-3 h-3 group-hover:rotate-12 transition-transform" /> Why?
              </button>
            )}
            {statusText && (
              <div className={`text-sm font-medium px-2 py-1 rounded-md bg-opacity-20 ${getStatusColor()} bg-current`}>
                {statusText}
              </div>
            )}
          </div>
        </div>
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
