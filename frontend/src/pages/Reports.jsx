/**
 * pages/Reports.jsx - گزارش‌های کلیدی سامانه (تب‌بندی‌شده)
 */
import React, { useEffect, useState } from "react";
import apiClient from "../api/client";
import DataTable from "../components/DataTable.jsx";

const TABS = [
  { key: "current-stock", label: "موجودی لحظه‌ای" },
  { key: "low-stock", label: "کم‌موجودی" },
  { key: "expiring-batches", label: "نزدیک انقضا" },
  { key: "turnover", label: "گردش کالا" },
];

export default function Reports() {
  const [activeTab, setActiveTab] = useState("current-stock");
  const [rows, setRows] = useState([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    setLoading(true);
    apiClient.get(`/reports/${activeTab}`).then((res) => {
      setRows(res.data);
      setLoading(false);
    });
  }, [activeTab]);

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-800">گزارش‌ها</h1>

      <div className="flex gap-2 border-b border-gray-200">
        {TABS.map((tab) => (
          <button
            key={tab.key}
            onClick={() => setActiveTab(tab.key)}
            className={`px-4 py-2 text-sm font-medium border-b-2 transition ${
              activeTab === tab.key ? "border-brand-600 text-brand-700" : "border-transparent text-gray-500 hover:text-gray-700"
            }`}
          >
            {tab.label}
          </button>
        ))}
      </div>

      <div className="card">
        {loading ? <div className="text-gray-400">در حال بارگذاری...</div> : <ReportTable tab={activeTab} rows={rows} />}
      </div>
    </div>
  );
}

function ReportTable({ tab, rows }) {
  if (tab === "current-stock") {
    return (
      <DataTable
        rows={rows}
        columns={[
          { key: "item_code", label: "کد" },
          { key: "item_name", label: "کالا" },
          { key: "total_on_hand", label: "موجودی فیزیکی" },
          { key: "total_allocated", label: "تخصیص‌یافته" },
          { key: "total_available", label: "قابل تخصیص" },
          { key: "min_stock", label: "حداقل مجاز" },
          { key: "is_low_stock", label: "وضعیت", render: (r) => (r.is_low_stock ? "⚠️ کم‌موجود" : "✅ نرمال") },
        ]}
      />
    );
  }
  if (tab === "low-stock") {
    return (
      <DataTable
        rows={rows}
        columns={[
          { key: "item_code", label: "کد" },
          { key: "item_name", label: "کالا" },
          { key: "total_available", label: "موجودی قابل تخصیص" },
          { key: "min_stock", label: "حداقل مجاز" },
        ]}
        emptyMessage="هیچ کالایی کم‌موجود نیست 🎉"
      />
    );
  }
  if (tab === "expiring-batches") {
    return (
      <DataTable
        rows={rows}
        columns={[
          { key: "item_name", label: "کالا" },
          { key: "location_name", label: "مکان" },
          { key: "batch_no", label: "شماره بچ" },
          { key: "expiry_date", label: "تاریخ انقضا" },
          { key: "quantity_on_hand", label: "موجودی" },
        ]}
        emptyMessage="بچی نزدیک به انقضا نیست 🎉"
      />
    );
  }
  // turnover
  return (
    <DataTable
      rows={rows}
      columns={[
        { key: "item_name", label: "کالا" },
        { key: "total_received", label: "جمع ورودی" },
        { key: "total_issued", label: "جمع خروجی" },
      ]}
    />
  );
}
