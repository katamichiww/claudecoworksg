#!/usr/bin/env python3
"""Auto-generates the blog listing and homepage blog section from blog/*.html post files."""
import os, re, json, math
from datetime import datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
BLOG_DIR = os.path.join(ROOT, 'blog')
BLOG_HTML = os.path.join(ROOT, 'blog.html')
INDEX_HTML = os.path.join(ROOT, 'index.html')
HOME_MAX = 7
POSTS_PER_PAGE = 8


def extract_meta(filepath):
    with open(filepath, encoding='utf-8') as f:
        content = f.read()

    if '"BlogPosting"' not in content:
        return None

    m = re.search(r'<script type="application/ld\+json">(.*?)</script>', content, re.DOTALL)
    if not m:
        return None
    try:
        ld = json.loads(m.group(1))
    except Exception:
        return None

    # Prefer og:image meta for cover (more reliably maintained than JSON-LD image)
    og_img = re.search(r'<meta property="og:image" content="([^"]+)"', content)
    cover_abs = og_img.group(1) if og_img else ld.get('image', '')
    cover = cover_abs.split('claudecowork.sg/')[-1] if 'claudecowork.sg/' in cover_abs else ''

    tag_m = re.search(r'class="label label-coral"[^>]*>([^<]+)<', content)
    tags = tag_m.group(1).strip() if tag_m else ''

    time_m = re.search(r'~(\d+)\s*min', content)
    read_time = f"~{time_m.group(1)} min" if time_m else ''

    url = ld.get('url', '')
    slug = url.replace('https://claudecowork.sg/blog/', '').rstrip('/')

    return {
        'slug': slug,
        'title': ld.get('headline', ''),
        'description': ld.get('description', ''),
        'date': ld.get('datePublished', ''),
        'tags': tags,
        'cover': cover,
        'read_time': read_time,
    }


def card_html(post, img_prefix=''):
    if post['cover']:
        src = f'{img_prefix}{post["cover"]}'
        img = f'<img class="blog-card-image" src="{src}" alt="{post["title"]}" />'
    else:
        img = '<div class="blog-card-image-placeholder"><span></span></div>'

    try:
        date_str = datetime.strptime(post['date'], '%Y-%m-%d').strftime('%-d %b %Y')
    except Exception:
        date_str = post['date']

    return (
        f'      <a href="/blog/{post["slug"]}" class="blog-card">\n'
        f'        {img}\n'
        f'        <div class="blog-card-body">\n'
        f'          <div class="blog-card-meta">\n'
        f'            <span class="blog-card-tag">{post["tags"]}</span>\n'
        f'            <span class="blog-card-date">{date_str}</span>\n'
        f'          </div>\n'
        f'          <h3>{post["title"]}</h3>\n'
        f'          <p>{post["description"]}</p>\n'
        f'          <span class="blog-card-read">Read post → <span>{post["read_time"]}</span></span>\n'
        f'        </div>\n'
        f'      </a>'
    )


def pagination_html(current_page, total_pages):
    parts = []

    # Prev button
    if current_page == 1:
        parts.append('      <span class="blog-pagination-prev disabled">← Prev</span>')
    elif current_page == 2:
        parts.append('      <a href="/blog" class="blog-pagination-prev">← Prev</a>')
    else:
        parts.append(f'      <a href="/blog/page-{current_page - 1}" class="blog-pagination-prev">← Prev</a>')

    # Page number buttons
    for p in range(1, total_pages + 1):
        if p == current_page:
            parts.append(f'      <span class="blog-pagination-page active">{p}</span>')
        elif p == 1:
            parts.append(f'      <a href="/blog" class="blog-pagination-page">{p}</a>')
        else:
            parts.append(f'      <a href="/blog/page-{p}" class="blog-pagination-page">{p}</a>')

    # Next button
    if current_page == total_pages:
        parts.append('      <span class="blog-pagination-next disabled">Next →</span>')
    else:
        parts.append(f'      <a href="/blog/page-{current_page + 1}" class="blog-pagination-next">Next →</a>')

    inner = '\n'.join(parts)
    return f'    <div class="blog-pagination">\n{inner}\n    </div>'


