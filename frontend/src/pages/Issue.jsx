/**
 * pages/Issue.jsx - فرم ثبت خروج نهایی کالا (Issue / تحویل به گیرنده)
 */
import React, { useEffect, useState } from "react";
import apiClient from "../api/client";

export default function Issue() {
  const [batches, setBatches] = useState([]);
  const [missions, setMissions] = useState([]);
  const [form, setForm] = useState({ batch_id: "", quantity: 1, mission_id: "", recipient: "", destination: "", note: "" });
  const [message, setMessage] = useState(null);

  useEffect(() => {
    apiClient.get("/batches", { params: { only_available: false } }).then((res) => setBatches(res.data));
    apiClient.get("/missions").then((res) => setMissions(res.data));
  }, []);

  async function handleSubmit(e) {
    e.preventDefault();
    setMessage(null);
    try {
      const payload = {
        batch_id: Number(form.batch_id),
        quantity: Number(form.quantity),
        mission_id: form.mission_id ? Number(form.mission_id) : null,
        recipient: form.recipient || null,
        destination: form.destination || null,
        note: form.note || null,
      };
      await apiClient.post("/transactions/issue", payload);
      setMessage({ type: "success", text: "خروج کالا با موفقیت ثبت شد ✅" });
      setForm({ batch_id: "", quantity: 1, mission_id: "", recipient: "", destination: "", note: "" });
    } catch (err) {
      setMessage({ type: "error", text: err.response?.data?.detail || "خطا در ثبت خروج کالا" });
    }
  }

  return (
    <div className="max-w-2xl space-y-6">
      <h1 className="text-2xl font-bold text-gray-800">ثبت خروج کالا (تحویل)</h1>
      <form onSubmit={handleSubmit} className="card space-y-4">
        <Field label="بچ موجودی">
          <select className="input-field" required value={form.batch_id} onChange={(e) => setForm({ ...form, batch_id: e.target.value })}>
            <option value="">انتخاب کنید...</option>
            {batches.map((b) => (
              <option key={b.id} value={b.id}>
                {b.item?.name} | {b.location?.code} | موجودی: {b.quantity_on_hand}
              </option>
            ))}
          </select>
        </Field>

        <Field label="تعداد">
          <input type="number" min="1" className="input-field" required value={form.quantity}
            onChange={(e) => setForm({ ...form, quantity: e.target.value })} />
        </Field>

        <Field label="مأموریت مرتبط (اختیاری)">
          <select className="input-field" value={form.mission_id} onChange={(e) => setForm({ ...form, mission_id: e.target.value })}>
            <option value="">بدون مأموریت</option>
            {missions.map((m) => (
              <option key={m.id} value={m.id}>{m.code} - {m.title}</option>
            ))}
          </select>
        </Field>

        <div className="grid grid-cols-2 gap-4">
          <Field label="گیرنده">
            <input className="input-field" value={form.recipient} onChange={(e) => setForm({ ...form, recipient: e.target.value })} />
          </Field>
          <Field label="مقصد">
            <input className="input-field" value={form.destination} onChange={(e) => setForm({ ...form, destination: e.target.value })} />
          </Field>
        </div>

        <Field label="یادداشت">
          <textarea className="input-field" rows="2" value={form.note} onChange={(e) => setForm({ ...form, note: e.target.value })} />
        </Field>

        {message && (
          <div className={`text-sm rounded-lg p-2 ${message.type === "success" ? "bg-green-50 text-green-700" : "bg-red-50 text-red-700"}`}>
            {message.text}
          </div>
        )}

        <button type="submit" className="btn-primary w-full">ثبت خروج کالا</button>
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
