"use client";

import { useState } from "react";
import { useRouter } from "next/navigation";
import Link from "next/link";

export default function LoginPage() {
  const router = useRouter();
  const [username, setUsername] = useState("admin");
  const [password, setPassword] = useState("admin123");
  const [err, setErr] = useState("");

  const submit = async (e: React.FormEvent) => {
    e.preventDefault();
    setErr("");
    const res = await fetch("/api/auth/login", {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ username, password }),
      credentials: "include",
    });
    if (!res.ok) {
      const j = await res.json().catch(() => ({}));
      setErr(j.detail || "Login failed");
      return;
    }
    router.push("/");
  };

  return (
    <div className="min-h-screen flex items-center justify-center bg-slate-950 p-6">
      <form
        onSubmit={submit}
        className="w-full max-w-md bg-slate-900/80 border border-slate-700 rounded-2xl p-8 shadow-xl"
      >
        <h1 className="text-xl font-bold text-slate-100 mb-6">Smart City Login</h1>
        <label className="block text-sm text-slate-400 mb-1">Username</label>
        <input
          className="w-full mb-4 bg-slate-800 border border-slate-600 rounded-lg px-3 py-2 text-slate-100"
          value={username}
          onChange={(e) => setUsername(e.target.value)}
          autoComplete="username"
        />
        <label className="block text-sm text-slate-400 mb-1">Password</label>
        <input
          type="password"
          className="w-full mb-6 bg-slate-800 border border-slate-600 rounded-lg px-3 py-2 text-slate-100"
          value={password}
          onChange={(e) => setPassword(e.target.value)}
          autoComplete="current-password"
        />
        {err && <p className="text-red-400 text-sm mb-4">{err}</p>}
        <button
          type="submit"
          className="w-full py-2.5 rounded-lg bg-blue-600 hover:bg-blue-500 text-white font-semibold"
        >
          Sign in
        </button>
        <p className="text-xs text-slate-500 mt-4 text-center">
          Demo: admin / admin123 or viewer / viewer123
        </p>
        <p className="text-center mt-2">
          <Link href="/" className="text-blue-400 text-sm hover:underline">
            Back to dashboard
          </Link>
        </p>
      </form>
    </div>
  );
}
