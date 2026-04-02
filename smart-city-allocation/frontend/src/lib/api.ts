import axios from "axios";

const api = axios.create({
  baseURL: "/api/bff",
  withCredentials: true,
  headers: { "Content-Type": "application/json" },
});

api.interceptors.response.use(
  (r) => r,
  (err) => {
    if (typeof window !== "undefined" && err.response?.status === 401) {
      const p = window.location.pathname;
      if (!p.startsWith("/login")) window.location.href = "/login";
    }
    return Promise.reject(err);
  }
);

export default api;
