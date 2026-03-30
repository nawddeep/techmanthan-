"use client";

import React, { Component, ErrorInfo, ReactNode } from "react";
import { AlertCircle } from "lucide-react";

interface Props {
  children?: ReactNode;
  fallbackText?: string;
}

interface State {
  hasError: boolean;
}

export default class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false
  };

  public static getDerivedStateFromError(_: Error): State {
    return { hasError: true };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error("Uncaught error:", error, errorInfo);
  }

  public render() {
    if (this.state.hasError) {
      return (
        <div className="flex flex-col items-center justify-center p-6 bg-slate-900/50 rounded-xl border border-red-500/20 text-center min-h-[200px] w-full h-full">
          <AlertCircle className="w-10 h-10 text-red-500/80 mb-3" />
          <h2 className="text-sm font-bold text-slate-200 uppercase tracking-wider">{this.props.fallbackText || "Something went wrong"}</h2>
          <p className="text-xs text-slate-400 mt-2 mb-4">Please refresh the page</p>
          <button
            onClick={() => this.setState({ hasError: false })}
            className="px-3 py-1.5 bg-blue-600/20 text-blue-400 hover:bg-blue-600 hover:text-white rounded-md transition-colors border border-blue-500/50 text-xs font-bold uppercase tracking-widest"
          >
            Retry
          </button>
        </div>
      );
    }

    return this.props.children;
  }
}
