import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';

export default defineConfig({
  plugins: [react()],
  server: {
    port: 5173,
    proxy: {
      '/claude': 'http://localhost:8000',
      '/messages': 'http://localhost:8000',
      '/history': 'http://localhost:8000',
      '/bots': 'http://localhost:8000',
      '/memory': 'http://localhost:8000',
    },
  },
});
