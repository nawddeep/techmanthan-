import Link from "next/link";
import { AlertTriangle } from "lucide-react";

export default function NotFound() {
  return (
    <div className="min-h-screen bg-[#0B0F19] flex flex-col items-center justify-center font-sans tracking-tight">
      <div className="glass-panel p-10 flex flex-col items-center max-w-sm text-center border border-slate-700/50 shadow-2xl">
        <div className="w-16 h-16 bg-red-500/10 rounded-full flex items-center justify-center mb-6">
          <AlertTriangle className="w-8 h-8 text-red-500" />
        </div>
        <h2 className="text-2xl font-black text-slate-100 mb-2 tracking-wide">404 — Page Not Found</h2>
        <p className="text-sm text-slate-400 mb-8 px-2 font-medium">
          The quadrant you are looking for does not exist in the active Smart City layout.
        </p>
        <Link 
          href="/" 
          className="px-6 py-2.5 bg-blue-600 hover:bg-blue-500 text-white rounded-md transition-colors font-bold uppercase tracking-widest shadow-lg shadow-blue-500/20 text-sm"
        >
          Back to Dashboard
        </Link>
      </div>
    </div>
  );
}
