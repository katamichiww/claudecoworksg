/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,ts,tsx}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // ANCHR AI Labs "Salt & Sand" palette
        salt:  '#FAFAF8',   // Primary BG
        sand:  '#F0EBE3',   // Alt BG / cards
        sky:   '#BDD5EA',   // Ticker / highlights
        sea:   '#4A90A4',   // CTA / links
        terra: '#C17F5A',   // Accent / alert
        navy:  '#1E2B38',   // Hero / footer / primary text
      },
      fontFamily: {
        display:  ['"Clash Display"', 'sans-serif'],
        playfair: ['"Playfair Display"', 'serif'],
        sans:     ['"DM Sans"', 'sans-serif'],
        ui:       ['Outfit', 'sans-serif'],
        mono:     ['"DM Mono"', 'monospace'],
      },
      animation: {
        'ticker': 'ticker-scroll 28s linear infinite',
      },
      keyframes: {
        'ticker-scroll': {
          from: { transform: 'translateX(0)' },
          to:   { transform: 'translateX(-50%)' },
        },
      },
    },
  },
  plugins: [
    require('@tailwindcss/typography'),
  ],
};
