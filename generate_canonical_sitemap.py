#!/usr/bin/env python3
import os
from datetime import datetime

BASE_URL = "https://vedtam.com"

# Root HTML files that are part of the site
ROOT_PAGES = [
    ("index.html", "/", "weekly", "1.0"),
    ("about-us.html", "/about-us", "monthly", "0.8"),
    ("contact-us.html", "/contact-us", "monthly", "0.9"),
    ("careers.html", "/careers", "monthly", "0.8"),
    ("cert-advisory.html", "/cert-advisory", "daily", "0.8"),
    ("client-success-portfolio.html", "/client-success-portfolio", "monthly", "0.7"),
    ("solutions.html", "/solutions", "monthly", "0.9"),
    ("why-us.html", "/why-us", "monthly", "0.8"),
    ("privacy-policy.html", "/privacy-policy", "yearly", "0.3"),
    ("terms-of-service.html", "/terms-of-service", "yearly", "0.3")
]

# Folders to scan dynamically
FOLDERS_TO_SCAN = [
    ("solutions", "solutions", "monthly", "0.8"),
    ("consulting", "consulting", "monthly", "0.8"),
    ("blog", "blog", "weekly", "0.7")
]

def get_lastmod(filepath):
    try:
        mtime = os.path.getmtime(filepath)
        return datetime.fromtimestamp(mtime).strftime('%Y-%m-%d')
    except Exception:
        return datetime.now().strftime('%Y-%m-%d')

def main():
    urls = []

    # 1. Add root pages
    for filename, route, changefreq, priority in ROOT_PAGES:
        if os.path.exists(filename):
            lastmod = get_lastmod(filename)
            urls.append((f"{BASE_URL}{route}", lastmod, changefreq, priority))

    # 2. Scan folders
    for folder, route_prefix, changefreq, priority in FOLDERS_TO_SCAN:
        if os.path.exists(folder) and os.path.isdir(folder):
            for file in sorted(os.listdir(folder)):
                if file.endswith(".html") and file != "index.html":
                    filepath = os.path.join(folder, file)
                    clean_name = file[:-5] # remove .html
                    loc = f"{BASE_URL}/{route_prefix}/{clean_name}"
                    lastmod = get_lastmod(filepath)
                    urls.append((loc, lastmod, changefreq, priority))

    # 3. Write XML sitemap
    xml_lines = [
        '<?xml version="1.0" encoding="UTF-8"?>',
        '<urlset xmlns="http://www.sitemaps.org/schemas/sitemap/0.9">'
    ]

    for loc, lastmod, changefreq, priority in urls:
        xml_lines.append("  <url>")
        xml_lines.append(f"    <loc>{loc}</loc>")
        xml_lines.append(f"    <lastmod>{lastmod}</lastmod>")
        xml_lines.append(f"    <changefreq>{changefreq}</changefreq>")
        xml_lines.append(f"    <priority>{priority}</priority>")
        xml_lines.append("  </url>")

    xml_lines.append("</urlset>")

    with open("sitemap.xml", "w", encoding="utf-8") as f:
        f.write("\n".join(xml_lines) + "\n")

    print(f"Generated sitemap.xml with {len(urls)} URLs successfully.")

if __name__ == "__main__":
    main()
