# Claude Cowork

**claudecowork.sg** — A content hub teaching non-technical professionals how to use AI tools to build real workflows. Powered by [ANCHR AI Labs](https://anchr.ai).

> "Most people use AI tools. Operators build systems."

## Stack

- [Astro](https://astro.build) 4.x with TypeScript (strict)
- Tailwind CSS + `@tailwindcss/typography`
- Markdown content collections with Zod schema validation
- Deploy target: [Vercel](https://vercel.com)

---

## Local development

```bash
npm install
npm run dev
```

The dev server starts at `http://localhost:4321`.

---

## Adding a new blog post (daily workflow)

1. Create a file in `src/content/blog/` named `YYYY-MM-DD-your-slug.md`
2. Add the required frontmatter:

```md
---
title: "Your Post Title"
date: 2026-04-25
description: "One sentence that appears in the blog card and meta description."
tags: ["claude", "workflows"]
draft: false
---

Your post body in Markdown.
```

3. Set `draft: true` while writing; change to `false` to publish.
4. The post will appear at `/blog/YYYY-MM-DD-your-slug` and show up in the blog index, homepage feed, and RSS automatically.
5. Every post automatically gets a **Bridge CTA** at the bottom pointing to `/workshops`.

**Reading time** is calculated automatically from word count (~200 wpm).

---

## Wiring up email capture

The `EmailCapture` component uses Formspree as a placeholder. To activate:

1. Create a free account at [formspree.io](https://formspree.io)
2. Create a new form and copy the form ID (e.g. `xpwzabcd`)
3. Open `src/components/EmailCapture.astro` and replace `YOUR_FORMSPREE_ID` with your ID, **or** pass it as a prop:

```astro
<EmailCapture formspreeId="xpwzabcd" />
```

When you're ready to switch to ConvertKit or Mailchimp, replace the `<form>` action in `EmailCapture.astro`.

---

## Deploying to Vercel

### First deploy

1. Push this repo to GitHub:

```bash
cd claudecowork
git init
git add .
git commit -m "Initial commit"
gh repo create claudecowork --public --source=. --push
# or: git remote add origin https://github.com/YOUR_USERNAME/claudecowork.git && git push -u origin main
```

2. Go to [vercel.com](https://vercel.com) → **Add New Project** → import your GitHub repo.

3. Vercel auto-detects Astro. Leave the build settings as-is:
   - Build command: `npm run build`
   - Output directory: `dist`

4. Click **Deploy**. Done.

### Pointing claudecowork.sg at Vercel

In your domain registrar (where you bought `claudecowork.sg`):

1. Add an **A record** pointing `@` to Vercel's IP: `76.76.21.21`
2. Add a **CNAME record** pointing `www` to `cname.vercel-dns.com`

In Vercel dashboard → your project → **Settings → Domains**:
- Add `claudecowork.sg` and `www.claudecowork.sg`
- Vercel will provision SSL automatically

DNS propagation takes 10–60 minutes.

### Subsequent deploys

Push to `main` — Vercel deploys automatically via GitHub integration.

---

## Project structure

```
src/
├── content/
│   ├── config.ts          ← Zod schema for blog collection
│   └── blog/              ← Markdown posts (YYYY-MM-DD-slug.md)
├── components/
│   ├── Header.astro
│   ├── Footer.astro
│   ├── Hero.astro
│   ├── UseCaseCard.astro
│   ├── BlogCard.astro
│   ├── EmailCapture.astro ← Wire up Formspree ID here
│   ├── BridgeCTA.astro    ← Auto-appended to every post
│   └── PoweredByAnchr.astro
├── layouts/
│   ├── BaseLayout.astro   ← All pages
│   └── BlogLayout.astro   ← Blog post pages
└── pages/
    ├── index.astro        ← Homepage
    ├── blog/
    │   ├── index.astro    ← Blog listing
    │   └── [...slug].astro← Individual posts
    ├── templates.astro
    ├── about.astro
    ├── workshops.astro
    └── rss.xml.ts         ← RSS feed
```

Sitemap is auto-generated at `/sitemap-index.xml` by `@astrojs/sitemap`.
