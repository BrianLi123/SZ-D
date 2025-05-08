import { defineConfig, splitVendorChunkPlugin } from 'vite';
import react from '@vitejs/plugin-react';
import { resolve } from 'path';
import AutoImport from 'unplugin-auto-import/vite';
import { theme } from 'antd';

const { getDesignToken } = theme;
const {colorPrimary} = getDesignToken();

// https://vitejs.dev/config/
/** @type {import('vite').UserConfig} */
export default defineConfig({
  server: {
    port: 3003,
    proxy: {
      '/api': {
        target: 'http://127.0.0.1:8000',
        changeOrigin: true,
        rewrite: (path) => path.replace(/^\/api/, '')
      }
    },
    open: false
  },
  resolve: {
    alias: {
      '@': resolve(__dirname, './src'),
      scan: resolve(__dirname, './scan')
    }
  },
  plugins: [
    react(),
    splitVendorChunkPlugin(),
    AutoImport({
      imports: ['react'],
      dts: 'src/auto-imports.d.ts',
      dirs: ['src/hooks', 'src/locales', 'src/store/reducer'],
      eslintrc: {
        enabled: true, // Default `false`
        filepath: './.eslintrc-auto-import.json', // Default `./.eslintrc-auto-import.json`
        globalsPropValue: true // Default `true`, (true | false | 'readonly' | 'readable' | 'writable' | 'writeable')
      }
    })
  ],
  css: {
    preprocessorOptions: {
      less: {
        modifyVars: {
          "@primary-color": colorPrimary
        },
        javascriptEnabled: true
      }
    }
  }
});
