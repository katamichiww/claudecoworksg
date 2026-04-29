#!/usr/bin/env python3
"""Auto-generates the blog listing page from blog/*.html post files."""
import os, re, json
from datetime import datetime

ROOT = os.path.dirname(os.path.abspath(__file__))
BLOG_DIR = os.path.join(ROOT, 'blog')
BLOG_HTML = os.path.join(ROOT, 'blog.html')


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


def card_html(post):
    if post['cover']:
        img = f'<img class="blog-card-image" src="{post["cover"]}" alt="{post["title"]}" />'
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


def main():
    posts = []
    for fname in sorted(os.listdir(BLOG_DIR)):
        if not fname.endswith('.html'):
            continue
        meta = extract_meta(os.path.join(BLOG_DIR, fname))
        if meta and meta['slug']:
            posts.append(meta)

    posts.sort(key=lambda p: p['date'], reverse=True)

    cards = '\n\n'.join(card_html(p) for p in posts)

    with open(BLOG_HTML, encoding='utf-8') as f:
        html = f.read()

    html = re.sub(
        r'<span class="blog-post-count">\d+ posts</span>',
        f'<span class="blog-post-count">{len(posts)} posts</span>',
        html,
    )
    html = re.sub(
        r'<!-- POSTS_START -->.*?<!-- POSTS_END -->',
        f'<!-- POSTS_START -->\n{cards}\n    <!-- POSTS_END -->',
        html,
        flags=re.DOTALL,
    )

    with open(BLOG_HTML, 'w', encoding='utf-8') as f:
        f.write(html)

    print(f'blog.html updated — {len(posts)} posts')


if __name__ == '__main__':
    main()
