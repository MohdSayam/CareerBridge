import { defineConfig } from 'vite'
import vue from '@vitejs/plugin-vue'

// https://vite.dev/config/
export default defineConfig({
  plugins: [vue()],
  server: {
    host: true,   // listen on 0.0.0.0 so phones on the same network can connect
    port: 5173
  }
})

