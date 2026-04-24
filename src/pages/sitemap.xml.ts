import type { APIContext } from 'astro';
import { getCollection } from 'astro:content';

export async function GET(context: APIContext) {
  const siteUrl = context.site?.toString().replace(/\/$/, '') ?? 'https://claudecowork.sg';

  const posts = await getCollection('blog', ({ data }) => !data.draft);
  const postUrls = posts.map(
    (post) => `<url><loc>${siteUrl}/blog/${post.slug}/</loc><lastmod>${post.data.date.toISOString().split('T')[0]}</lastmod></url>`,
  );

  const staticUrls = ['', '/blog', '/templates', '/about', '/workshops'].map(
    (path) => `<url><loc>${siteUrl}${path}/</loc></url>`,
  );

  const xml = `<?xml version="1.0" encoding="UTF-8"?>
<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">
${[...staticUrls, ...postUrls].join('\n')}
</urlset>`;

  return new Response(xml, {
    headers: { 'Content-Type': 'application/xml' },
  });
}
