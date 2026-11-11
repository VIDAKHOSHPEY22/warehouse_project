/**
 * context/AuthContext.jsx
 * ----------------------------------------------------------------
 * مدیریت وضعیت سراسری احراز هویت با استفاده از React Context.
 * توکن و اطلاعات کاربر در localStorage نگهداری می‌شود تا با رفرش
 * صفحه از بین نرود.
 * ----------------------------------------------------------------
 */
import React, { createContext, useContext, useState, useCallback } from "react";
import apiClient from "../api/client";

const AuthContext = createContext(null);

export function AuthProvider({ children }) {
  const [user, setUser] = useState(() => {
    const stored = localStorage.getItem("user");
    return stored ? JSON.parse(stored) : null;
  });

  const login = useCallback(async (username, password) => {
    // بک‌اند از فرمت form-data استاندارد OAuth2 استفاده می‌کند
    const form = new URLSearchParams();
    form.append("username", username);
    form.append("password", password);

    const { data } = await apiClient.post("/auth/login", form, {
      headers: { "Content-Type": "application/x-www-form-urlencoded" },
    });
    localStorage.setItem("access_token", data.access_token);

    const meResponse = await apiClient.get("/auth/me");
    localStorage.setItem("user", JSON.stringify(meResponse.data));
    setUser(meResponse.data);
    return meResponse.data;
  }, []);

  const logout = useCallback(() => {
    localStorage.removeItem("access_token");
    localStorage.removeItem("user");
    setUser(null);
  }, []);

  return (
    <AuthContext.Provider value={{ user, login, logout, isAuthenticated: !!user }}>
      {children}
    </AuthContext.Provider>
  );
}

export function useAuth() {
  const ctx = useContext(AuthContext);
  if (!ctx) throw new Error("useAuth باید داخل AuthProvider استفاده شود");
  return ctx;
}
