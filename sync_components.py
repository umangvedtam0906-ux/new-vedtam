"""
sync_components.py — Vedtam Website Component Sync Tool
=========================================================
PURPOSE:
  Syncs the shared <nav> (header) and <footer> from index.html to every
  other HTML page in this directory.

USAGE:
  1. Edit the navigation bar or footer in index.html (your "master" file).
  2. Double-click this file  —OR—  run: python sync_components.py
  3. Done! All other pages will be updated automatically.

SAFETY:
  - A timestamped backup of each modified file is created in ./backups/
  - index.html is never modified.
  - Only files in THIS directory (not subdirectories) are processed.
  - Script-only .html files like cookie-preferences.html can be excluded.
"""

import os
import re
import sys
import shutil
from datetime import datetime
from bs4 import BeautifulSoup

# Configure console encoding to handle emojis/unicode characters properly on Windows
if hasattr(sys.stdout, 'reconfigure'):
    try:
        sys.stdout.reconfigure(encoding='utf-8')
    except Exception:
        pass

# ─── Configuration ───────────────────────────────────────────────────────────

DIRECTORY = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = DIRECTORY # Explicitly set ROOT_DIR for clarity

MASTER_FILE = "index.html"
BACKUP_DIR = os.path.join(DIRECTORY, "backups")

# Pages to SKIP (will not have their nav/footer updated)
SKIP_FILES = {
    "index.html",
    "cookie-preferences.html",
}

# Define the new directory structure (needed for path mapping)
NEW_STRUCTURE = {
    "solutions": [
        "cyber-security-services.html",
        "network-security-solutions.html",
        "devops-solutions.html",
        "ot-security-services.html",
        "cloud-services.html",
        "it-managed-services.html",
        "software-solutions.html", # Will be renamed to software-services.html
    ],
    "consulting": [
        "virtual-ciso-services.html",
        "iso-consulting-services.html",
        "qms-consulting-services.html",
        "hipaa-consulting-services.html",
        "pci-dss-consulting-services.html",
        "gdpr-consulting-services.html",
        "soc-2-consulting-services.html", # Will be renamed to soc2-consulting-services.html
        "dpdp-act-consulting-services.html",
        "network-security-consulting-services.html",
        "network-security-audit-services.html",
    ],
    "blog": [
        "blog-data-protection-officer-dpdp-act.html",
        "blog-dpdp-act-penalties-non-compliance.html",
        "blog-dpdp-act-vs-gdpr-differences.html",
        "blog-iso-27001-certification-guide-india.html",
        "blog-iso-27001-vs-soc-2.html",
        "blog-zero-trust-cloud-architecture.html",
    ],
    "assets": {
        "css": [
            "vedtam.css",
            "dpdp-hero.css",
            "gdpr-hero.css",
            "hipaa-hero.css",
            "network-security.css",
            "pci-hero.css",
            "soc2-hero.css",
        ],
        "js": [
            "vedtam.js",
            "force-field.js",
            "gooey-gradient.js",
            "network-security-canvas.js",
        ],
        "videos": [
            "videos", # This is a directory
        ],
        "data": [
            "cert-data.json",
        ]
    }
}

# Mapping for renames (also needed for path mapping)
RENAMES = {
    "software-solutions.html": "software-services.html",
    "soc-2-consulting-services.html": "soc2-consulting-services.html",
}

# ─── Extraction Patterns ──────────────────────────────────────────────────────

