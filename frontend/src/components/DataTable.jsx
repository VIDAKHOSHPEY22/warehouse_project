/**
 * components/DataTable.jsx
 * جدول عمومی و قابل استفاده مجدد برای نمایش لیست‌ها.
 * columns: [{ key, label, render? }]
 */
import React from "react";

export default function DataTable({ columns, rows, emptyMessage = "داده‌ای برای نمایش وجود ندارد" }) {
  if (!rows || rows.length === 0) {
    return <div className="text-center text-gray-400 py-10">{emptyMessage}</div>;
  }

  return (
    <div className="overflow-x-auto">
      <table className="table-base">
        <thead>
          <tr>
            {columns.map((col) => (
              <th key={col.key}>{col.label}</th>
            ))}
          </tr>
        </thead>
        <tbody>
          {rows.map((row, idx) => (
            <tr key={row.id ?? idx} className="hover:bg-gray-50">
              {columns.map((col) => (
                <td key={col.key}>{col.render ? col.render(row) : row[col.key]}</td>
              ))}
            </tr>
          ))}
        </tbody>
      </table>
    </div>
  );
}
