/** @type {import('tailwindcss').Config} */
export default {
  content: ['./src/**/*.{astro,html,js,jsx,md,mdx,ts,tsx}'],
  darkMode: 'class',
  theme: {
    extend: {
      colors: {
        // Cowork SG Brand Identity Kit palette
        salt:  '#FAFAFA',   // Light background (white)
        sand:  '#F5F0EB',   // Alt BG / cards (cream)
        sky:   '#F5DDD6',   // Light coral tint — ticker / card highlights
        sea:   '#C84330',   // Coral CTAs / links (Pantone 16-1444 TCX)
        terra: '#D98B10',   // Orange accent (Pantone 15-0945 TCX)
        navy:  '#1B3464',   // Deep Blue — hero / footer / primary (Pantone 19-4004 TCX)
      },
      fontFamily: {
        // Cowork SG uses serif headings per brand kit
        display:  ['"Playfair Display"', 'serif'],
        playfair: ['"Playfair Display"', 'serif'],
        sans:     ['"DM Sans"', 'sans-serif'],
        ui:       ['Outfit', 'sans-serif'],
        mono:     ['"DM Mono"', 'monospace'],
      },
      animation: {
        'ticker': 'ticker-scroll 32s linear infinite',
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