def page_html(page_num, page_posts, total_posts, total_pages):
    cards = '\n\n'.join(card_html(p, img_prefix='../') for p in page_posts)
    pagination = pagination_html(page_num, total_pages)
    return f'''<!DOCTYPE html>
<html lang="en">
<head>
  <meta charset="UTF-8" />
  <meta name="author" content="Wan Wei Soh" />
  <meta name="robots" content="index, follow" />
  <meta name="viewport" content="width=device-width, initial-scale=1.0" />
  <title>Blog & Resources — Page {page_num} | Cowork SG</title>
  <meta name="description" content="Practical AI guides and how-tos written for non-technical professionals — by the Cowork SG community. Always free." />
  <link rel="canonical" href="https://claudecowork.sg/blog/page-{page_num}" />
  <meta property="og:type" content="website" />
  <meta property="og:url" content="https://claudecowork.sg/blog/page-{page_num}" />
  <meta property="og:title" content="Blog & Resources — Page {page_num} | Cowork SG" />
  <meta property="og:description" content="Practical AI guides and how-tos written for non-technical professionals — by the Cowork SG community. Always free." />
  <meta property="og:image" content="https://claudecowork.sg/uploads/og-image.png" />
  <link rel="stylesheet" href="../styles.css" />
  <style>
    .blog-index-hero {{ background: var(--navy); padding: 5rem 2rem 3.5rem; }}
    .blog-index-hero-inner {{ max-width: 960px; margin: 0 auto; }}
    .blog-index-hero h1 {{ font-family: var(--serif); font-size: clamp(2rem, 5vw, 3rem); font-weight: 700; color: white; margin: 0.75rem 0 0.5rem; }}
    .blog-index-hero p {{ font-size: 1rem; color: rgba(255,255,255,0.55); max-width: 520px; margin: 0; }}
    .blog-index-body {{ max-width: 960px; margin: 0 auto; padding: 3rem 2rem 5rem; }}
    .blog-index-meta-row {{ display: flex; align-items: center; justify-content: space-between; margin-bottom: 2rem; }}
    .blog-post-count {{ font-size: 0.82rem; color: var(--ink-3); font-weight: 600; letter-spacing: 0.05em; text-transform: uppercase; }}
    .blog-card-grid {{ display: grid; grid-template-columns: 1fr 1fr; gap: 1.75rem; }}
    .blog-card {{ display: flex; flex-direction: column; border: 1.5px solid var(--border); border-radius: 12px; overflow: hidden; text-decoration: none; color: inherit; background: white; transition: border-color 200ms ease, box-shadow 200ms ease, transform 200ms ease; }}
    .blog-card:hover {{ border-color: var(--coral); box-shadow: 0 6px 24px rgba(232,97,74,0.10); transform: translateY(-2px); }}
    .blog-card-image {{ width: 100%; aspect-ratio: 16 / 9; object-fit: cover; object-position: center top; display: block; background: var(--surface-2); }}
    .blog-card-image-placeholder {{ width: 100%; aspect-ratio: 16 / 9; background: linear-gradient(135deg, var(--navy) 0%, var(--navy-light) 100%); display: flex; align-items: center; justify-content: center; }}
    .blog-card-image-placeholder span {{ font-size: 2.5rem; }}
    .blog-card-body {{ padding: 1.5rem; display: flex; flex-direction: column; flex: 1; }}
    .blog-card-meta {{ display: flex; align-items: center; gap: 0.75rem; flex-wrap: wrap; margin-bottom: 0.85rem; }}
    .blog-card-tag {{ font-size: 0.7rem; font-weight: 700; letter-spacing: 0.07em; text-transform: uppercase; color: var(--coral); }}
    .blog-card-date {{ font-size: 0.78rem; color: var(--ink-3); margin-left: auto; }}
    .blog-card-body h3 {{ font-family: var(--serif); font-size: 1.1rem; font-weight: 700; line-height: 1.35; color: var(--navy); margin-bottom: 0.65rem; }}
    .blog-card-body p {{ font-size: 0.9rem; line-height: 1.7; color: var(--ink-2); margin-bottom: 1.25rem; flex: 1; }}
    .blog-card-read {{ font-size: 0.83rem; font-weight: 600; color: var(--coral); }}
    .blog-card-read span {{ font-weight: 400; color: var(--ink-3); }}
    .blog-pagination {{ display: flex; align-items: center; justify-content: center; gap: 0.75rem; padding: 2.5rem 0 1rem; }}
    .blog-pagination-prev, .blog-pagination-next {{ font-size: 0.88rem; font-weight: 600; color: var(--coral); text-decoration: none; padding: 0.5rem 1rem; border: 1px solid var(--coral); border-radius: 6px; transition: background 0.15s; }}
    .blog-pagination-prev:hover, .blog-pagination-next:hover {{ background: var(--coral); color: white; }}
    .blog-pagination-prev.disabled, .blog-pagination-next.disabled {{ color: var(--border); border-color: var(--border); pointer-events: none; cursor: default; }}
    .blog-pagination-page {{ font-size: 0.88rem; font-weight: 700; width: 2rem; height: 2rem; display: flex; align-items: center; justify-content: center; border-radius: 50%; color: var(--ink-2); }}
    .blog-pagination-page.active {{ background: var(--navy); color: white; }}
    a.blog-pagination-page {{ text-decoration: none; color: var(--ink-2); }}
    a.blog-pagination-page:hover {{ background: var(--surface); }}
    @media (max-width: 640px) {{ .blog-card-grid {{ grid-template-columns: 1fr; }} .blog-index-hero {{ padding: 3.5rem 1.25rem 2.5rem; }} .blog-index-body {{ padding: 2.5rem 1.25rem 4rem; }} }}
  </style>
  <link rel="icon" type="image/png" sizes="32x32" href="../favicon-32x32.png" />
  <link rel="icon" type="image/png" sizes="16x16" href="../favicon-16x16.png" />
  <link rel="icon" type="image/png" href="../favicon.png" />
  <link rel="apple-touch-icon" sizes="180x180" href="../apple-touch-icon.png" />
</head>
<body>
  <nav class="site-nav">
    <div class="nav-inner">
      <a href="../index.html" class="nav-logo"><img src="../uploads/cowork-sg-logo.png" alt="Cowork SG" /></a>
      <ul class="nav-links" id="navLinks">
        <li><a href="../index.html">Home</a></li>
        <li><a href="../about.html">About</a></li>
        <li><a href="/blog" class="active">Blog</a></li>
        <li><a href="https://chat.whatsapp.com/FZXRkgwcwjA4EOaWIOBPGQ" target="_blank" rel="noopener" class="nav-cta">Join Free →</a></li>
      </ul>
      <button class="nav-mobile-toggle" id="mobileToggle" aria-label="Toggle menu"><span></span><span></span><span></span></button>
    </div>
  </nav>

  <section class="blog-index-hero">
    <div class="blog-index-hero-inner">
      <span class="label">Community Resources</span>
      <h1>All Posts</h1>
      <p>Practical guides written by non-technical professionals, for non-technical professionals. No jargon. No gatekeeping. Always free.</p>
    </div>
  </section>

  <div class="blog-index-body">
    <div class="blog-index-meta-row">
      <span class="blog-post-count">{total_posts} posts · Page {page_num} of {total_pages}</span>
    </div>

    <div class="blog-card-grid">
{cards}
    </div>

{pagination}
  </div>

  <footer class="site-footer">
    <div class="footer-inner">
      <div class="footer-top">
        <div class="footer-brand">
          <div class="footer-logo"><img src="../uploads/cowork-sg-logo-dark.png" alt="Cowork SG" /></div>
          <p>Singapore's free AI community for professionals who want to actually use Claude — not just talk about it.</p>
        </div>
        <div class="footer-col">
          <h4>Community</h4>
          <ul>
            <li><a href="../index.html">Home</a></li>
            <li><a href="/blog">All Posts</a></li>
            <li><a href="https://chat.whatsapp.com/FZXRkgwcwjA4EOaWIOBPGQ" target="_blank" rel="noopener">Join WhatsApp</a></li>
          </ul>
        </div>
        <div class="footer-col">
          <h4>Posts</h4>
          <ul>
            <li><a href="/blog/shipped-to-prod-5-hours">Shipped to Prod in 5 Hours</a></li>
            <li><a href="/blog/claude-architect-exam">Claude Architect Exam</a></li>
            <li><a href="/blog/claude-prompting-outcome-first">Outcome-First Prompting</a></li>
            <li><a href="/blog/claude-cowork-capabilities">7 Claude Capabilities</a></li>
            <li><a href="/blog/claude-whatsapp">Claude + WhatsApp</a></li>
          </ul>
        </div>
      </div>
      <div class="footer-bottom">
        <p class="footer-copy">© 2026 Cowork SG. All rights reserved.</p>
      </div>
    </div>
  </footer>

  <script src="../nav.js"></script>
</body>
</html>'''


