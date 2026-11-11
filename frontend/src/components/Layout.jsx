/**
 * components/Layout.jsx
 * چیدمان کلی صفحات: منوی کناری + محتوای اصلی.
 */
import React from "react";
import Sidebar from "./Sidebar.jsx";

export default function Layout({ children }) {
  return (
    <div className="flex min-h-screen" dir="rtl">
      <Sidebar />
      <main className="flex-1 p-6 max-w-7xl mx-auto w-full">{children}</main>
    </div>
  );
}
