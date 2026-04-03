import axios, { AxiosRequestConfig } from "axios";

// Extend config to track retry state so we never loop
interface _Config extends AxiosRequestConfig {
  _retried?: boolean;
}

const api = axios.create({
  baseURL: "/api/bff",
  withCredentials: true,
  headers: { "Content-Type": "application/json" },
});

/**
 * Keeps a single in-flight refresh promise so that when multiple requests
 * 401 simultaneously they all await the same refresh call instead of each
 * firing their own.
 */
let _refreshPromise: Promise<boolean> | null = null;

async function refreshAccessToken(): Promise<boolean> {
  try {
    const res = await fetch("/api/auth/refresh", {
      method: "POST",
      credentials: "include",
    });
    return res.ok;
  } catch {
    return false;
  }
}

api.interceptors.response.use(
  (response) => response,
  async (error) => {
    const config = error.config as _Config | undefined;

    // Only attempt to refresh on 401s from our own BFF that haven't been
    // retried yet. Never try to refresh the refresh endpoint itself.
    if (
      error.response?.status === 401 &&
      config &&
      !config._retried &&
      !config.url?.includes("/auth/")
    ) {
      config._retried = true;

      // Deduplicate: share one refresh promise across concurrent failures
      if (!_refreshPromise) {
        _refreshPromise = refreshAccessToken().finally(() => {
          _refreshPromise = null;
        });
      }

      const refreshed = await _refreshPromise;

      if (refreshed) {
        // New access_token cookie is now set — retry the original request
        return api.request(config);
      }

      // Refresh failed — send user to login page
      if (typeof window !== "undefined") {
        window.location.href = "/login";
      }
    }

    return Promise.reject(error);
  }
);

export default api;
