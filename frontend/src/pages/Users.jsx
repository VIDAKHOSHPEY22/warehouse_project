/**
 * pages/Users.jsx - مدیریت کاربران (فقط قابل مشاهده برای ادمین)
 */
import React, { useEffect, useState } from "react";
import apiClient from "../api/client";
import DataTable from "../components/DataTable.jsx";

const EMPTY_FORM = { username: "", full_name: "", password: "", role: "warehouse" };
const ROLE_LABELS = { admin: "مدیر سیستم", operator: "کارشناس عملیات", warehouse: "انباردار" };

export default function Users() {
  const [users, setUsers] = useState([]);
  const [form, setForm] = useState(EMPTY_FORM);
  const [showForm, setShowForm] = useState(false);
  const [error, setError] = useState("");

  async function load() {
    const { data } = await apiClient.get("/users");
    setUsers(data);
  }

  useEffect(() => {
    load();
  }, []);

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    try {
      await apiClient.post("/users", form);
      setForm(EMPTY_FORM);
      setShowForm(false);
      load();
    } catch (err) {
      setError(err.response?.data?.detail || "خطا در ثبت کاربر");
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-800">مدیریت کاربران</h1>
        <button className="btn-primary" onClick={() => setShowForm((s) => !s)}>
          {showForm ? "بستن فرم" : "+ کاربر جدید"}
        </button>
      </div>

      {showForm && (
        <form onSubmit={handleSubmit} className="card grid grid-cols-1 md:grid-cols-2 gap-4">
          <Field label="نام کاربری">
            <input className="input-field" required value={form.username} onChange={(e) => setForm({ ...form, username: e.target.value })} />
          </Field>
          <Field label="نام کامل">
            <input className="input-field" required value={form.full_name} onChange={(e) => setForm({ ...form, full_name: e.target.value })} />
          </Field>
          <Field label="رمز عبور">
            <input type="password" className="input-field" required value={form.password} onChange={(e) => setForm({ ...form, password: e.target.value })} />
          </Field>
          <Field label="نقش">
            <select className="input-field" value={form.role} onChange={(e) => setForm({ ...form, role: e.target.value })}>
              <option value="warehouse">انباردار</option>
              <option value="operator">کارشناس عملیات</option>
              <option value="admin">مدیر سیستم</option>
            </select>
          </Field>
          {error && <div className="md:col-span-2 text-sm text-red-600">{error}</div>}
          <div className="md:col-span-2">
            <button type="submit" className="btn-primary">ثبت کاربر</button>
          </div>
        </form>
      )}

      <div className="card">
        <DataTable
          columns={[
            { key: "username", label: "نام کاربری" },
            { key: "full_name", label: "نام کامل" },
            { key: "role", label: "نقش", render: (r) => ROLE_LABELS[r.role] },
            { key: "is_active", label: "وضعیت", render: (r) => (r.is_active ? "فعال" : "غیرفعال") },
          ]}
          rows={users}
        />
      </div>
    </div>
  );
}

function Field({ label, children }) {
  return (
    <div>
      <label className="block text-sm font-medium text-gray-600 mb-1">{label}</label>
      {children}
    </div>
  );
}
