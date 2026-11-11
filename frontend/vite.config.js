import { defineConfig } from "vite";
import react from "@vitejs/plugin-react";

// پیکربندی Vite - در توسعه، درخواست‌های /api به بک‌اند FastAPI پروکسی می‌شوند
export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      "/api": {
        target: "http://localhost:8000",
        changeOrigin: true,
      },
    },
  },
});
