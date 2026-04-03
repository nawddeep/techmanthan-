"use client";

import React, { Component, ErrorInfo, ReactNode } from "react";
import { AlertCircle, RefreshCw } from "lucide-react";

interface Props {
  children?: ReactNode;
  fallbackText?: string;
  /** Optional callback to run before remounting — e.g. refetch data */
  onRetry?: () => void;
}

interface State {
  hasError: boolean;
  /** Increment to force a full remount of children on retry */
  retryKey: number;
}

export default class ErrorBoundary extends Component<Props, State> {
  public state: State = {
    hasError: false,
    retryKey: 0,
  };

  public static getDerivedStateFromError(_: Error): Partial<State> {
    return { hasError: true };
  }

  public componentDidCatch(error: Error, errorInfo: ErrorInfo) {
    console.error("[ErrorBoundary] Uncaught error:", error, errorInfo);
  }

  private handleRetry = () => {
    // 1. Call the parent's onRetry so it can refetch data / reset state.
    this.props.onRetry?.();
    // 2. Increment retryKey so children fully remount — not just re-render.
    this.setState((prev) => ({
      hasError: false,
      retryKey: prev.retryKey + 1,
    }));
  };

  public render() {
    if (this.state.hasError) {
      return (
        <div className="flex flex-col items-center justify-center p-6 bg-slate-900/50 rounded-xl border border-red-500/20 text-center min-h-[200px] w-full h-full">
          <AlertCircle className="w-10 h-10 text-red-500/80 mb-3" />
          <h2 className="text-sm font-bold text-slate-200 uppercase tracking-wider">
            {this.props.fallbackText || "Something went wrong"}
          </h2>
          <p className="text-xs text-slate-400 mt-2 mb-4">
            An unexpected error occurred in this panel.
          </p>
          <button
            onClick={this.handleRetry}
            className="px-3 py-1.5 bg-blue-600/20 text-blue-400 hover:bg-blue-600 hover:text-white rounded-md transition-colors border border-blue-500/50 text-xs font-bold uppercase tracking-widest flex items-center gap-2"
          >
            <RefreshCw className="w-3 h-3" />
            Retry
          </button>
        </div>
      );
    }

    // key changes on retry → forces a full unmount+remount of all children
    return (
      <React.Fragment key={this.state.retryKey}>
        {this.props.children}
      </React.Fragment>
    );
  }
}
