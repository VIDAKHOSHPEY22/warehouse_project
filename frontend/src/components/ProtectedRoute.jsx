/**
 * components/ProtectedRoute.jsx
 * یک Route Guard ساده: اگر کاربر لاگین نکرده باشد به /login هدایت
 * می‌شود. اگر allowedRoles داده شود و نقش کاربر در آن نباشد،
 * پیام عدم دسترسی نمایش داده می‌شود.
 */
import React from "react";
import { Navigate } from "react-router-dom";
import { useAuth } from "../context/AuthContext.jsx";

export default function ProtectedRoute({ children, allowedRoles }) {
  const { user, isAuthenticated } = useAuth();

  if (!isAuthenticated) {
    return <Navigate to="/login" replace />;
  }

  if (allowedRoles && !allowedRoles.includes(user.role)) {
    return (
      <div className="p-8 text-center text-red-600">
        شما دسترسی لازم برای مشاهده این صفحه را ندارید.
      </div>
    );
  }

  return children;
}
