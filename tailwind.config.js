/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './**/templates/**/*.html', // templates at the app level
    './templates/**/*.html' // templates at the project level
  ],
  theme: {
    extend: {
      fontFamily:{
        'roboto': ["Roboto Condensed", 'sans-serif'],
        'mono': ["Roboto Mono", 'monospace'],
        'poppins': ["Poppins", 'sans-serif'],
      }
    },
  },
  plugins: [],
}