def find_nav_block_span(content):
    """Finds the character indices of the complete navigation header block,
    from <nav class="navbar" id="navbar"> to the end of <div class="mobile-nav" id="mobileNav">,
    taking into account nested divs in the mobile dropdowns.
    """
    nav_match = re.search(r'<nav\s+class=["\']navbar["\']\s+id=["\']navbar["\']\s*>', content, re.IGNORECASE)
    if not nav_match:
        return None
    start_pos = nav_match.start()
    
    # Find </nav>
    nav_end = content.find('</nav>', nav_match.end())
    if nav_end == -1:
        return None
    nav_end += 6 # length of '</nav>'
    
    # Find start of <div class="mobile-nav" id="mobileNav">
    mobile_match = re.search(r'<div\s+class=["\']mobile-nav["\']\s+id=["\']mobileNav["\']\s*>', content[nav_end:], re.IGNORECASE)
    if not mobile_match:
        return None
    
    mobile_start = nav_end + mobile_match.start()
    
    # Find matching closing </div> by counting open/close tags
    pos = content.find('>', mobile_start) + 1
    depth = 1
    while depth > 0 and pos < len(content):
        next_open = content.find('<div', pos)
        next_close = content.find('</div>', pos)
        
        if next_close == -1:
            break
        if next_open != -1 and next_open < next_close:
            depth += 1
            pos = next_open + 4
        else:
            depth -= 1
            pos = next_close + 6
            if depth == 0:
                return (start_pos, pos)
                
    return None

# Captures: <footer class="footer"> ... </footer>
FOOTER_PATTERN = re.compile(
    r'(\s*<footer class="footer">.*?</footer>)',
    re.DOTALL
)


# ─── Helpers ──────────────────────────────────────────────────────────────────

def safe_sub(pattern, replacement, content):
    """Replace first match of pattern with replacement string (safely escaping backslashes)."""
    # re.sub uses backslashes specially in replacement — escape them
    safe_replacement = replacement.replace('\\', r'\\')
    return pattern.sub(safe_replacement, content, count=1)

def backup_file(filepath):
    """Create a timestamped backup of a file in ./backups/"""
    os.makedirs(BACKUP_DIR, exist_ok=True)
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = os.path.basename(filepath)
    backup_path = os.path.join(BACKUP_DIR, f"{timestamp}_{filename}")
    shutil.copy2(filepath, backup_path)

# Build a comprehensive mapping of old relative paths to new relative paths
def build_path_map():
    path_map = {}

    # HTML files
    for new_dir, files in NEW_STRUCTURE.items():
        if isinstance(files, list):
            for old_filename in files:
                new_filename = RENAMES.get(old_filename, old_filename)
                path_map[old_filename] = os.path.join(new_dir, new_filename).replace('\\', '/')

    # Asset files/directories
    for asset_type, items in NEW_STRUCTURE["assets"].items():
        for item_name in items:
            # For directories, we map the directory name itself.
            # For files, we map the file name.
            path_map[item_name] = os.path.join("assets", asset_type, item_name).replace('\\', '/')

    # Add root level files that don't move but might link to moved files
    root_html_files = ["index.html", "about-us.html", "contact-us.html", "client-success-portfolio.html", "privacy-policy.html", "terms-of-service.html", "cert-advisory.html", "blog.html"]
    for filename in root_html_files:
        path_map[filename] = filename # They stay in the root

    return path_map

def adjust_links_in_snippet(html_snippet, target_filepath, root_dir, path_map):
    """
    Adjusts relative links within an HTML snippet to be correct relative to the target_filepath.
    """
    soup = BeautifulSoup(html_snippet, "html.parser")
    
    for tag in soup.find_all(['a', 'link', 'script', 'img', 'source']):
        for attr in ['href', 'src']:
            if tag.has_attr(attr):
                old_relative_path = tag[attr]

                # Skip external links, anchors, absolute paths, and custom protocols
                if old_relative_path.startswith(('http', '#', '/', 'data:', 'mailto:', 'tel:', 'javascript:')):
                    continue

                # Normalize path for consistent lookup
                normalized_old_path = old_relative_path.replace('\\', '/')
                
                new_root_relative_path = None

                # Try to find the new root-relative path for the target of the link
                # This logic is adapted from restructure_website.py's link updating
                for new_top_dir, contents in NEW_STRUCTURE.items():
                    if isinstance(contents, dict): # Assets
                        for sub_dir, items in contents.items():
                            for item_name in items:
                                if normalized_old_path.startswith(item_name + '/') or normalized_old_path == item_name: # Handle files within moved dirs or direct file matches
                                    new_root_relative_path = os.path.join(new_top_dir, sub_dir, normalized_old_path).replace('\\', '/')
                                    break
                            if new_root_relative_path: break
                    elif isinstance(contents, list): # HTML files
                        if normalized_old_path in contents or RENAMES.get(normalized_old_path) in contents:
                            new_root_relative_path = os.path.join(new_top_dir, RENAMES.get(normalized_old_path, normalized_old_path)).replace('\\', '/')
                            break
                
                if not new_root_relative_path:
                    # Fallback: if the link is not moving, its root-relative path is the old path
                    new_root_relative_path = normalized_old_path

                if new_root_relative_path:
                    final_relative_path = os.path.relpath(os.path.join(root_dir, new_root_relative_path), os.path.dirname(target_filepath)).replace('\\', '/')
                    tag[attr] = final_relative_path

    return str(soup)

