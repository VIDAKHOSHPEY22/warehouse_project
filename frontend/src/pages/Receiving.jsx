/**
 * pages/Receiving.jsx - فرم ثبت ورود کالا (Receiving)
 */
import React, { useEffect, useState } from "react";
import apiClient from "../api/client";

export default function Receiving() {
  const [items, setItems] = useState([]);
  const [locations, setLocations] = useState([]);
  const [form, setForm] = useState({
    item_id: "", location_id: "", quantity: 1, batch_no: "", expiry_date: "", source: "", note: "",
  });
  const [message, setMessage] = useState(null);

  useEffect(() => {
    apiClient.get("/items").then((res) => setItems(res.data));
    apiClient.get("/locations").then((res) => setLocations(res.data));
  }, []);

  async function handleSubmit(e) {
    e.preventDefault();
    setMessage(null);
    try {
      const payload = {
        ...form,
        item_id: Number(form.item_id),
        location_id: Number(form.location_id),
        quantity: Number(form.quantity),
        batch_no: form.batch_no || null,
        expiry_date: form.expiry_date || null,
        source: form.source || null,
        note: form.note || null,
      };
      await apiClient.post("/transactions/receive", payload);
      setMessage({ type: "success", text: "ورود کالا با موفقیت ثبت شد ✅" });
      setForm({ item_id: "", location_id: "", quantity: 1, batch_no: "", expiry_date: "", source: "", note: "" });
    } catch (err) {
      setMessage({ type: "error", text: err.response?.data?.detail || "خطا در ثبت ورود کالا" });
    }
  }

  return (
    <div className="max-w-2xl space-y-6">
      <h1 className="text-2xl font-bold text-gray-800">ثبت ورود کالا</h1>
      <form onSubmit={handleSubmit} className="card space-y-4">
        <Field label="کالا">
          <select className="input-field" required value={form.item_id} onChange={(e) => setForm({ ...form, item_id: e.target.value })}>
            <option value="">انتخاب کنید...</option>
            {items.map((i) => (
              <option key={i.id} value={i.id}>{i.name} ({i.code})</option>
            ))}
          </select>
        </Field>

        <Field label="مکان نگهداری">
          <select className="input-field" required value={form.location_id} onChange={(e) => setForm({ ...form, location_id: e.target.value })}>
            <option value="">انتخاب کنید...</option>
            {locations.map((l) => (
              <option key={l.id} value={l.id}>{l.code} - {l.name}</option>
            ))}
          </select>
        </Field>

        <Field label="تعداد">
          <input type="number" min="1" className="input-field" required value={form.quantity}
            onChange={(e) => setForm({ ...form, quantity: e.target.value })} />
        </Field>

        <div className="grid grid-cols-2 gap-4">
          <Field label="شماره بچ (اختیاری)">
            <input className="input-field" value={form.batch_no} onChange={(e) => setForm({ ...form, batch_no: e.target.value })} />
          </Field>
          <Field label="تاریخ انقضا (اختیاری)">
            <input type="date" className="input-field" value={form.expiry_date} onChange={(e) => setForm({ ...form, expiry_date: e.target.value })} />
          </Field>
        </div>

        <Field label="منبع تأمین (اهداکننده/تأمین‌کننده)">
          <input className="input-field" value={form.source} onChange={(e) => setForm({ ...form, source: e.target.value })} />
        </Field>

        <Field label="یادداشت">
          <textarea className="input-field" rows="2" value={form.note} onChange={(e) => setForm({ ...form, note: e.target.value })} />
        </Field>

        {message && (
          <div className={`text-sm rounded-lg p-2 ${message.type === "success" ? "bg-green-50 text-green-700" : "bg-red-50 text-red-700"}`}>
            {message.text}
          </div>
        )}

        <button type="submit" className="btn-primary w-full">ثبت ورود کالا</button>
      </form>
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
