/**
 * pages/Login.jsx - صفحه ورود کاربر
 */
import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext.jsx";

export default function Login() {
  const { login } = useAuth();
  const navigate = useNavigate();
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const [loading, setLoading] = useState(false);

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    setLoading(true);
    try {
      await login(username, password);
      navigate("/");
    } catch (err) {
      setError(err.response?.data?.detail || "خطا در ورود به سیستم");
    } finally {
      setLoading(false);
    }
  }

  return (
    <div className="min-h-screen flex items-center justify-center bg-gradient-to-br from-brand-50 to-white" dir="rtl">
      <div className="card w-full max-w-sm">
        <div className="text-center mb-6">
          <h1 className="text-xl font-bold text-brand-700">سامانه مدیریت انبار امدادی</h1>
          <p className="text-sm text-gray-400 mt-1">برای ادامه وارد حساب کاربری خود شوید</p>
        </div>

        <form onSubmit={handleSubmit} className="space-y-4">
          <div>
            <label className="block text-sm font-medium text-gray-600 mb-1">نام کاربری</label>
            <input
              className="input-field"
              value={username}
              onChange={(e) => setUsername(e.target.value)}
              placeholder="مثلا admin"
              required
            />
          </div>
          <div>
            <label className="block text-sm font-medium text-gray-600 mb-1">رمز عبور</label>
            <input
              type="password"
              className="input-field"
              value={password}
              onChange={(e) => setPassword(e.target.value)}
              required
            />
          </div>

          {error && <div className="text-sm text-red-600 bg-red-50 rounded-lg p-2 text-center">{error}</div>}

          <button type="submit" disabled={loading} className="btn-primary w-full">
            {loading ? "در حال ورود..." : "ورود"}
          </button>
        </form>

        <p className="text-xs text-gray-400 text-center mt-4">
          کاربر پیش‌فرض: admin / Admin@12345 (بعد از seed اولیه)
        </p>
      </div>
    </div>
  );
}
