import axios from "axios";

const api = axios.create({
  baseURL: "/api/bff",
  withCredentials: true,
  headers: { "Content-Type": "application/json" },
});

api.interceptors.response.use(
  (r) => r,
  (err) => {
    // No authentication redirect - open access
    return Promise.reject(err);
  }
);

export default api;
