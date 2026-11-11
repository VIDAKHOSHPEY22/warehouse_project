/** @type {import('tailwindcss').Config} */
export default {
  content: ["./index.html", "./src/**/*.{js,jsx}"],
  theme: {
    extend: {
      colors: {
        // پالت رنگی برند سامانه - آبی امدادی + قرمز هلال‌احمر به عنوان رنگ تاکیدی
        brand: {
          50: "#eff6ff",
          100: "#dbeafe",
          500: "#2563eb",
          600: "#1d4ed8",
          700: "#1e40af",
        },
        accent: "#dc2626",
      },
      fontFamily: {
        vazir: ["Vazirmatn", "Tahoma", "sans-serif"],
      },
    },
  },
  plugins: [],
};
