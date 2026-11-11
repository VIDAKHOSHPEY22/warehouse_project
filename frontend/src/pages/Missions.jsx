/**
 * pages/Missions.jsx - مدیریت مأموریت‌ها/درخواست‌های توزیع
 */
import React, { useEffect, useState } from "react";
import apiClient from "../api/client";
import DataTable from "../components/DataTable.jsx";

const EMPTY_FORM = { code: "", title: "", requester: "", destination: "", note: "" };
const STATUS_LABELS = {
  draft: "پیش‌نویس",
  allocated: "تخصیص‌یافته",
  partially_delivered: "تحویل جزئی",
  delivered: "تحویل شده",
  cancelled: "لغو شده",
};

export default function Missions() {
  const [missions, setMissions] = useState([]);
  const [form, setForm] = useState(EMPTY_FORM);
  const [showForm, setShowForm] = useState(false);
  const [error, setError] = useState("");

  async function load() {
    const { data } = await apiClient.get("/missions");
    setMissions(data);
  }

  useEffect(() => {
    load();
  }, []);

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    try {
      await apiClient.post("/missions", form);
      setForm(EMPTY_FORM);
      setShowForm(false);
      load();
    } catch (err) {
      setError(err.response?.data?.detail || "خطا در ثبت مأموریت");
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-800">مأموریت‌ها / درخواست‌های توزیع</h1>
        <button className="btn-primary" onClick={() => setShowForm((s) => !s)}>
          {showForm ? "بستن فرم" : "+ مأموریت جدید"}
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleSubmit} className="card grid grid-cols-1 md:grid-cols-2 gap-4">
          <Field label="کد مأموریت">
            <input className="input-field" required value={form.code} onChange={(e) => setForm({ ...form, code: e.target.value })} />
          </Field>
          <Field label="عنوان">
            <input className="input-field" required value={form.title} onChange={(e) => setForm({ ...form, title: e.target.value })} />
          </Field>
          <Field label="درخواست‌کننده">
            <input className="input-field" value={form.requester} onChange={(e) => setForm({ ...form, requester: e.target.value })} />
          </Field>
          <Field label="مقصد">
            <input className="input-field" value={form.destination} onChange={(e) => setForm({ ...form, destination: e.target.value })} />
          </Field>
          <div className="md:col-span-2">
            <Field label="یادداشت">
              <textarea className="input-field" rows="2" value={form.note} onChange={(e) => setForm({ ...form, note: e.target.value })} />
            </Field>
          </div>
          {error && <div className="md:col-span-2 text-sm text-red-600">{error}</div>}
          <div className="md:col-span-2">
            <button type="submit" className="btn-primary">ثبت مأموریت</button>
          </div>
        </form>
      )}

      <div className="card">
        <DataTable
          columns={[
            { key: "code", label: "کد" },
            { key: "title", label: "عنوان" },
            { key: "requester", label: "درخواست‌کننده" },
            { key: "destination", label: "مقصد" },
            { key: "status", label: "وضعیت", render: (r) => <StatusBadge status={r.status} /> },
          ]}
          rows={missions}
        />
      </div>
    </div>
  );
}

function StatusBadge({ status }) {
  const colors = {
    draft: "bg-gray-100 text-gray-600",
    allocated: "bg-blue-100 text-blue-700",
    partially_delivered: "bg-yellow-100 text-yellow-700",
    delivered: "bg-green-100 text-green-700",
    cancelled: "bg-red-100 text-red-700",
  };
  return <span className={`px-2 py-1 rounded-full text-xs font-medium ${colors[status]}`}>{STATUS_LABELS[status]}</span>;
}

function Field({ label, children }) {
  return (
    <div>
      <label className="block text-sm font-medium text-gray-600 mb-1">{label}</label>
      {children}
    </div>
  );
}
