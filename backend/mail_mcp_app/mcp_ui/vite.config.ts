import react from '@vitejs/plugin-react'
import { defineConfig } from 'vite'
import { viteSingleFile } from 'vite-plugin-singlefile'

const isDevelopment = process.env.NODE_ENV === "development";

// Key:Value pairs - Assign a unique name : PATH to UI's HTML file
const ENTRY_POINTS = {
  "draftEmailView" : "src/DraftEmailView.html",
};

// https://vite.dev/config/
export default defineConfig({
  plugins: [react(), viteSingleFile()],
  build: {
    sourcemap: isDevelopment ? "inline" : undefined,
    cssMinify: !isDevelopment,
    minify: !isDevelopment,

    outDir: "dist",
    emptyOutDir: false,
    rollupOptions: {
      input: ENTRY_POINTS
    },
  }
})
