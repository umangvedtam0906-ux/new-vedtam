#!/usr/bin/env python3
import os
import re
from html.parser import HTMLParser
from urllib.parse import urlparse, urljoin, unquote

# Config
BASE_DOMAIN = "vedtam.com"
WORKSPACE_DIR = os.path.dirname(os.path.abspath(__file__))

class LinkExtractor(HTMLParser):
    def __init__(self):
        super().__init__()
        self.links = []

    def handle_starttag(self, tag, attrs):
        attrs_dict = dict(attrs)
        if tag == 'a' and 'href' in attrs_dict:
            self.links.append(('href', attrs_dict['href']))
        elif tag in ['img', 'script'] and 'src' in attrs_dict:
            self.links.append(('src', attrs_dict['src']))
        elif tag == 'link' and 'href' in attrs_dict:
            self.links.append(('href', attrs_dict['href']))

def get_html_files():
    html_files = []
    for root, dirs, files in os.walk(WORKSPACE_DIR):
        # Skip some folders
        if '.git' in root or 'scratch_coverage' in root or '__pycache__' in root or 'backups' in root:
            continue
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
    return html_files

def is_internal(url):
    if not url:
        return False
    # Ignore email, phone, fragment-only links
    if url.startswith(('mailto:', 'tel:', '#', 'javascript:')):
        return False
    parsed = urlparse(url)
    if parsed.scheme and parsed.scheme not in ['http', 'https']:
        return False
    if not parsed.netloc:
        return True
    return BASE_DOMAIN in parsed.netloc

def resolve_to_local_path(link, current_file_path):
    parsed = urlparse(link)
    path = unquote(parsed.path)
    if not path:
        return None

    # Handle absolute paths vs relative paths
    if path.startswith('/'):
        # Relative to workspace root
        target_path = os.path.join(WORKSPACE_DIR, path.lstrip('/'))
    else:
        # Relative to current file's directory
        current_dir = os.path.dirname(current_file_path)
        target_path = os.path.join(current_dir, path)

    target_path = os.path.normpath(target_path)
    return target_path

def verify_path_exists(target_path):
    if not target_path:
        return False

    # 1. Direct match
    if os.path.exists(target_path):
        return True

    # 2. If it's a directory, check for index.html inside it
    if os.path.isdir(target_path):
        if os.path.exists(os.path.join(target_path, 'index.html')):
            return True

    # 3. If it doesn't have an extension, try appending .html (due to .htaccess)
    if not os.path.splitext(target_path)[1]:
        if os.path.exists(target_path + '.html'):
            return True
        # Try checking if it's a directory with index.html
        if os.path.exists(os.path.join(target_path, 'index.html')):
            return True

    return False

def main():
    html_files = get_html_files()
    print(f"Scanning {len(html_files)} HTML files for broken links...\n")

    broken_links_count = 0
    checked_links_count = 0

    for file_path in sorted(html_files):
        rel_file_path = os.path.relpath(file_path, WORKSPACE_DIR)
        
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
        except Exception as e:
            print(f"Error reading {rel_file_path}: {e}")
            continue

        parser = LinkExtractor()
        parser.feed(content)

        file_broken_links = []

        for attr_type, link in parser.links:
            if not is_internal(link):
                continue
            
            checked_links_count += 1
            local_path = resolve_to_local_path(link, file_path)
            
            if local_path and not verify_path_exists(local_path):
                file_broken_links.append((link, local_path))

        if file_broken_links:
            print(f"[BROKEN] {rel_file_path}:")
            for link, resolved in file_broken_links:
                print(f"   - Broken Link: {link}")
                print(f"     Resolved Path: {os.path.relpath(resolved, WORKSPACE_DIR)}")
                broken_links_count += 1
            print()

    print(f"Scan complete. Checked {checked_links_count} links. Found {broken_links_count} broken links.")

if __name__ == "__main__":
    main()
