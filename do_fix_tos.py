import os
import re

# 1. Read the good nav from privacy-policy.html
with open('privacy-policy.html', 'r', encoding='utf-8') as f:
    privacy_html = f.read()

nav_match = re.search(r'<nav class="navbar" id="navbar">.*?</nav>', privacy_html, re.DOTALL)
mob_match = re.search(r'<div class="mobile-nav" id="mobileNav">.*?</div>', privacy_html, re.DOTALL)

nav_html = nav_match.group(0) if nav_match else ""
mob_html = mob_match.group(0) if mob_match else ""

# Fix the active class in mobile nav for Terms of Service
mob_html = mob_html.replace('class="active">Privacy Policy', '>Privacy Policy')
mob_html = mob_html.replace('>Terms of Service', ' class="active">Terms of Service')

# 2. Reconstruct terms-of-service.html from the good pieces
with open('terms-of-service.html', 'r', encoding='utf-8') as f:
    tos_content = f.read()

# Currently tos_content might be mangled. We need to find everything up to <body> 
# and everything after the Hero section starts to reconstruct it.
# Wait, let's just use the pristine text from the view_file logs. I will recreate it manually.

pristine_top = """<!DOCTYPE html>
<html lang="en">

<head>
  <link rel="icon" type="image/png" href="Vedtam Logo favicon.png">
  <meta charset="UTF-8">
  <meta name="robots" content="index, follow, max-image-preview:large">
  <meta name="viewport" content="width=device-width, initial-scale=1.0">
  <title>Terms of Service - Vedtam Tech Solutions</title>
  <meta name="description"
    content="Read the Terms of Service for Vedtam Tech Solutions. Understand the conditions governing use of our website, IT, cybersecurity, and consulting services.">
  <link rel="canonical" href="https://www.vedtam.com/terms-of-service.html">
  <meta property="og:type" content="website">
  <meta property="og:url" content="https://www.vedtam.com/terms-of-service.html">
  <meta property="og:title" content="Terms of Service - Vedtam Tech Solutions">
  <meta property="og:description"
    content="Read the Terms of Service for Vedtam Tech Solutions covering website use, service agreements, and liability.">
  <meta property="og:image" content="https://www.vedtam.com/favicon%20vedtam.png">
  <meta name="twitter:card" content="summary_large_image">
  <link rel="preconnect" href="https://fonts.googleapis.com">
  <link rel="preconnect" href="https://fonts.gstatic.com" crossorigin>
  <link href="https://fonts.googleapis.com/css2?family=Manrope:wght@400;500;600;700;800&display=swap" rel="stylesheet">
  <link rel="stylesheet" href="vedtam.css">
  <script
    type="application/ld+json">{"@context":"https://schema.org","@type":"WebPage","name":"Terms of Service","url":"https://www.vedtam.com/terms-of-service.html","isPartOf":{"@type":"WebSite","name":"Vedtam Tech Solutions","url":"https://www.vedtam.com"}}</script>
  <style>
    .legal-hero {
      background: linear-gradient(135deg, #111114 0%, #1a1a20 100%);
      padding: 7rem 0 4rem;
      position: relative;
      overflow: hidden;
    }

    .legal-hero::before {
      content: '';
      position: absolute;
      inset: 0;
      background: radial-gradient(ellipse 60% 80% at 20% 50%, rgba(8, 68, 129, 0.12), transparent 60%);
      pointer-events: none;
    }

    .legal-hero-inner {
      position: relative;
      z-index: 1;
    }

    .legal-hero .hero-badge {
      display: inline-block;
      padding: 0.45rem 1.1rem;
      background: rgba(8, 68, 129, 0.15);
      border: 1px solid rgba(8, 68, 129, 0.3);
      border-radius: 999px;
      color: var(--orange) !important;
      font-size: 0.78rem;
      font-weight: 700;
      letter-spacing: 0.08em;
      text-transform: uppercase;
      margin-bottom: 1.2rem;
    }

    .legal-hero h1 {
      font-size: clamp(2rem, 5vw, 3rem);
      font-weight: 800;
      color: #ffffff !important;
      line-height: 1.2;
      margin-bottom: 1rem;
    }

    .legal-hero p {
      color: rgba(255, 255, 255, 0.65) !important;
      font-size: 1rem;
      max-width: 560px;
    }

    .legal-meta {
      display: flex;
      gap: 2rem;
      margin-top: 1.5rem;
      flex-wrap: wrap;
    }

    .legal-meta-item {
      display: flex;
      align-items: center;
      gap: 0.5rem;
      color: rgba(255, 255, 255, 0.55) !important;
      font-size: 0.86rem;
    }

    .legal-meta-item span {
      color: rgba(255, 255, 255, 0.55) !important;
    }

    .legal-meta-item strong {
      color: rgba(255, 255, 255, 0.8) !important;
    }

    .legal-body {
      display: grid;
      grid-template-columns: 260px 1fr;
      gap: 3rem;
      align-items: start;
      padding: 4rem 0 6rem;
    }

    @media (max-width: 900px) {
      .legal-body {
        grid-template-columns: 1fr;
      }

      .legal-toc {
        display: none;
      }
    }

    .legal-toc {
      position: sticky;
      top: 90px;
      background: #111a2e;
      border: 1px solid rgba(255, 255, 255, 0.1);
      border: 1px solid rgba(8, 68, 129, 0.12);
      border-radius: 16px;
      padding: 1.5rem;
      box-shadow: 0 8px 32px rgba(0, 0, 0, 0.06);
    }

    .legal-toc h3 {
      font-size: 0.78rem;
      font-weight: 700;
      text-transform: uppercase;
      letter-spacing: 0.08em;
      color: var(--orange) !important;
      margin-bottom: 1rem;
    }

    .legal-toc ol {
      list-style: none;
      padding: 0;
      margin: 0;
      display: flex;
      flex-direction: column;
      gap: 0.4rem;
    }

    .legal-toc ol li a {
      display: block;
      padding: 0.45rem 0.75rem;
      color: #ffffff !important;
      font-size: 0.86rem;
      font-weight: 500;
      text-decoration: none;
      border-radius: 8px;
      transition: all 0.2s;
      line-height: 1.4;
    }

    .legal-toc ol li a:hover {
      background: rgba(8, 68, 129, 0.07);
      color: var(--orange) !important;
    }

    .legal-content {
      max-width: 760px;
    }

    .legal-section {
      margin-bottom: 3rem;
      padding-bottom: 3rem;
      border-bottom: 1px solid rgba(255, 255, 255, 0.1);
    }

    .legal-section:last-child {
      border-bottom: none;
      margin-bottom: 0;
    }

    .legal-section h2 {
      font-size: 1.4rem;
      font-weight: 800;
      color: #ffffff !important;
      margin-bottom: 1rem;
      display: flex;
      align-items: center;
      gap: 0.75rem;
    }

    .legal-section h2 .sec-num {
      display: inline-flex;
      align-items: center;
      justify-content: center;
      width: 32px;
      height: 32px;
      background: rgba(8, 68, 129, 0.10);
      border: 1px solid rgba(8, 68, 129, 0.20);
      border-radius: 8px;
      color: var(--orange) !important;
      font-size: 0.82rem;
      font-weight: 800;
      flex-shrink: 0;
    }

    .legal-section p {
      color: rgba(255, 255, 255, 0.7) !important;
      font-size: 0.97rem;
      line-height: 1.8;
      margin-bottom: 1rem;
    }

    .legal-section p:last-child {
      margin-bottom: 0;
    }

    .legal-section ul,
    .legal-section ol {
      padding-left: 1.5rem;
      margin: 0.75rem 0 1rem;
      display: flex;
      flex-direction: column;
      gap: 0.5rem;
    }

    .legal-section ul li,
    .legal-section ol li {
      color: rgba(255, 255, 255, 0.7) !important;
      font-size: 0.97rem;
      line-height: 1.7;
    }

    .legal-section ul li::marker {
      color: var(--orange);
    }

    .legal-section ol li::marker {
      color: var(--orange);
      font-weight: 700;
    }

    .legal-section h3 {
      font-size: 1.05rem;
      font-weight: 700;
      color: #ffffff !important;
      margin: 1.5rem 0 0.5rem;
    }

    .legal-highlight {
      background: rgba(8, 68, 129, 0.1);
      border: 1px solid rgba(8, 68, 129, 0.14);
      border-left: 3px solid var(--orange);
      border-radius: 0 10px 10px 0;
      padding: 1rem 1.25rem;
      margin: 1.25rem 0;
    }

    .legal-highlight p {
      color: #ffffff !important;
      font-size: 0.93rem;
      margin: 0;
    }

    .legal-warning {
      background: rgba(239, 68, 68, 0.05);
      border: 1px solid rgba(239, 68, 68, 0.18);
      border-left: 3px solid #ef4444;
      border-radius: 0 10px 10px 0;
      padding: 1rem 1.25rem;
      margin: 1.25rem 0;
    }

    .legal-warning p {
      color: #7f1d1d !important;
      font-size: 0.93rem;
      margin: 0;
    }

    .legal-contact-card {
      background: #111114;
      border-radius: 16px;
      padding: 2rem;
      margin-top: 1.5rem;
    }

    .legal-contact-card h3 {
      color: #ffffff !important;
      margin-bottom: 0.5rem;
    }

    .legal-contact-card p {
      color: rgba(255, 255, 255, 0.65) !important;
      margin-bottom: 0.4rem;
      font-size: 0.93rem;
    }

    .legal-contact-card a {
      color: var(--orange) !important;
      font-weight: 600;
      text-decoration: none;
    }

    .legal-contact-card a:hover {
      text-decoration: underline;
    }
  </style>

  <!-- Theme init: runs before paint to prevent flash -->
  <script>
    (function () {
      var t = localStorage.getItem('vt-theme');
      if (t === 'light') document.documentElement.setAttribute('data-theme', 'light');
    })();
  </script>
</head>

<body>
"""

