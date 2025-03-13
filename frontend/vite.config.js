import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  optimizeDeps: {
    exclude: ['latex.js'], // Exclude latex.js from optimization
  },
  build: {
    rollupOptions: {
      external: ['latex.js'], // Treat latex.js as an external dependency
    },
  },
});