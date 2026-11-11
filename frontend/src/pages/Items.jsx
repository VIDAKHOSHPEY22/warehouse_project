/**
 * pages/Items.jsx - مدیریت شناسنامه کالا (لیست + فرم افزودن)
 */
import React, { useEffect, useState } from "react";
import apiClient from "../api/client";
import DataTable from "../components/DataTable.jsx";
import { useAuth } from "../context/AuthContext.jsx";

const EMPTY_FORM = { code: "", name: "", category: "", unit: "عدد", expiry_required: false, min_stock: 0 };

export default function Items() {
  const { user } = useAuth();
  const canEdit = user.role === "admin" || user.role === "operator";
  const [items, setItems] = useState([]);
  const [form, setForm] = useState(EMPTY_FORM);
  const [showForm, setShowForm] = useState(false);
  const [error, setError] = useState("");

  async function load() {
    const { data } = await apiClient.get("/items");
    setItems(data);
  }

  useEffect(() => {
    load();
  }, []);

  async function handleSubmit(e) {
    e.preventDefault();
    setError("");
    try {
      await apiClient.post("/items", form);
      setForm(EMPTY_FORM);
      setShowForm(false);
      load();
    } catch (err) {
      setError(err.response?.data?.detail || "خطا در ثبت کالا");
    }
  }

  return (
    <div className="space-y-6">
      <div className="flex items-center justify-between">
        <h1 className="text-2xl font-bold text-gray-800">اقلام (SKU)</h1>
        {canEdit && (
          <button className="btn-primary" onClick={() => setShowForm((s) => !s)}>
            {showForm ? "بستن فرم" : "+ افزودن کالای جدید"}
          </button>
        )}
      </div>

      {showForm && (
        <form onSubmit={handleSubmit} className="card grid grid-cols-1 md:grid-cols-3 gap-4">
          <Field label="کد کالا">
            <input className="input-field" required value={form.code} onChange={(e) => setForm({ ...form, code: e.target.value })} />
          </Field>
          <Field label="نام کالا">
            <input className="input-field" required value={form.name} onChange={(e) => setForm({ ...form, name: e.target.value })} />
          </Field>
          <Field label="دسته‌بندی">
            <input className="input-field" value={form.category} onChange={(e) => setForm({ ...form, category: e.target.value })} />
          </Field>
          <Field label="واحد شمارش">
            <input className="input-field" value={form.unit} onChange={(e) => setForm({ ...form, unit: e.target.value })} />
          </Field>
          <Field label="حداقل موجودی هشدار">
            <input
              type="number"
              className="input-field"
              value={form.min_stock}
              onChange={(e) => setForm({ ...form, min_stock: Number(e.target.value) })}
            />
          </Field>
          <Field label="نیاز به تاریخ انقضا">
            <select
              className="input-field"
              value={form.expiry_required ? "yes" : "no"}
              onChange={(e) => setForm({ ...form, expiry_required: e.target.value === "yes" })}
            >
              <option value="no">خیر</option>
              <option value="yes">بله</option>
            </select>
          </Field>

          {error && <div className="md:col-span-3 text-sm text-red-600">{error}</div>}
          <div className="md:col-span-3">
            <button type="submit" className="btn-primary">
              ثبت کالا
            </button>
          </div>
        </form>
      )}

      <div className="card">
        <DataTable
          columns={[
            { key: "code", label: "کد" },
            { key: "name", label: "نام کالا" },
            { key: "category", label: "دسته" },
            { key: "unit", label: "واحد" },
            { key: "total_on_hand", label: "موجودی فیزیکی" },
            { key: "total_available", label: "موجودی قابل تخصیص" },
            { key: "min_stock", label: "حداقل مجاز" },
          ]}
          rows={items}
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