pristine_middle = """
  <!-- Hero -->
  <section class="hero legal-hero">
    <div class="container">
      <div class="legal-hero-inner">
        <div class="hero-badge">Legal</div>
        <h1>Terms of Service</h1>
        <p>Please read these terms carefully before using our website or engaging Vedtam Tech Solutions for any IT,
          cybersecurity, or consulting services.</p>
        <div class="legal-meta">
          <div class="legal-meta-item">
            <span>Effective Date:</span>
            <strong>1 January 2025</strong>
          </div>
          <div class="legal-meta-item">
            <span>Last Updated:</span>
            <strong>22 April 2026</strong>
          </div>
          <div class="legal-meta-item">
            <span>Governing Law:</span>
            <strong>India (IT Act 2000)</strong>
          </div>
        </div>
      </div>
    </div>
  </section>
"""

# Now we need the rest of the terms-of-service file. We'll extract it from the currently broken file.
body_start = tos_content.find("<!-- Body -->")
if body_start == -1:
    body_start = tos_content.find('<div class="legal-body">')
    # Backup a bit if we can't find <!-- Body -->
    
pristine_bottom = tos_content[body_start:]

full_html = pristine_top + nav_html + "\n\n" + mob_html + "\n" + pristine_middle + "\n  <!-- Body -->\n  <div class=" + pristine_bottom.split('<div class="', 1)[-1] if '<!-- Body -->' not in pristine_bottom else pristine_bottom

with open('terms-of-service.html', 'w', encoding='utf-8') as f:
    f.write(full_html)
