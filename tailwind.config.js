/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './templates/**/*.html',
    './static/js/main.js',
  ],
  theme: {
    extend: {
      // Punto de quiebre del menú completo (laptop 1024 px y tablet 800 px usan el menú móvil)
      screens: {
        nav: '1200px',
      },
      fontFamily: {
        sans: ['Plus Jakarta Sans', 'sans-serif'],
        display: ['Outfit', 'sans-serif'],
        serif: ['Playfair Display', 'Georgia', 'serif'],
      },
      colors: {
        agro: {
          50: '#f2f8f1',
          100: '#e1f0de',
          200: '#c4e2be',
          300: '#98cb90',
          400: '#65af5b',
          500: '#3f9136',
          600: '#2b7a3d',
          700: '#215f30',
          800: '#1b4c27',
          900: '#14361d',
          950: '#0b2010',
        },
        xpo: {
          cream: '#f4f8f2',
          sand: '#e6f0e2',
          border: '#cde0c6',
          red: '#2b7a3d',
          redDark: '#1e5c2c',
          gold: '#c5a059',
        },
      },
    },
  },
  plugins: [],
};
