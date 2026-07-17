import re

def update_blog():
    with open('blog.html', 'r', encoding='utf-8') as f:
        content = f.read()

    css = """
<style id="premium-blog-grid-css">
  #blog-grid {
    padding: 4rem 0 8rem 0;
    position: relative;
    z-index: 2;
  }
  .premium-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(340px, 1fr));
    gap: 2.5rem;
  }
  .premium-grid .blog-card:first-child {
    grid-column: 1 / -1;
    display: grid;
    grid-template-columns: 1.2fr 1fr;
    gap: 3rem;
    align-items: center;
    background: rgba(13, 21, 32, 0.4);
  }
  [data-theme="light"] .premium-grid .blog-card:first-child {
    background: rgba(255, 255, 255, 0.6);
  }
  @media (max-width: 992px) {
    .premium-grid .blog-card:first-child {
      grid-template-columns: 1fr;
      gap: 1.5rem;
    }
  }
  .blog-card {
    background: var(--card-bg, rgba(13, 21, 32, 0.6));
    backdrop-filter: blur(12px);
    -webkit-backdrop-filter: blur(12px);
    border: 1px solid var(--border, rgba(255, 255, 255, 0.08));
    border-radius: 20px;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    transition: all 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275);
    position: relative;
    overflow: hidden;
    box-shadow: var(--shadow-soft, 0 10px 30px rgba(0,0,0,0.1));
  }
  .blog-card::before {
    content: '';
    position: absolute;
    top: 0; left: 0; right: 0; bottom: 0;
    background: var(--gradient-brand, linear-gradient(135deg, rgba(6, 182, 212, 0.1), rgba(59, 130, 246, 0.1)));
    opacity: 0;
    transition: opacity 0.5s ease;
    z-index: 0;
    pointer-events: none;
  }
  .blog-card:hover {
    transform: translateY(-8px);
    border-color: rgba(6, 182, 212, 0.4);
    box-shadow: 0 20px 40px rgba(0, 0, 0, 0.2), 0 0 20px rgba(6, 182, 212, 0.15);
  }
  .blog-card:hover::before {
    opacity: 0.1;
  }
  [data-theme="light"] .blog-card:hover::before {
    opacity: 0.05;
  }
  .bc-image-wrapper {
    width: 100%;
    height: 240px;
    border-radius: 14px;
    overflow: hidden;
    margin-bottom: 1.5rem;
    position: relative;
    z-index: 1;
    box-shadow: inset 0 0 0 1px rgba(255,255,255,0.1);
  }
  .premium-grid .blog-card:first-child .bc-image-wrapper {
    height: 380px;
    margin-bottom: 0;
  }
  .bc-image {
    width: 100%;
    height: 100%;
    object-fit: cover;
    transition: transform 0.7s ease;
  }
  .blog-card:hover .bc-image {
    transform: scale(1.08);
  }
  .bc-content {
    flex-grow: 1;
    display: flex;
    flex-direction: column;
    z-index: 1;
  }
  .bc-meta {
    display: flex;
    align-items: center;
    gap: 1rem;
    margin-bottom: 1rem;
    font-size: 0.8rem;
    text-transform: uppercase;
    letter-spacing: 1px;
    color: var(--text-muted, #94a3b8);
  }
  .bc-tag {
    background: rgba(6, 182, 212, 0.1);
    color: #06b6d4;
    padding: 0.35rem 0.85rem;
    border-radius: 20px;
    font-weight: 700;
    border: 1px solid rgba(6, 182, 212, 0.2);
  }
  [data-theme="light"] .bc-tag {
    background: rgba(6, 182, 212, 0.15);
    color: #0284c7;
    border-color: rgba(6, 182, 212, 0.3);
  }
  .bc-title {
    font-size: 1.4rem;
    font-weight: 800;
    color: var(--text-primary, #f8fafc);
    margin-bottom: 1rem;
    line-height: 1.4;
    transition: color 0.3s ease;
  }
  .premium-grid .blog-card:first-child .bc-title {
    font-size: 2.2rem;
  }
  .blog-card:hover .bc-title {
    color: #06b6d4;
  }
  .bc-excerpt {
    color: var(--text-secondary, #cbd5e1);
    font-size: 1rem;
    line-height: 1.6;
    margin-bottom: 1.5rem;
    flex-grow: 1;
  }
  .bc-footer {
    display: flex;
    align-items: center;
    justify-content: space-between;
    margin-top: auto;
    padding-top: 1.2rem;
    border-top: 1px solid var(--border, rgba(255, 255, 255, 0.1));
  }
  .bc-read-more {
    display: inline-flex;
    align-items: center;
    gap: 0.5rem;
    color: var(--text-primary, #fff);
    text-decoration: none;
    font-weight: 700;
    font-size: 0.95rem;
    transition: all 0.3s ease;
    text-transform: uppercase;
    letter-spacing: 0.5px;
  }
  .bc-read-more i {
    transition: transform 0.3s ease;
  }
  .blog-card:hover .bc-read-more {
    color: #06b6d4;
  }
  .blog-card:hover .bc-read-more i {
    transform: translateX(6px);
  }
</style>
<section class="tm-section" id="blog-grid">
  <div class="container">
    <div class="premium-grid">
"""

    pattern = r'<!-- Post.*?<article.*?>\s*<div.*?>\s*<img src="(.*?)".*?alt="(.*?)".*?/>\s*</div>\s*<div.*?>(.*?)&nbsp;&nbsp;(.*?)</div>\s*<h3.*?>(.*?)</h3>\s*<p.*?>(.*?)</p>\s*<a.*?href="(.*?)".*?>.*?</a>\s*</article>'
    
    matches = re.finditer(r'<!-- Post (.*?) -->\s*<article class="tm-card-premium"(.*?)</article>', content, flags=re.DOTALL)
    
    cards_html = ""
    for match in matches:
        block = match.group(0)
        img_src_m = re.search(r'<img src="(.*?)"', block)
        img_alt_m = re.search(r'alt="(.*?)"', block)
        meta_m = re.search(r'<div.*?text-transform: uppercase;.*?>(.*?)</div>', block)
        title_m = re.search(r'<h3.*?>(.*?)</h3>', block)
        excerpt_m = re.search(r'<p class="tm-text".*?>(.*?)</p>', block, re.DOTALL)
        link_m = re.search(r'<a.*?href="(.*?)"', block)
        
        if all([img_src_m, img_alt_m, meta_m, title_m, excerpt_m, link_m]):
            img_src = img_src_m.group(1)
            img_alt = img_alt_m.group(1)
            meta = meta_m.group(1).split('  ') # double space
            tag = meta[0].strip()
            date = meta[1].strip() if len(meta) > 1 else ""
            title = title_m.group(1)
            excerpt = excerpt_m.group(1).strip()
            link = link_m.group(1)
            
            cards_html += f'''
      <!-- Post {img_alt} -->
      <article class="blog-card">
        <div class="bc-image-wrapper">
          <img src="{img_src}" alt="{img_alt}" class="bc-image" loading="lazy" />
        </div>
        <div class="bc-content">
          <div class="bc-meta">
            <span class="bc-tag">{tag}</span>
            <span class="bc-date">{date}</span>
          </div>
          <h3 class="bc-title">{title}</h3>
          <p class="bc-excerpt">{excerpt}</p>
          <div class="bc-footer">
            <a href="{link}" class="bc-read-more">Read Article <i class="fas fa-arrow-right"></i></a>
          </div>
        </div>
      </article>'''

    new_section = css + cards_html + '''
    </div>
  </div>
</section>'''

    # Replace the old section
    new_content = re.sub(r'<!-- Blog Grid Section -->\s*<section class="tm-section" id="blog-grid".*?</section>', '<!-- Blog Grid Section -->\n' + new_section, content, flags=re.DOTALL)
    
    with open('blog.html', 'w', encoding='utf-8') as f:
        f.write(new_content)

if __name__ == '__main__':
    update_blog()
    print("Blog updated successfully!")