def home_row_html(post):
    try:
        date_str = datetime.strptime(post['date'], '%Y-%m-%d').strftime('%-d %b %Y')
    except Exception:
        date_str = post['date']

    if post['cover'] and 'og-image' not in post['cover']:
        img = (
            f'<img src="{post["cover"]}" alt="{post["title"]}" '
            f'style="width:130px;height:130px;object-fit:cover;object-position:center top;'
            f'border-radius:8px;flex-shrink:0;" />'
        )
    else:
        img = ''

    img_block = f'\n          {img}' if img else ''

    return (
        f'        <a href="/blog/{post["slug"]}" class="blog-post-row" style="display:flex;gap:1.5rem;align-items:flex-start;">\n'
        f'          <div style="flex:1;min-width:0;">\n'
        f'            <div class="blog-post-meta">\n'
        f'              <span class="blog-post-tag">{post["tags"]}</span>\n'
        f'              <span class="blog-post-date">{date_str}</span>\n'
        f'            </div>\n'
        f'            <h3>{post["title"]}</h3>\n'
        f'            <p>{post["description"]}</p>\n'
        f'            <span class="blog-post-read">Read post → <span class="blog-post-time">{post["read_time"]}</span></span>\n'
        f'          </div>{img_block}\n'
        f'        </a>'
    )


