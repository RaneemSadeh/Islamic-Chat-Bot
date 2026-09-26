import path from 'node:path';

import react from '@vitejs/plugin-react';
import { defineConfig, loadEnv } from 'vite';

export default defineConfig(({ mode }) => {
  const env = loadEnv(mode, process.cwd(), '');

  // Accept either name so an existing `.env` with GEMINI_API_KEY keeps working
  // while the code reads the conventional, explicitly public VITE_ prefix.
  const geminiKey = env.VITE_GEMINI_API_KEY || env.GEMINI_API_KEY || '';

  return {
    server: { port: 3000, host: '0.0.0.0' },
    preview: { port: 3000 },
    plugins: [react()],
    define: {
      'import.meta.env.VITE_GEMINI_API_KEY': JSON.stringify(geminiKey),
    },
    resolve: {
      alias: { '@': path.resolve(__dirname, 'src') },
    },
    build: {
      outDir: 'dist',
      sourcemap: mode !== 'production',
    },
  };
});
