/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        space: {
          900: '#0a0a1a',
          800: '#1a1a2e',
          700: '#16213e',
          600: '#0f3460',
          500: '#533483',
        },
        cosmic: {
          cyan: '#00d4ff',
          purple: '#b0b0ff',
          glow: '#0099ff',
        }
      },
      backgroundImage: {
        'space-gradient': 'linear-gradient(135deg, rgba(0, 212, 255, 0.1) 0%, rgba(0, 153, 255, 0.05) 100%)',
      }
    },
  },
  darkMode: 'class',
  plugins: [],
}
