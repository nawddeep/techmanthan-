import { NextRequest, NextResponse } from "next/server";
import { cookies } from "next/headers";

const BACKEND =
  process.env.INTERNAL_API_URL ||
  process.env.NEXT_PUBLIC_API_URL ||
  "http://127.0.0.1:8000";

async function proxy(
  req: NextRequest,
  context: { params: Promise<{ path: string[] }> }
) {
  const { path } = await context.params;
  const subpath = path.join("/");
  const url = `${BACKEND.replace(/\/$/, "")}/${subpath}${req.nextUrl.search}`;
  const token = (await cookies()).get("access_token")?.value;
  const headers: Record<string, string> = {};
  if (token) headers["Authorization"] = `Bearer ${token}`;
  const ct = req.headers.get("content-type");
  if (ct) headers["Content-Type"] = ct;

  const init: RequestInit = {
    method: req.method,
    headers,
    cache: "no-store",
  };
  if (!["GET", "HEAD"].includes(req.method)) {
    init.body = await req.arrayBuffer();
  }

  const res = await fetch(url, init);
  const body = await res.arrayBuffer();
  const out = new NextResponse(body, { status: res.status });
  const contentType = res.headers.get("content-type");
  if (contentType) out.headers.set("content-type", contentType);
  return out;
}

export const GET = proxy;
export const POST = proxy;
export const PUT = proxy;
export const DELETE = proxy;
export const PATCH = proxy;
