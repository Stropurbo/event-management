/** @type {import('tailwindcss').Config} */
module.exports = {
  content: [
    './**/templates/**/*.html', // templates at the app level
    './templates/**/*.html' // templates at the project level
  ],
  theme: {
    extend: {},
  },
  plugins: [],
}

