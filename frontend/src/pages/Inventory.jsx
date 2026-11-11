/**
 * pages/Inventory.jsx - نمایش موجودی بچ‌ها به تفکیک مکان و کالا
 */
import React, { useEffect, useState } from "react";
import apiClient from "../api/client";
import DataTable from "../components/DataTable.jsx";

export default function Inventory() {
  const [batches, setBatches] = useState([]);

  useEffect(() => {
    apiClient.get("/batches").then((res) => setBatches(res.data));
  }, []);

  return (
    <div className="space-y-6">
      <h1 className="text-2xl font-bold text-gray-800">موجودی انبار (بچ‌ها)</h1>
      <div className="card">
        <DataTable
          columns={[
            { key: "item", label: "کالا", render: (r) => r.item?.name },
            { key: "location", label: "مکان", render: (r) => `${r.location?.code} - ${r.location?.name}` },
            { key: "batch_no", label: "شماره بچ", render: (r) => r.batch_no || "-" },
            { key: "expiry_date", label: "تاریخ انقضا", render: (r) => r.expiry_date || "-" },
            { key: "quantity_on_hand", label: "موجودی فیزیکی" },
            { key: "quantity_allocated", label: "تخصیص‌یافته" },
            { key: "quantity_available", label: "قابل تخصیص" },
          ]}
          rows={batches}
        />
      </div>
    </div>
  );
}
