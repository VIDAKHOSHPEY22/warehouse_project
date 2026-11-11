/**
 * api/client.js
 * ----------------------------------------------------------------
 * یک نمونه Axios متمرکز برای همه فراخوانی‌های API.
 *   - baseURL از متغیر محیطی VITE_API_BASE_URL خوانده می‌شود
 *   - Interceptor درخواست: توکن JWT را از localStorage خوانده و به
 *     هدر Authorization اضافه می‌کند
 *   - Interceptor پاسخ: اگر 401 برگردد (توکن منقضی)، کاربر را به
 *     صفحه ورود هدایت می‌کند
 * ----------------------------------------------------------------
 */
import axios from "axios";

const apiClient = axios.create({
  baseURL: import.meta.env.VITE_API_BASE_URL || "/api",
});

apiClient.interceptors.request.use((config) => {
  const token = localStorage.getItem("access_token");
  if (token) {
    config.headers.Authorization = `Bearer ${token}`;
  }
  return config;
});

apiClient.interceptors.response.use(
  (response) => response,
  (error) => {
    if (error.response?.status === 401) {
      localStorage.removeItem("access_token");
      localStorage.removeItem("user");
      window.location.href = "/login";
    }
    return Promise.reject(error);
  }
);

export default apiClient;
