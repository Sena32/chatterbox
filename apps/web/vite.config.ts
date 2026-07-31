import { defineConfig } from "vite"
import react from "@vitejs/plugin-react"

const API_BASE_URL = process.env.API_INTERNAL_URL  ?? "http://api:8000"

export default defineConfig({
  plugins: [react()],
  server: {
    host: "0.0.0.0",
    port: 5173,
    // Proxy das chamadas /api para o backend FastAPI em dev (evita CORS)
    proxy: {
      "/api": {
        target: API_BASE_URL,
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, ""),
      },
    },
  },
})
