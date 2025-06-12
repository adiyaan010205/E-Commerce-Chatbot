/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,ts,jsx,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        primary: {
          50: '#eff6ff',
          500: '#3b82f6',
          600: '#2563eb',
          700: '#1d4ed8',
        }
      },
      keyframes: {
        'bounce-once': {
          '0%, 100%': { transform: 'translateY(0)' },
          '20%': { transform: 'translateY(-8px)' },
          '40%': { transform: 'translateY(0)' },
          '60%': { transform: 'translateY(-4px)' },
          '80%': { transform: 'translateY(0)' },
        }
      },
      animation: {
        'bounce-once': 'bounce-once 0.8s ease-in-out 1',
      }
    },
  },
  plugins: [],
}
