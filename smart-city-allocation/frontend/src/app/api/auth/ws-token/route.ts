import { NextRequest, NextResponse } from "next/server";
import { cookies } from "next/headers";

/**
 * GET /api/auth/ws-token
 *
 * Returns the current access_token so the browser can pass it as a query
 * parameter when opening the WebSocket connection. The token is HttpOnly and
 * cannot be read by JavaScript directly.
 *
 * This endpoint is intentionally lightweight — it does not validate the token,
 * it just forwards it to the client for use in the WS handshake URL.
 */
export async function GET(_req: NextRequest) {
  const cookieStore = await cookies();
  const token = cookieStore.get("access_token")?.value;

  if (!token) {
    return NextResponse.json({ error: "Not authenticated" }, { status: 401 });
  }

  return NextResponse.json({ token });
}