def main():
    posts = []
    for fname in sorted(os.listdir(BLOG_DIR)):
        if not fname.endswith('.html') or fname.startswith('page-'):
            continue
        meta = extract_meta(os.path.join(BLOG_DIR, fname))
        if meta and meta['slug']:
            posts.append(meta)

    posts.sort(key=lambda p: p['date'], reverse=True)

    total_posts = len(posts)
    total_pages = max(1, math.ceil(total_posts / POSTS_PER_PAGE))

    # Update blog.html (page 1)
    page1_posts = posts[:POSTS_PER_PAGE]
    cards = '\n\n'.join(card_html(p) for p in page1_posts)
    with open(BLOG_HTML, encoding='utf-8') as f:
        html = f.read()
    html = re.sub(
        r'<span class="blog-post-count">[^<]+</span>',
        f'<span class="blog-post-count">{total_posts} posts · Page 1 of {total_pages}</span>',
        html,
    )
    html = re.sub(
        r'<!-- POSTS_START -->.*?<!-- POSTS_END -->',
        f'<!-- POSTS_START -->\n{cards}\n    <!-- POSTS_END -->',
        html,
        flags=re.DOTALL,
    )
    new_pagination = pagination_html(1, total_pages)
    html = re.sub(
        r'<!-- PAGINATION_START -->.*?<!-- PAGINATION_END -->',
        f'<!-- PAGINATION_START -->\n{new_pagination}\n    <!-- PAGINATION_END -->',
        html,
        flags=re.DOTALL,
    )
    with open(BLOG_HTML, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f'blog.html updated — {len(page1_posts)} posts (page 1 of {total_pages})')

    # Remove stale page-N.html files
    for fname in os.listdir(BLOG_DIR):
        if re.match(r'^page-\d+\.html$', fname):
            os.remove(os.path.join(BLOG_DIR, fname))

    # Generate page-N.html for pages 2+
    for page_num in range(2, total_pages + 1):
        start = (page_num - 1) * POSTS_PER_PAGE
        page_posts = posts[start:start + POSTS_PER_PAGE]
        content = page_html(page_num, page_posts, total_posts, total_pages)
        out_path = os.path.join(BLOG_DIR, f'page-{page_num}.html')
        with open(out_path, 'w', encoding='utf-8') as f:
            f.write(content)
        print(f'blog/page-{page_num}.html written — {len(page_posts)} posts')

    # Update index.html homepage (max HOME_MAX newest posts)
    home_posts = posts[:HOME_MAX]
    rows = '\n'.join(home_row_html(p) for p in home_posts)
    with open(INDEX_HTML, encoding='utf-8') as f:
        idx = f.read()
    idx = re.sub(
        r'<!-- HOME_POSTS_START -->.*?<!-- HOME_POSTS_END -->',
        f'<!-- HOME_POSTS_START -->\n{rows}\n        <!-- HOME_POSTS_END -->',
        idx,
        flags=re.DOTALL,
    )
    with open(INDEX_HTML, 'w', encoding='utf-8') as f:
        f.write(idx)
    print(f'index.html updated — {len(home_posts)} posts (max {HOME_MAX})')


if __name__ == '__main__':
    main()
