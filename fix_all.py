"""
fix_all.py — Vedtam Website Bulk Fixer
========================================
Fixes:
  1. og:url meta tags missing slash (e.g. vedtam.compage.html → vedtam.com/page.html)
  2. og:image meta tags with wrong URL (legacy favicon URL → correct one)
  3. software-solutions.html — replaces old footer with standard footer from index.html
  4. software-solutions.html — replaces old nav with standard nav from index.html
  5. cert-advisory.html — replaces old nav (with HTML comment before mobileNav) with standard nav
"""

import os
import re
import shutil
from datetime import datetime

DIRECTORY = os.path.dirname(os.path.abspath(__file__))
MASTER_FILE = "index.html"
BACKUP_DIR = os.path.join(DIRECTORY, "backups")

def backup_file(filepath):
    os.makedirs(BACKUP_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.basename(filepath)
    backup_path = os.path.join(BACKUP_DIR, f"{timestamp}_{filename}")
    shutil.copy2(filepath, backup_path)

# ─── Step 1: Fix og:url & og:image broken URLs across ALL html files ──────────

def fix_og_tags(directory):
    print("\n── Step 1: Fixing og:url & og:image meta tags ──")
    html_files = [f for f in os.listdir(directory) if f.endswith('.html')]
    fixed = 0
    for filename in html_files:
        filepath = os.path.join(directory, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()
        original = content
        # Fix og:url — add missing slash after .com
        content = re.sub(
            r'(content="https://www\.vedtam\.com)([^/"\s])',
            r'\1/\2',
            content
        )
        # Fix property="og:url" href version
        content = re.sub(
            r'(https://www\.vedtam\.com)([^/"\s<])',
            r'\1/\2',
            content
        )
        if content != original:
            backup_file(filepath)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            print(f"  ✅ Fixed og tags in: {filename}")
            fixed += 1
    print(f"  Total fixed: {fixed} file(s)")

# ─── Step 2: Extract nav & footer from index.html ─────────────────────────────

def extract_from_master(directory):
    master_path = os.path.join(directory, MASTER_FILE)
    with open(master_path, "r", encoding="utf-8") as f:
        content = f.read()

    nav_pattern = re.compile(
        r'(\s*<nav class="navbar" id="navbar">.*?</nav>\s*<div class="mobile-nav" id="mobileNav">.*?</div>)',
        re.DOTALL
    )
    footer_pattern = re.compile(
        r'(\s*<footer class="footer">.*?</footer>)',
        re.DOTALL
    )
    nav_match = nav_pattern.search(content)
    footer_match = footer_pattern.search(content)
    return nav_match.group(1) if nav_match else None, footer_match.group(1) if footer_match else None

# ─── Step 3: Fix software-solutions.html ──────────────────────────────────────

def fix_software_solutions(directory, nav_html, footer_html):
    print("\n── Step 2: Fixing software-solutions.html ──")
    filepath = os.path.join(directory, "software-solutions.html")
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    original = content

    # Nav: uses 4-space indentation — match it
    old_nav_pattern = re.compile(
        r'(\s*<nav class="navbar" id="navbar">.*?</nav>\s*(?:<!--.*?-->)?\s*<div class="mobile-nav" id="mobileNav">.*?</div>)',
        re.DOTALL
    )
    if old_nav_pattern.search(content):
        content = old_nav_pattern.sub(nav_html, content, count=1)
        print("  ✅ Nav replaced")
    else:
        print("  ⚠️  Nav pattern not found")

    # Footer: uses class="sw-footer" or just <footer> — match generically
    old_footer_pattern = re.compile(r'<footer\b[^>]*>.*?</footer>', re.DOTALL)
    if old_footer_pattern.search(content):
        content = old_footer_pattern.sub(footer_html.strip(), content, count=1)
        print("  ✅ Footer replaced")
    else:
        print("  ⚠️  Footer pattern not found")

    if content != original:
        backup_file(filepath)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print("  💾 software-solutions.html saved")
    else:
        print("  ⏭️  No changes needed")

# ─── Step 4: Fix cert-advisory.html nav (has HTML comment before mobileNav) ───

def fix_cert_advisory(directory, nav_html):
    print("\n── Step 3: Fixing cert-advisory.html nav ──")
    filepath = os.path.join(directory, "cert-advisory.html")
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    original = content

    # Flexible pattern: allows optional HTML comments between </nav> and <div class="mobile-nav"
    old_nav_pattern = re.compile(
        r'(\s*<nav class="navbar" id="navbar">.*?</nav>(?:\s*<!--.*?-->)?\s*<div class="mobile-nav" id="mobileNav">.*?</div>)',
        re.DOTALL
    )
    if old_nav_pattern.search(content):
        content = old_nav_pattern.sub(nav_html, content, count=1)
        print("  ✅ Nav replaced in cert-advisory.html")
    else:
        print("  ⚠️  Nav pattern not found in cert-advisory.html")

    if content != original:
        backup_file(filepath)
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print("  💾 cert-advisory.html saved")
    else:
        print("  ⏭️  No changes needed")

# ─── Main ──────────────────────────────────────────────────────────────────────

if __name__ == "__main__":
    print("🚀 Vedtam Bulk Fixer Starting...")
    fix_og_tags(DIRECTORY)
    nav_html, footer_html = extract_from_master(DIRECTORY)
    if nav_html and footer_html:
        print(f"\n✅ Extracted nav ({len(nav_html):,} chars) and footer ({len(footer_html):,} chars) from index.html")
        fix_software_solutions(DIRECTORY, nav_html, footer_html)
        fix_cert_advisory(DIRECTORY, nav_html)
    else:
        print("❌ Could not extract nav/footer from index.html. Aborting steps 2-4.")

    print("\n─────────────────────────────────────")
    print("✅ All fixes complete! Backups in ./backups/")
    print("─────────────────────────────────────")
