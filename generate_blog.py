import re
import os
from bs4 import BeautifulSoup
with open("about-us.html", "r", encoding="utf-8") as f:
    content = f.read()

# We need the top part: from <html> to the end of <nav> or the start of <section class="hero ...">
# Let's find where the hero section starts and ends.
# We also need the footer. Let's find <!-- Footer -->

header_match = re.search(r'^(.*?)(<!-- Hero Section|<!-- Hero|<!-- Hero Section -->|<section class="hero)', content, flags=re.DOTALL | re.IGNORECASE)
footer_match = re.search(r'(<!-- Footer -->|<footer>|<footer class=.*?>).*$', content, flags=re.DOTALL | re.IGNORECASE)

if header_match and footer_match:
    header = header_match.group(1)
    footer = footer_match.group(0)

    # Blog content (This will be the template for individual blog posts)
    blog_content = """
  <!-- Blog Hero Section -->
  <section class="hero">
    <!-- Keep the interactive aurora backgrounds -->
    <div class="hero-aurora"></div>
    <div class="hero-aurora" style="top: 20%; left: 60%; background: radial-gradient(circle at center, rgba(15, 95, 220, 0.4), transparent 50%);"></div>

    <!-- Navigation included in header normally, but maybe hero contains nav? Let's assume header has nav or hero has nav -->
    <div class="container hero-content" style="padding-top: 150px; text-align: center;">
      <div class="hero-badge reveal">Latest Insights</div>
      <h1 class="hero-title reveal" style="font-size: 4rem; line-height: 1.1;">Vedtam <span class="gradient-text">Blog</span></h1>
      <p class="hero-subtitle reveal">News, technology advice, and cybersecurity culture.</p>
    </div>
  </section>

  <!-- Blog Grid Section -->
  <section class="blog-section" style="padding: 5rem 0; background: var(--dark1); position: relative; z-index: 2;">
    <div class="container">
      <div class="blog-grid" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(320px, 1fr)); gap: 2rem;">
        
        <!-- Post 1 -->
        <article class="tm-card-premium blog-card" style="text-align: left; padding: 2rem;">
          <div class="blog-thumb" style="height: 200px; background: rgba(0,0,0,0.5); border-radius: 8px; margin-bottom: 1.5rem; overflow: hidden; display: flex; align-items: center; justify-content: center; border: 1px solid rgba(255,255,255,0.1);">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.2)" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><circle cx="8.5" cy="8.5" r="1.5"></circle><polyline points="21 15 16 10 5 21"></polyline></svg>
          </div>
          <div class="blog-meta" style="font-size: 0.85rem; color: #64748b; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 1px;">Cybersecurity • Oct 12, 2026</div>
          <h3 class="blog-title" style="font-size: 1.5rem; color: #fff; margin-bottom: 1rem; line-height: 1.3;">The Future of Zero Trust Architecture</h3>
          <p class="blog-excerpt" style="color: rgba(255,255,255,0.7); font-size: 0.95rem; line-height: 1.6; margin-bottom: 1.5rem;">Discover how implementing a zero trust model protects your digital assets against evolving sophisticated threats.</p>
          <a href="#" class="blog-read-more" style="color: #00a3d9; text-decoration: none; font-weight: 600; display: inline-flex; align-items: center; gap: 0.5rem;">Read Article <span style="font-size:1.2rem;">→</span></a>
        </article>

        <!-- Post 2 -->
        <article class="tm-card-premium blog-card" style="text-align: left; padding: 2rem;">
          <div class="blog-thumb" style="height: 200px; background: rgba(0,0,0,0.5); border-radius: 8px; margin-bottom: 1.5rem; overflow: hidden; display: flex; align-items: center; justify-content: center; border: 1px solid rgba(255,255,255,0.1);">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.2)" stroke-width="2"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path><polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" y1="22.08" x2="12" y2="12"></line></svg>
          </div>
          <div class="blog-meta" style="font-size: 0.85rem; color: #64748b; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 1px;">Cloud Infrastructure • Sep 28, 2026</div>
          <h3 class="blog-title" style="font-size: 1.5rem; color: #fff; margin-bottom: 1rem; line-height: 1.3;">Scaling Seamlessly During Peak Traffic</h3>
          <p class="blog-excerpt" style="color: rgba(255,255,255,0.7); font-size: 0.95rem; line-height: 1.6; margin-bottom: 1.5rem;">A deep dive into auto-scaling strategies and resilient cloud deployments for high-volume enterprise applications.</p>
          <a href="#" class="blog-read-more" style="color: #00a3d9; text-decoration: none; font-weight: 600; display: inline-flex; align-items: center; gap: 0.5rem;">Read Article <span style="font-size:1.2rem;">→</span></a>
        </article>

        <!-- Post 3 -->
        <article class="tm-card-premium blog-card" style="text-align: left; padding: 2rem;">
          <div class="blog-thumb" style="height: 200px; background: rgba(0,0,0,0.5); border-radius: 8px; margin-bottom: 1.5rem; overflow: hidden; display: flex; align-items: center; justify-content: center; border: 1px solid rgba(255,255,255,0.1);">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.2)" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>
          </div>
          <div class="blog-meta" style="font-size: 0.85rem; color: #64748b; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 1px;">Compliance • Sep 10, 2026</div>
          <h3 class="blog-title" style="font-size: 1.5rem; color: #fff; margin-bottom: 1rem; line-height: 1.3;">Navigating the New DPDP Act Requirements</h3>
          <p class="blog-excerpt" style="color: rgba(255,255,255,0.7); font-size: 0.95rem; line-height: 1.6; margin-bottom: 1.5rem;">Ensure your business is ready for India's Digital Personal Data Protection Act with these actionable compliance steps.</p>
          <a href="#" class="blog-read-more" style="color: #00a3d9; text-decoration: none; font-weight: 600; display: inline-flex; align-items: center; gap: 0.5rem;">Read Article <span style="font-size:1.2rem;">→</span></a>
        </article>

        <!-- Post 4 -->
        <article class="tm-card-premium blog-card" style="text-align: left; padding: 2rem;">
          <div class="blog-thumb" style="height: 200px; background: rgba(0,0,0,0.5); border-radius: 8px; margin-bottom: 1.5rem; overflow: hidden; display: flex; align-items: center; justify-content: center; border: 1px solid rgba(255,255,255,0.1);">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.2)" stroke-width="2"><path d="M21.21 15.89A10 10 0 1 1 8 2.83"></path><path d="M22 12A10 10 0 0 0 12 2v10z"></path></svg>
          </div>
          <div class="blog-meta" style="font-size: 0.85rem; color: #64748b; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 1px;">DevOps • Aug 22, 2026</div>
          <h3 class="blog-title" style="font-size: 1.5rem; color: #fff; margin-bottom: 1rem; line-height: 1.3;">Why CI/CD Automation is Non-Negotiable</h3>
          <p class="blog-excerpt" style="color: rgba(255,255,255,0.7); font-size: 0.95rem; line-height: 1.6; margin-bottom: 1.5rem;">How automated pipelines reduce human error and dramatically accelerate time-to-market for enterprise software.</p>
          <a href="#" class="blog-read-more" style="color: #00a3d9; text-decoration: none; font-weight: 600; display: inline-flex; align-items: center; gap: 0.5rem;">Read Article <span style="font-size:1.2rem;">→</span></a>
        </article>

        <!-- Post 5 -->
        <article class="tm-card-premium blog-card" style="text-align: left; padding: 2rem;">
          <div class="blog-thumb" style="height: 200px; background: rgba(0,0,0,0.5); border-radius: 8px; margin-bottom: 1.5rem; overflow: hidden; display: flex; align-items: center; justify-content: center; border: 1px solid rgba(255,255,255,0.1);">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.2)" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect><line x1="8" y1="21" x2="16" y2="21"></line><line x1="12" y1="17" x2="12" y2="21"></line></svg>
          </div>
          <div class="blog-meta" style="font-size: 0.85rem; color: #64748b; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 1px;">Company News • Aug 05, 2026</div>
          <h3 class="blog-title" style="font-size: 1.5rem; color: #fff; margin-bottom: 1rem; line-height: 1.3;">Vedtam Recognized as Top Managed Service Provider</h3>
          <p class="blog-excerpt" style="color: rgba(255,255,255,0.7); font-size: 0.95rem; line-height: 1.6; margin-bottom: 1.5rem;">We are honored to receive industry recognition for our commitment to 24/7 proactive IT managed services.</p>
          <a href="#" class="blog-read-more" style="color: #00a3d9; text-decoration: none; font-weight: 600; display: inline-flex; align-items: center; gap: 0.5rem;">Read Article <span style="font-size:1.2rem;">→</span></a>
        </article>

        <!-- Post 6 -->
        <article class="tm-card-premium blog-card" style="text-align: left; padding: 2rem;">
          <div class="blog-thumb" style="height: 200px; background: rgba(0,0,0,0.5); border-radius: 8px; margin-bottom: 1.5rem; overflow: hidden; display: flex; align-items: center; justify-content: center; border: 1px solid rgba(255,255,255,0.1);">
            <svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.2)" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>
          </div>
          <div class="blog-meta" style="font-size: 0.85rem; color: #64748b; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 1px;">OT Security • Jul 18, 2026</div>
          <h3 class="blog-title" style="font-size: 1.5rem; color: #fff; margin-bottom: 1rem; line-height: 1.3;">Securing Critical Infrastructure Networks</h3>
          <p class="blog-excerpt" style="color: rgba(255,255,255,0.7); font-size: 0.95rem; line-height: 1.6; margin-bottom: 1.5rem;">Why traditional IT security measures fail in industrial settings, and how to properly segment and protect OT environments.</p>
          <a href="#" class="blog-read-more" style="color: #00a3d9; text-decoration: none; font-weight: 600; display: inline-flex; align-items: center; gap: 0.5rem;">Read Article <span style="font-size:1.2rem;">→</span></a>
        </article>

      </div>
    </div>
  </section>
"""

    # Fix the title and meta for SEO
    header = header.replace('<title>About Us - Vedtam Tech Solutions</title>', '<title>Blog & Insights | Vedtam Tech Solutions</title>')
    header = header.replace('content="Learn about Vedtam Tech Solutions', 'content="Vedtam Tech Solutions Blog. Discover the latest insights')
    header = header.replace('about-us.html', 'blog.html')

    # Create the main blog listing page (blog.html)
    with open(os.path.join(os.path.dirname(__file__), "blog.html"), "w", encoding="utf-8") as out:
        out.write(header + blog_content + footer) # blog_content here is actually the hero for the blog listing page
    print("blog.html (listing page) created successfully.")

    # Now, let's generate the individual blog posts
    blog_posts_data = [
        {
            "filename": "blog-iso-27001-vs-soc-2.html",
            "title": "ISO 27001 vs SOC 2: Which Certification Does Your Business Need?",
            "category": "Compliance",
            "date": "Apr 08, 2026",
            "read_time": "5 Min Read",
            "image_svg": '<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.15)" stroke-width="2"><rect x="3" y="3" width="18" height="18" rx="2" ry="2"></rect><circle cx="8.5" cy="8.5" r="1.5"></circle><polyline points="21 15 16 10 5 21"></polyline></svg>',
            "excerpt": "Compare ISO 27001 and SOC 2 certifications to determine which is right for your business — covering scope, cost, timeline, and market requirements.",
            "content_file": "blog-iso-27001-vs-soc-2.html" # This will be the actual content
        },
        {
            "filename": "blog-zero-trust-cloud-architecture.html",
            "title": "How to Build a Zero Trust Cloud Architecture",
            "category": "Cybersecurity",
            "date": "Apr 08, 2026",
            "read_time": "4 Min Read",
            "image_svg": '<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.15)" stroke-width="2"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path><polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" y1="22.08" x2="12" y2="12"></line></svg>',
            "excerpt": "A practical guide to building Zero Trust cloud architecture for Indian enterprises — covering identity, network, workload, and data security in AWS, Azure, and GCP.",
            "content_file": "blog-zero-trust-cloud-architecture.html"
        },
        {
            "filename": "blog-iso-27001-certification-guide-india.html",
            "title": "ISO 27001 Certification: Step-by-Step Guide for Indian Companies",
            "category": "Compliance",
            "date": "Apr 08, 2026",
            "read_time": "4 Min Read",
            "image_svg": '<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.15)" stroke-width="2"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" y1="13" x2="8" y2="13"></line><line x1="16" y1="17" x2="8" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>',
            "excerpt": "A complete step-by-step guide to ISO 27001 certification for Indian enterprises, from gap assessment to audit and certification.",
            "content_file": "blog-iso-27001-certification-guide-india.html"
        },
        {
            "filename": "blog-data-protection-officer-dpdp-act.html",
            "title": "How to Appoint a Data Protection Officer Under the DPDP Act",
            "category": "DPDP Act & Data Privacy",
            "date": "Apr 08, 2026",
            "read_time": "5 Min Read",
            "image_svg": '<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.15)" stroke-width="2"><path d="M21.21 15.89A10 10 0 1 1 8 2.83"></path><path d="M22 12A10 10 0 0 0 12 2v10z"></path></svg>',
            "excerpt": "A complete guide to understanding when a DPO is required under India's DPDP Act, what qualifications they need, and how to appoint one.",
            "content_file": "blog-data-protection-officer-dpdp-act.html"
        },
        {
            "filename": "blog-dpdp-act-penalties-non-compliance.html",
            "title": "DPDP Act Penalties: What Happens if Your Business is Non-Compliant?",
            "category": "DPDP Act & Data Privacy",
            "date": "Apr 08, 2026",
            "read_time": "5 Min Read",
            "image_svg": '<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.15)" stroke-width="2"><rect x="2" y="3" width="20" height="14" rx="2" ry="2"></rect><line x1="8" y1="21" x2="16" y2="21"></line><line x1="12" y1="17" x2="12" y2="21"></line></svg>',
            "excerpt": "Understand the financial penalties, enforcement mechanisms, and business consequences of DPDP Act non-compliance for Indian enterprises.",
            "content_file": "blog-dpdp-act-penalties-non-compliance.html"
        },
        {
            "filename": "blog-dpdp-act-vs-gdpr-differences.html",
            "title": "DPDP Act vs GDPR: Key Differences Indian Companies Must Know",
            "category": "DPDP Act & Data Privacy",
            "date": "Apr 08, 2026",
            "read_time": "5 Min Read",
            "image_svg": '<svg width="48" height="48" viewBox="0 0 24 24" fill="none" stroke="rgba(255,255,255,0.15)" stroke-width="2"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>',
            "excerpt": "A detailed comparison of India's DPDP Act 2023 and Europe's GDPR — helping Indian enterprises understand the similarities, gaps, and dual compliance requirements.",
            "content_file": "blog-dpdp-act-vs-gdpr-differences.html"
        },
        # Add more blog posts here following the same structure
    ]

    # Generate individual blog post HTML files
    for post_data in blog_posts_data:
        post_header = header.replace('<title>Blog & Insights | Vedtam Tech Solutions</title>', f'<title>{post_data["title"]} | Vedtam</title>')
        post_header = post_header.replace('content="Vedtam Tech Solutions Blog. Discover the latest insights', f'content="{post_data["excerpt"]}"')
        post_header = post_header.replace('blog.html', post_data["filename"])

        post_hero = f"""
  <!-- Blog Post Hero Section -->
  <section class="hero" style="min-height: 60vh;">
    <div class="hero-media" aria-hidden="true">
      <div class="hero-interactive-bg" id="heroInteractiveBg">
        <span class="hero-aurora orb-a"></span>
        <span class="hero-aurora orb-b"></span>
        <span class="hero-aurora orb-c"></span>
        <span class="hero-spotlight"></span>
      </div>
    </div>
    <div class="hero-bg"></div>
    <div class="hero-grid"></div>
    <div class="hero-glow"></div>
    <div class="container hero-shell" style="padding-top: 150px; text-align: center; justify-content: center; align-items: center;">
      <div class="hero-content" style="max-width: 900px;">
        <div class="hero-badge reveal">{post_data["category"]}</div>
        <h1 class="hero-title reveal" style="margin-bottom: 1rem; font-size: 3.5rem;"><span class="gradient-text">{post_data["title"].split(':')[0]}:</span> {post_data["title"].split(':')[1] if ':' in post_data["title"] else ''}</h1>
        <div class="article-meta-info reveal">
            <span>By Vedtam Tech Solutions</span>
            <span>•</span>
            <span>{post_data["date"]}</span>
            <span>•</span>
            <span>{post_data["read_time"]}</span>
        </div>
      </div>
    </div>
  </section>
"""
        # Read the actual content from the corresponding HTML file
        with open(os.path.join(os.path.dirname(__file__), "blog", post_data["content_file"]), "r", encoding="utf-8") as f:
            article_content = f.read()
        
        # Extract only the main content from the article HTML (assuming it's within <section class="tm-section">)
        article_soup = BeautifulSoup(article_content, 'html.parser')
        main_article_section = article_soup.find('section', class_='tm-section')
        
        if main_article_section:
            # Replace the placeholder blog_content with the actual article content
            final_post_content = post_header + post_hero + str(main_article_section) + footer
            
            # Save the individual blog post file in the blog subdirectory
            output_filepath = os.path.join(os.path.dirname(__file__), "blog", post_data["filename"])
            with open(output_filepath, "w", encoding="utf-8") as out:
                out.write(final_post_content)
            print(f"Generated individual blog post: {post_data['filename']}")
        else:
            print(f"Warning: Could not find <section class='tm-section'> in {post_data['content_file']}")

else:
    print("Could not find header or footer.")
