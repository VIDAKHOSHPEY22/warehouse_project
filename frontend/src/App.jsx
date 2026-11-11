/**
 * App.jsx - تعریف مسیرهای (Routes) اصلی اپلیکیشن
 */
import React from "react";
import { Routes, Route } from "react-router-dom";

import Layout from "./components/Layout.jsx";
import ProtectedRoute from "./components/ProtectedRoute.jsx";

import Login from "./pages/Login.jsx";
import Dashboard from "./pages/Dashboard.jsx";
import Items from "./pages/Items.jsx";
import Inventory from "./pages/Inventory.jsx";
import Receiving from "./pages/Receiving.jsx";
import Issue from "./pages/Issue.jsx";
import Missions from "./pages/Missions.jsx";
import Reports from "./pages/Reports.jsx";
import Users from "./pages/Users.jsx";

export default function App() {
  return (
    <Routes>
      <Route path="/login" element={<Login />} />

      <Route path="/" element={<ProtectedRoute><Layout><Dashboard /></Layout></ProtectedRoute>} />
      <Route path="/items" element={<ProtectedRoute><Layout><Items /></Layout></ProtectedRoute>} />
      <Route path="/inventory" element={<ProtectedRoute><Layout><Inventory /></Layout></ProtectedRoute>} />
      <Route path="/receiving" element={<ProtectedRoute><Layout><Receiving /></Layout></ProtectedRoute>} />
      <Route path="/issue" element={<ProtectedRoute><Layout><Issue /></Layout></ProtectedRoute>} />
      <Route
        path="/missions"
        element={<ProtectedRoute allowedRoles={["admin", "operator"]}><Layout><Missions /></Layout></ProtectedRoute>}
      />
      <Route path="/reports" element={<ProtectedRoute><Layout><Reports /></Layout></ProtectedRoute>} />
      <Route
        path="/users"
        element={<ProtectedRoute allowedRoles={["admin"]}><Layout><Users /></Layout></ProtectedRoute>}
      />
    </Routes>
  );
}
