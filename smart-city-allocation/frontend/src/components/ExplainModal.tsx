"use client";

import { motion, AnimatePresence } from "framer-motion";
import {
  X,
  Info,
  TrendingUp,
  TrendingDown,
  Target,
  BrainCircuit,
  Car,
  Clock,
  CloudRain,
  MapPin,
  Users,
  Trash2,
  Calendar,
  Gauge,
} from "lucide-react";

interface FeatureDetail {
  feature: string;
  display_name: string;
  value: number;
  impact: number;
  effect: "increase" | "decrease";
}

interface ExplainResponse {
  prediction: string;
  confidence: number;
  top_features: FeatureDetail[];
  explanation: string;
}

interface ExplainModalProps {
  isOpen: boolean;
  onClose: () => void;
  data: ExplainResponse | null;
  loading: boolean;
  title: string;
}

const getFeatureIcon = (feature: string) => {
  const f = feature.toLowerCase();
  if (f.includes("vehicle")) return <Car className="w-4 h-4 text-orange-400" />;
  if (f.includes("hour") || f.includes("time"))
    return <Clock className="w-4 h-4 text-blue-400" />;
  if (f.includes("weather"))
    return <CloudRain className="w-4 h-4 text-slate-400" />;
  if (f.includes("junction") || f.includes("location") || f.includes("area"))
    return <MapPin className="w-4 h-4 text-emerald-400" />;
  if (f.includes("population"))
    return <Users className="w-4 h-4 text-indigo-400" />;
  if (f.includes("bin") || f.includes("waste"))
    return <Trash2 className="w-4 h-4 text-rose-400" />;
  if (f.includes("day")) return <Calendar className="w-4 h-4 text-amber-400" />;
  if (f.includes("collection"))
    return <Gauge className="w-4 h-4 text-cyan-400" />;
  return <Target className="w-4 h-4 text-slate-400" />;
};

