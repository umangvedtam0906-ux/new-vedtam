#!/usr/bin/env python3
import os
import re

WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))

def fix_sitemap_html_links():
    # 1. Update sitemap.html links in subdirectories
    subdirs = ["solutions", "consulting", "blog"]
    for subdir in subdirs:
        subdir_path = os.path.join(WORKSPACE_DIR, subdir)
        if not os.path.exists(subdir_path):
            continue
        for file in os.listdir(subdir_path):
            if file.endswith(".html"):
                filepath = os.path.join(subdir_path, file)
                with open(filepath, "r", encoding="utf-8") as f:
                    content = f.read()

                # Replace <a href="sitemap.html">Sitemap</a> with <a href="../sitemap.html">Sitemap</a>
                if 'href="sitemap.html"' in content:
                    content = content.replace('href="sitemap.html"', 'href="../sitemap.html"')
                    with open(filepath, "w", encoding="utf-8") as f:
                        f.write(content)
                    print(f"Fixed sitemap.html link in {subdir}/{file}")

def fix_solutions_index_html():
    # 2. Fix broken links in solutions/index.html
    filepath = os.path.join(WORKSPACE_DIR, "solutions", "index.html")
    if os.path.exists(filepath):
        with open(filepath, "r", encoding="utf-8") as f:
            content = f.read()

        # Fix consulting.html -> ../consulting.html
        content = content.replace('href="consulting.html"', 'href="../consulting.html"')
        # Fix website-logo/ -> ../website-logo/
        content = content.replace('src="website-logo/VEDTAM%20TECH%20SOLUTIONS%20en.png"', 'src="../website-logo/VEDTAM%20TECH%20SOLUTIONS%20en.png"')
        # Fix sitemap.html -> ../sitemap.html
        content = content.replace('href="sitemap.html"', 'href="../sitemap.html"')

        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print("Fixed broken links in solutions/index.html")

def fix_canonical_typos():
    # 3. Fix canonical and og:url typos in specific blog posts
    pci_blog = os.path.join(WORKSPACE_DIR, "blog", "pci-dss-v4.0.html")
    if os.path.exists(pci_blog):
        with open(pci_blog, "r", encoding="utf-8") as f:
            content = f.read()
        content = content.replace('https://vedtam.com/blog/pci-dss-v4-changes-compliance', 'https://vedtam.com/blog/pci-dss-v4.0')
        with open(pci_blog, "w", encoding="utf-8") as f:
            f.write(content)
        print("Fixed canonical and og:url in blog/pci-dss-v4.0.html")

    vciso_blog = os.path.join(WORKSPACE_DIR, "blog", "virtual-ciso-services.html")
    if os.path.exists(vciso_blog):
        with open(vciso_blog, "r", encoding="utf-8") as f:
            content = f.read()
        content = content.replace('https://vedtam.com/blog/virtual-ciso-services-india', 'https://vedtam.com/blog/virtual-ciso-services')
        with open(vciso_blog, "w", encoding="utf-8") as f:
            f.write(content)
        print("Fixed canonical and og:url in blog/virtual-ciso-services.html")

def update_generate_sitemap_py():
    # 4. Update generate_sitemap.py to dynamically handle relative pathing for terms-of-service.html
    script_path = os.path.join(WORKSPACE_DIR, "generate_sitemap.py")
    if os.path.exists(script_path):
        with open(script_path, "r", encoding="utf-8") as f:
            content = f.read()

        # Target content
        target = '''                    if 'sitemap.html' not in content and 'Terms of Service</a>' in content:
                        # Depending on the level of indentation in different files, use a regex
                        content = re.sub(
                            r'(<a href="[./]*terms-of-service\\.html">Terms of Service</a>)',
                            r'\\1\\n          <a href="sitemap.html">Sitemap</a>',
                            content
                        )
                        changed = True'''

        # Replacement content
        replacement = '''                    if 'sitemap.html' not in content and 'Terms of Service</a>' in content:
                        # Depending on the level of indentation in different files, use a regex
                        content = re.sub(
                            r'(<a href="([./]*)terms-of-service\\.html">Terms of Service</a>)',
                            r'\\1\\n          <a href="\\2sitemap.html">Sitemap</a>',
                            content
                        )
                        changed = True'''

        if target in content:
            content = content.replace(target, replacement)
            with open(script_path, "w", encoding="utf-8") as f:
                f.write(content)
            print("Updated generate_sitemap.py script")
        else:
            print("Could not find the target code in generate_sitemap.py. Checking if it's already updated.")

if __name__ == "__main__":
    fix_sitemap_html_links()
    fix_solutions_index_html()
    fix_canonical_typos()
    update_generate_sitemap_py()
