import { defineConfig } from 'vite';
import { config as tailwindConfig } from 'tailwindcss';
import { parseColor } from 'tailwindcss/colors';
import { hydra } from 'tailwindcss/plugin';

export default defineConfig({
  plugins: [
    hydra({
      darkMode: ['class', '.dark'],
    }),
  ],
  theme: {
    extend: {
      colors: {
        // Use CSS variables for theme tokens
        '--bg': 'rgb(var(--bg) / <alpha-value>)',
        '--fg': 'rgb(var(--fg) / <alpha-value>)',
        '--muted': 'rgb(var(--muted) / <alpha-value>)',
        '--card': 'rgb(var(--card) / <alpha-value>)',
        '--border': 'rgb(var(--border) / <alpha-value>)',
        '--accent': 'rgb(var(--accent) / <alpha-value>)',
      },
    },
  ],
});