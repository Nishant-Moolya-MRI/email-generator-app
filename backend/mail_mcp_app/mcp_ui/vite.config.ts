import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'
import { viteSingleFile } from 'vite-plugin-singlefile'

const isDevelopment = process.env.NODE_ENV === "development";
// const entry = process.env.ENTRY;

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), viteSingleFile()],
  build: {
    sourcemap: isDevelopment ? "inline" : undefined,
    cssMinify: !isDevelopment,
    minify: !isDevelopment,

    outDir: "dist",
    emptyOutDir: false,
    // rollupOptions: entry ? { input: entry } : undefined,
    rolldownOptions: {
      input: "src/DraftEmailView.html"
    }
  }
})
