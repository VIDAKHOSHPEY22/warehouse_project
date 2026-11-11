/**
 * components/Sidebar.jsx
 * منوی کناری اصلی اپلیکیشن. آیتم‌ها بر اساس نقش کاربر فیلتر می‌شوند
 * (مثلا "کاربران" فقط برای ادمین نمایش داده می‌شود).
 */
import React from "react";
import { NavLink } from "react-router-dom";
import { useAuth } from "../context/AuthContext.jsx";

const NAV_ITEMS = [
  { to: "/", label: "داشبورد", icon: "📊", roles: ["admin", "operator", "warehouse"] },
  { to: "/items", label: "اقلام", icon: "📦", roles: ["admin", "operator", "warehouse"] },
  { to: "/inventory", label: "موجودی انبار", icon: "🏬", roles: ["admin", "operator", "warehouse"] },
  { to: "/receiving", label: "ثبت ورود کالا", icon: "⬇️", roles: ["admin", "operator", "warehouse"] },
  { to: "/issue", label: "ثبت خروج کالا", icon: "⬆️", roles: ["admin", "operator", "warehouse"] },
  { to: "/missions", label: "مأموریت‌ها", icon: "🎯", roles: ["admin", "operator"] },
  { to: "/reports", label: "گزارش‌ها", icon: "📈", roles: ["admin", "operator", "warehouse"] },
  { to: "/users", label: "کاربران", icon: "👥", roles: ["admin"] },
];

export default function Sidebar() {
  const { user, logout } = useAuth();

  return (
    <aside className="w-64 bg-white border-l border-gray-200 h-screen sticky top-0 flex flex-col">
      <div className="p-4 border-b border-gray-100">
        <h1 className="text-lg font-bold text-brand-700">انبار امدادی</h1>
        <p className="text-xs text-gray-400 mt-1">سامانه مدیریت هوشمند انبار</p>
      </div>

      <nav className="flex-1 overflow-y-auto p-3 space-y-1">
        {NAV_ITEMS.filter((item) => item.roles.includes(user?.role)).map((item) => (
          <NavLink
            key={item.to}
            to={item.to}
            end={item.to === "/"}
            className={({ isActive }) =>
              `flex items-center gap-2 px-3 py-2 rounded-lg text-sm font-medium transition ${
                isActive ? "bg-brand-50 text-brand-700" : "text-gray-600 hover:bg-gray-50"
              }`
            }
          >
            <span>{item.icon}</span>
            <span>{item.label}</span>
          </NavLink>
        ))}
      </nav>

      <div className="p-3 border-t border-gray-100">
        <div className="text-sm text-gray-700 mb-2">{user?.full_name}</div>
        <div className="text-xs text-gray-400 mb-3">نقش: {roleLabel(user?.role)}</div>
        <button onClick={logout} className="btn-secondary w-full text-sm">
          خروج از حساب
        </button>
      </div>
    </aside>
  );
}

function roleLabel(role) {
  const map = { admin: "مدیر سیستم", operator: "کارشناس عملیات", warehouse: "انباردار" };
  return map[role] || role;
}
