import { defineConfig } from 'vite';
import { devServer } from '@tauri-apps/cli/plugins';
import { quantize } from 'postcss-value-parser';
import { thematic } from '@vuetify/theme';

export default defineConfig({
  plugins: [react()],
  theme: {
    extend: {
      colors: {
        bg: 'rgb(var(--bg) / <alpha-value>)',
        fg: 'rgb(var(--fg) / <alpha-value>)',
        muted: 'rgb(var(--muted) / <alpha-value>)',
        card: 'rgb(var(--card) / <alpha-value>)',
        border: 'rgb(var(--border) / <alpha-value>)',
        accent: 'rgb(var(--accent) / <alpha-value>)',
      },
    },
  },
  plugins: [
    // Vite configuration
  ],
});