export default function ExplainModal({
  isOpen,
  onClose,
  data,
  loading,
  title,
}: ExplainModalProps) {
  if (!isOpen) return null;

  return (
    <AnimatePresence>
      <div className="fixed inset-0 z-50 flex items-center justify-center p-4">
        {/* Backdrop */}
        <motion.div
          initial={{ opacity: 0 }}
          animate={{ opacity: 1 }}
          exit={{ opacity: 0 }}
          onClick={onClose}
          className="absolute inset-0 bg-black/80 backdrop-blur-md"
        />

        {/* Modal content */}
        <motion.div
          initial={{ opacity: 0, scale: 0.9, y: 30, rotateX: -10 }}
          animate={{ opacity: 1, scale: 1, y: 0, rotateX: 0 }}
          exit={{ opacity: 0, scale: 0.9, y: 30, rotateX: 10 }}
          transition={{ type: "spring", damping: 25, stiffness: 300 }}
          className="relative w-full max-w-xl glass-panel overflow-hidden border-blue-500/30 shadow-[0_0_50px_-12px_rgba(59,130,246,0.3)] perspective-1000"
        >
          {/* Animated Header Background */}
          <div className="absolute top-0 left-0 w-full h-1 bg-gradient-to-r from-transparent via-blue-500 to-transparent" />

          {/* Header */}
          <div className="p-6 border-b border-white/5 flex justify-between items-center bg-slate-900/60 backdrop-blur-xl">
            <div className="flex items-center gap-4">
              <div className="relative">
                <div className="absolute inset-0 bg-blue-500/20 blur-xl rounded-full" />
                <div className="relative p-2.5 rounded-xl bg-gradient-to-br from-blue-500/20 to-blue-600/10 border border-blue-500/30 text-blue-400">
                  <BrainCircuit className="w-6 h-6 animate-pulse" />
                </div>
              </div>
              <div>
                <h2 className="text-xl font-black text-white tracking-tight">
                  AI EXPLAINABILITY
                </h2>
                <p className="text-[10px] text-blue-400 font-bold tracking-[0.2em] uppercase">
                  {title}
                </p>
              </div>
            </div>
            <button
              onClick={onClose}
              className="p-2 rounded-xl hover:bg-white/5 text-slate-400 hover:text-white transition-all active:scale-90"
            >
              <X className="w-6 h-6" />
            </button>
          </div>

          {/* Body */}
          <div className="p-8 space-y-8 max-h-[75vh] overflow-y-auto custom-scrollbar">
            {loading ? (
              <div className="py-24 flex flex-col items-center justify-center gap-6">
                <div className="relative w-16 h-16">
                  <motion.div
                    animate={{ rotate: 360 }}
                    transition={{
                      duration: 2,
                      repeat: Infinity,
                      ease: "linear",
                    }}
                    className="absolute inset-0 border-4 border-blue-500/10 rounded-full"
                  />
                  <motion.div
                    animate={{ rotate: -360 }}
                    transition={{
                      duration: 1.5,
                      repeat: Infinity,
                      ease: "linear",
                    }}
                    className="absolute inset-0 border-t-4 border-blue-500 rounded-full shadow-[0_0_15px_rgba(59,130,246,0.5)]"
                  />
                </div>
                <div className="flex flex-col items-center gap-1">
                  <span className="text-blue-400 font-black tracking-widest text-sm uppercase">
                    Processing SHAP Vectors
                  </span>
                  <span className="text-slate-500 text-[10px] font-bold">
                    Unpacking model decision trees...
                  </span>
                </div>
              </div>
            ) : data ? (
              <>
                {/* Confidence & Prediction Segment */}
                <div className="grid grid-cols-2 gap-4 p-5 rounded-2xl bg-gradient-to-br from-white/[0.03] to-transparent border border-white/[0.05] relative group overflow-hidden">
                  <div className="absolute -right-4 -bottom-4 w-24 h-24 bg-blue-500/5 blur-3xl rounded-full" />

                  <div className="space-y-1">
                    <span className="text-[10px] uppercase tracking-[0.2em] text-slate-500 font-black">
                      Prediction
                    </span>
                    <div className="text-2xl font-black text-white italic">
                      {data.prediction}
                    </div>
                  </div>

                  <div className="space-y-1 text-right">
                    <span className="text-[10px] uppercase tracking-[0.2em] text-slate-500 font-black">
                      Confidence
                    </span>
                    <div className="flex items-center justify-end gap-3 translate-y-1">
                      <div className="text-2xl font-black text-blue-400 tracking-tighter">
                        {data.confidence.toFixed(1)}%
                      </div>
                      <div className="w-12 h-1.5 bg-white/5 rounded-full overflow-hidden border border-white/5">
                        <motion.div
                          initial={{ width: 0 }}
                          animate={{ width: `${data.confidence}%` }}
                          transition={{ duration: 1, ease: "easeOut" }}
                          className="h-full bg-blue-500 shadow-[0_0_10px_rgba(59,130,246,0.5)]"
                        />
                      </div>
                    </div>
                  </div>
                </div>

                {/* Top Contributing Factors */}
                <div className="space-y-6">
                  <div className="flex items-center justify-between">
                    <h3 className="text-[11px] font-black text-slate-400 uppercase tracking-[0.3em] flex items-center gap-2">
                      Contributing Factors
                    </h3>
                    <div className="h-px flex-1 bg-gradient-to-r from-white/10 to-transparent ml-4" />
                  </div>

                  <div className="grid gap-5">
                    {data.top_features.map((feature, idx) => (
                      <motion.div
                        key={idx}
                        initial={{ opacity: 0, x: -20 }}
                        animate={{ opacity: 1, x: 0 }}
                        transition={{ delay: idx * 0.1 }}
                        className="group relative"
                      >
                        <div className="flex justify-between items-end mb-2.5 px-1">
                          <div className="flex items-center gap-3">
                            <div className="p-2 rounded-lg bg-white/5 border border-white/5 group-hover:border-blue-500/30 transition-colors">
                              {getFeatureIcon(feature.feature)}
                            </div>
                            <div className="flex flex-col">
                              <span className="text-sm font-bold text-slate-100 group-hover:text-blue-400 transition-colors tracking-tight">
                                {feature.display_name}
                              </span>
                              <span className="text-[10px] text-slate-500 font-medium">
                                Recorded Value:{" "}
                                <span className="text-slate-300 font-bold">
                                  {feature.value}
                                </span>
                              </span>
                            </div>
                          </div>
                          <div
                            className={`flex items-center gap-1.5 text-[10px] font-black uppercase tracking-tighter px-2.5 py-1 rounded-full border ${
                              feature.effect === "increase"
                                ? "text-rose-400 bg-rose-500/10 border-rose-500/20"
                                : "text-emerald-400 bg-emerald-500/10 border-emerald-500/20"
                            }`}
                          >
                            {feature.effect === "increase" ? (
                              <TrendingUp className="w-3 h-3" />
                            ) : (
                              <TrendingDown className="w-3 h-3" />
                            )}
                            {feature.effect === "increase"
                              ? "High Impact"
                              : "Lowers Risk"}
                          </div>
                        </div>

                        <div className="relative h-8 bg-white/5 rounded-xl overflow-hidden border border-white/5 p-[1px]">
                          <motion.div
                            initial={{ width: 0 }}
                            animate={{
                              width: `${Math.min(Math.abs(feature.impact) * 200, 100)}%`,
                            }}
                            transition={{
                              duration: 1.2,
                              ease: "circOut",
                              delay: 0.2 + idx * 0.1,
                            }}
                            className={`h-full rounded-lg ${
                              feature.effect === "increase"
                                ? "bg-gradient-to-r from-rose-600 via-rose-500 to-rose-400"
                                : "bg-gradient-to-r from-emerald-600 via-emerald-500 to-emerald-400"
                            } opacity-90 relative`}
                          >
                            <div className="absolute inset-0 bg-gradient-to-b from-white/20 to-transparent pointer-events-none" />
                          </motion.div>

                          <div className="absolute inset-0 flex items-center px-4 justify-between pointer-events-none">
                            <span className="text-[10px] text-white font-black drop-shadow-md">
                              {Math.abs(feature.impact * 100).toFixed(0)}%
                              INFLUENCE
                            </span>
                          </div>
                        </div>
                      </motion.div>
                    ))}
                  </div>
                </div>

                {/* Human-Readable Summary */}
                <motion.div
                  initial={{ opacity: 0, y: 10 }}
                  animate={{ opacity: 1, y: 0 }}
                  transition={{ delay: 0.5 }}
                  className="relative p-6 rounded-2xl bg-blue-500/5 border border-blue-500/10 overflow-hidden"
                >
                  <div className="absolute top-0 left-0 w-1 h-full bg-blue-500/40" />
                  <h3 className="text-[10px] font-black text-blue-400 uppercase tracking-[0.2em] mb-3 flex items-center gap-2">
                    <Info className="w-4 h-4" /> HUMAN-READABLE SUMMARY
                  </h3>
                  <p className="text-slate-200 leading-relaxed text-sm font-medium italic mb-2">
                    "{data.explanation}"
                  </p>
                  <p className="text-[10px] text-slate-500 font-bold uppercase tracking-tight">
                    * Derived via SHAP (Shapley Additive Explanations) framework
                  </p>
                </motion.div>
              </>
            ) : (
              <div className="text-center py-16">
                <div className="w-12 h-12 rounded-full bg-white/5 border border-white/5 flex items-center justify-center mx-auto mb-4">
                  <X className="text-slate-600" />
                </div>
                <h3 className="text-slate-400 font-bold">
                  Failed to load explainer data
                </h3>
                <p className="text-slate-600 text-sm">
                  Please refresh or try a different metric.
                </p>
              </div>
            )}
          </div>

          {/* Footer */}
          <div className="p-6 bg-slate-900/60 backdrop-blur-xl border-t border-white/5 flex justify-between items-center">
            <div className="flex gap-4">
              <div className="w-1 h-1 rounded-full bg-blue-500 shadow-[0_0_5px_rgba(59,130,246,1)]" />
              <div className="w-1 h-1 rounded-full bg-blue-500/30" />
              <div className="w-1 h-1 rounded-full bg-blue-500/10" />
            </div>
            <p className="text-[10px] text-slate-500 font-black tracking-[.2em] uppercase">
              SMART-CITY PROTOCOL • AX-74
            </p>
          </div>
        </motion.div>
      </div>
    </AnimatePresence>
  );
}
