import { motion } from "framer-motion";

export default function HealthScoreCard({ score }: { score: number }) {
  let status = "HEALTHY";
  let color = "text-green-500";
  let bgBlend = "bg-green-500/10 border-green-500";
  let strokeColor = "#22c55e"; // green-500
  
  if (score < 40) {
    status = "CRITICAL";
    color = "text-red-500";
    bgBlend = "bg-red-500/10 border-red-500";
    strokeColor = "#ef4444"; // red-500
  } else if (score < 70) {
    status = "STRESSED";
    color = "text-yellow-400";
    bgBlend = "bg-yellow-400/10 border-yellow-400";
    strokeColor = "#facc15"; // yellow-400
  }

  const radius = 35;
  const circumference = 2 * Math.PI * radius;
  const strokeDashoffset = circumference - (score / 100) * circumference;

  return (
    <motion.div 
      className="glass-panel p-6 flex flex-col justify-between items-center relative overflow-hidden"
      initial={{ opacity: 0, scale: 0.95 }}
      animate={{ opacity: 1, scale: 1 }}
      transition={{ duration: 0.5 }}
    >
      <div className="absolute top-4 left-4 text-slate-400 text-sm font-semibold uppercase tracking-wider">
        City Health
      </div>
      
      <div className="relative flex items-center justify-center mt-6">
        <svg className="w-28 h-28 transform -rotate-90">
          <circle
            className="text-slate-800"
            strokeWidth="8"
            stroke="currentColor"
            fill="transparent"
            r={radius}
            cx="56"
            cy="56"
          />
          <motion.circle
            stroke={strokeColor}
            strokeWidth="8"
            strokeDasharray={circumference}
            initial={{ strokeDashoffset: circumference }}
            animate={{ strokeDashoffset }}
            transition={{ duration: 1.5, ease: "easeOut" }}
            strokeLinecap="round"
            fill="transparent"
            r={radius}
            cx="56"
            cy="56"
          />
        </svg>
        <div className="absolute flex flex-col items-center justify-center">
          <span className="text-3xl font-bold text-slate-100">{Math.round(score)}</span>
        </div>
      </div>
      
      <div className={`mt-4 text-xs font-bold tracking-widest px-3 py-1 bg-opacity-10 rounded-full border ${bgBlend} ${color}`}>
        {status}
      </div>
    </motion.div>
  );
}
