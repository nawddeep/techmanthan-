import { NextRequest, NextResponse } from "next/server";
import { cookies } from "next/headers";

const BACKEND =
  process.env.INTERNAL_API_URL ||
  process.env.NEXT_PUBLIC_API_URL ||
  "http://127.0.0.1:8000";

/**
 * POST /api/auth/refresh
 *
 * Reads the refresh_token from the HttpOnly cookie, exchanges it for a new
 * access_token from the FastAPI backend, and sets the updated access_token
 * cookie. The Axios interceptor in api.ts calls this endpoint when it receives
 * a 401 before redirecting the user to the login page.
 */
export async function POST(_req: NextRequest) {
  const cookieStore = await cookies();
  const refreshToken = cookieStore.get("refresh_token")?.value;

  if (!refreshToken) {
    return NextResponse.json(
      { error: "No refresh token found" },
      { status: 401 }
    );
  }

  let backendRes: Response;
  try {
    backendRes = await fetch(`${BACKEND.replace(/\/$/, "")}/auth/refresh`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify({ refresh_token: refreshToken }),
    });
  } catch {
    return NextResponse.json(
      { error: "Backend unavailable during token refresh" },
      { status: 503 }
    );
  }

  if (!backendRes.ok) {
    // Refresh token is invalid or expired — clear cookies and force re-login.
    const out = NextResponse.json(
      { error: "Refresh token invalid or expired" },
      { status: 401 }
    );
    out.cookies.set("access_token", "", { maxAge: 0, path: "/" });
    out.cookies.set("refresh_token", "", { maxAge: 0, path: "/" });
    return out;
  }

  const data = await backendRes.json();

  const r = NextResponse.json({ ok: true });

  // Update access_token cookie (30-minute expiry matches backend)
  r.cookies.set("access_token", data.access_token, {
    httpOnly: true,
    path: "/",
    sameSite: "lax",
    maxAge: 60 * 30,
  });

  // Rotate the refresh token if backend issued a new one
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
