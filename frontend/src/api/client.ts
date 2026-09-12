import axios from "axios";

export const API_BASE_URL =
  import.meta.env.VITE_API_BASE_URL ?? "http://localhost:8000/api/v1";

export const api = axios.create({
  baseURL: API_BASE_URL,
  headers: { "Content-Type": "application/json" },
});

api.interceptors.request.use((config) => {
  const token = localStorage.getItem("ibam.access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

api.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("ibam.access_token");
      window.location.assign("/login");
    }
    return Promise.reject(error);
  },
);

export interface DashboardSummary {
  total_workflows: number;
  active_automations: number;
  tasks_completed_today: number;
  success_rate_pct: number;
  pending_approvals: number;
}

export async function fetchDashboardSummary(): Promise<DashboardSummary> {
  const { data } = await api.get<DashboardSummary>("/dashboard/summary");
  return data;
}

export async function login(
  username: string,
  password: string,
): Promise<string> {
  const form = new URLSearchParams({ username, password });
  const { data } = await axios.post<{ access_token: string }>(
    `${API_BASE_URL}/auth/login`,
    form,
    { headers: { "Content-Type": "application/x-www-form-urlencoded" } },
  );
  localStorage.setItem("ibam.access_token", data.access_token);
  return data.access_token;
}