# ─── Main Logic ───────────────────────────────────────────────────────────────

def main():
    master_path = os.path.join(DIRECTORY, MASTER_FILE)

    # 1. Read master file
    print(f"📖 Reading master file: {MASTER_FILE}")
    with open(master_path, "r", encoding="utf-8") as f:
        master_content = f.read()

    # 2. Extract nav and footer from master
    nav_span = find_nav_block_span(master_content)
    footer_match = FOOTER_PATTERN.search(master_content)

    if not nav_span:
        print("❌ ERROR: Could not find <nav class=\"navbar\" id=\"navbar\"> and <div class=\"mobile-nav\"> in index.html. Aborting.")
        return
    if not footer_match:
        print("❌ ERROR: Could not find <footer class=\"footer\"> in index.html. Aborting.")
        return

    nav_html = master_content[nav_span[0]:nav_span[1]]
    footer_html = footer_match.group(1)

    print(f"✅ Extracted nav block    ({len(nav_html):,} chars)")
    print(f"✅ Extracted footer block ({len(footer_html):,} chars)")
    print()

    # Build the path map once
    path_map = build_path_map()

    # 3. Process all HTML files in the directory
    html_files = sorted([ # Use ROOT_DIR instead of DIRECTORY for consistency
        f for f in os.listdir(ROOT_DIR)
        if f.endswith('.html') and f not in SKIP_FILES
    ])

    updated = 0
    skipped = 0
    no_match = []

    for filename in html_files:
        filepath = os.path.join(ROOT_DIR, filename)
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        original = content
        nav_updated = False
        footer_updated = False

        # Replace nav block
        target_nav_span = find_nav_block_span(content)
        if target_nav_span:
            adjusted_nav_html = adjust_links_in_snippet(nav_html, filepath, ROOT_DIR, path_map)
            content = content[:target_nav_span[0]] + adjusted_nav_html + content[target_nav_span[1]:]
            nav_updated = True

        # Replace footer block
        if FOOTER_PATTERN.search(content):
            adjusted_footer_html = adjust_links_in_snippet(footer_html, filepath, ROOT_DIR, path_map)
            content = safe_sub(FOOTER_PATTERN, adjusted_footer_html, content)
            footer_updated = True

        if content != original:
            # Backup then write
            backup_file(filepath)
            with open(filepath, "w", encoding="utf-8") as f:
                f.write(content)
            nav_status = "✅ nav" if nav_updated else "⚠️  nav(no match)"
            ftr_status = "✅ footer" if footer_updated else "⚠️  footer(no match)"
            print(f"  [{nav_status}] [{ftr_status}]  →  {filename}")
            updated += 1
        else:
            if not nav_updated or not footer_updated:

                no_match.append(filename)
            else:
                skipped += 1

    # 4. Summary
    print()
    print("─" * 55)
    print(f"✅ Updated:  {updated} file(s)")
    print(f"⏭️  Unchanged: {skipped} file(s)  (already up-to-date)")
    if no_match:
        print(f"⚠️  No nav/footer pattern found in: {', '.join(no_match)}")
    print(f"💾 Backups saved to: ./backups/")
    print("─" * 55)

if __name__ == "__main__":
    main()
