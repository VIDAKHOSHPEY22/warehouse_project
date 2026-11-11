/**
 * pages/Dashboard.jsx
 * نمای کلی سامانه: تعداد کالاهای کم‌موجود، تعداد مأموریت‌های فعال،
 * و آخرین تراکنش‌ها. یک نقطه شروع سریع برای کاربر بعد از ورود.
 */
import React, { useEffect, useState } from "react";
import apiClient from "../api/client";
import DataTable from "../components/DataTable.jsx";

export default function Dashboard() {
  const [lowStock, setLowStock] = useState([]);
  const [recentTx, setRecentTx] = useState([]);
  const [missions, setMissions] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function load() {
      const [lowStockRes, txRes, missionsRes] = await Promise.all([
        apiClient.get("/reports/low-stock"),
        apiClient.get("/transactions", { params: { limit: 8 } }),
        apiClient.get("/missions"),
      ]);
      setLowStock(lowStockRes.data);
      setRecentTx(txRes.data);
      setMissions(missionsRes.data);
      setLoading(false);
    }
    load();
  }, []);

  const activeMissions = missions.filter((m) => !["delivered", "cancelled"].includes(m.status));

  if (loading) return <div className="text-gray-400">در حال بارگذاری...</div>;

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-800">داشبورد</h1>

      <div className="grid grid-cols-1 md:grid-cols-3 gap-4">
        <StatCard title="اقلام کم‌موجود" value={lowStock.length} color="text-red-600" />
        <StatCard title="مأموریت‌های فعال" value={activeMissions.length} color="text-brand-600" />
        <StatCard title="کل مأموریت‌ها" value={missions.length} color="text-gray-700" />
      </div>

      <div className="grid grid-cols-1 lg:grid-cols-2 gap-6">
        <div className="card">
          <h2 className="font-semibold mb-3">هشدار کمبود موجودی</h2>
          <DataTable
            columns={[
              { key: "item_name", label: "کالا" },
              { key: "total_available", label: "موجودی قابل تخصیص" },
              { key: "min_stock", label: "حداقل مجاز" },
            ]}
            rows={lowStock}
            emptyMessage="در حال حاضر هیچ کالایی کم‌موجود نیست 🎉"
          />
        </div>

        <div className="card">
          <h2 className="font-semibold mb-3">آخرین تراکنش‌ها</h2>
          <DataTable
            columns={[
              { key: "type", label: "نوع", render: (r) => txTypeLabel(r.type) },
              { key: "quantity", label: "تعداد" },
              { key: "created_at", label: "تاریخ", render: (r) => new Date(r.created_at).toLocaleString("fa-IR") },
            ]}
            rows={recentTx}
          />
        </div>
      </div>
    </div>
  );
}

function StatCard({ title, value, color }) {
  return (
    <div className="card">
      <div className="text-sm text-gray-400">{title}</div>
      <div className={`text-3xl font-bold mt-1 ${color}`}>{value}</div>
    </div>
  );
}

function txTypeLabel(type) {
  const map = {
    receipt: "ورود کالا",
    issue: "خروج کالا",
    transfer: "جابجایی",
    adjustment: "اصلاح موجودی",
    allocation: "تخصیص",
  };
  return map[type] || type;
}
