import { NextRequest, NextResponse } from "next/server";

const BACKEND =
  process.env.INTERNAL_API_URL ||
  process.env.NEXT_PUBLIC_API_URL ||
  "http://127.0.0.1:8000";

export async function POST(req: NextRequest) {
  const contentType = req.headers.get("content-type") || "";
  let body: BodyInit;
  if (contentType.includes("application/json")) {
    const j = await req.json();
    const fd = new FormData();
    fd.set("username", j.username);
    fd.set("password", j.password);
    body = fd;
  } else {
    body = await req.formData();
  }

  const res = await fetch(`${BACKEND.replace(/\/$/, "")}/auth/token`, {
    method: "POST",
    body,
  });
  const data = await res.json();
  if (!res.ok) {
    return NextResponse.json(data, { status: res.status });
  }

  const r = NextResponse.json({ ok: true, role: data.token_type });
  r.cookies.set("access_token", data.access_token, {
    httpOnly: true,
    path: "/",
    sameSite: "lax",
    maxAge: 60 * 60,
  });
  if (data.refresh_token) {
    r.cookies.set("refresh_token", data.refresh_token, {
      httpOnly: true,
      path: "/",
      sameSite: "lax",
      maxAge: 60 * 60 * 24 * 7,
    });
  }
  return r;
}
