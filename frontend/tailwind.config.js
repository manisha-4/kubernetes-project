/** @type {import('tailwindcss').Config} */
export default {
  content: [
    "./index.html",
    "./src/**/*.{js,jsx,ts,tsx}",
  ],
  theme: {
    extend: {
      colors: {
        'paw-pink': '#FF10F0',
        'paw-light-pink': '#FF69B4',
        'paw-pale-pink': '#FFE4F0',
        'paw-dark': '#C71585',
      },
      backgroundImage: {
        'polka-dots': 'radial-gradient(circle, #8B5CF6 2px, transparent 2px)',
        'polka-light': 'radial-gradient(circle, #DCD0FF 2px, transparent 2px)',
      },
      backgroundSize: {
        'polka': '20px 20px',
      }
    },
  },
  plugins: [],
}
