import os
import re

directory = r"c:\Users\Manu\Desktop\vedtam website"

# 1. Read index.html to extract the latest header and footer
with open(os.path.join(directory, "index.html"), "r", encoding="utf-8") as f:
    index_content = f.read()

# Extract header (from <nav class="navbar" id="navbar"> to end of <div class="mobile-nav" id="mobileNav">...</div>)
header_pattern = re.compile(r'(<nav class="navbar" id="navbar">.*?</nav>\s*<div class="mobile-nav" id="mobileNav">.*?</div>)', re.DOTALL)
header_match = header_pattern.search(index_content)
if not header_match:
    print("Could not find header in index.html")
    exit(1)
header_html = header_match.group(1)

# Extract footer
footer_pattern = re.compile(r'(<footer class="footer">.*?</footer>)', re.DOTALL)
footer_match = footer_pattern.search(index_content)
if not footer_match:
    print("Could not find footer in index.html")
    exit(1)
footer_html = footer_match.group(1)

print(f"Extracted header length: {len(header_html)}")
print(f"Extracted footer length: {len(footer_html)}")

# 2. Iterate through all html files and update them
html_files = [f for f in os.listdir(directory) if f.endswith('.html')]

count = 0
for filename in html_files:
    if filename == "index.html":
        continue
    
    filepath = os.path.join(directory, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    original_content = content
    
    # Replace header
    # old header might be <nav class="navbar"... or <header id="header"...
    old_nav_pattern = re.compile(r'<nav class="navbar" id="navbar">.*?</nav>\s*<div class="mobile-nav" id="mobileNav">.*?</div>', re.DOTALL)
    old_header_pattern = re.compile(r'<header id="header".*?</header>', re.DOTALL)
    
    if old_nav_pattern.search(content):
        content = old_nav_pattern.sub(header_html.replace('\\', '\\\\'), content, count=1)
    elif old_header_pattern.search(content):
        content = old_header_pattern.sub(header_html.replace('\\', '\\\\'), content, count=1)
        
    # Replace footer
    old_footer_pattern = re.compile(r'<footer.*?</footer>', re.DOTALL)
    if old_footer_pattern.search(content):
        content = old_footer_pattern.sub(footer_html.replace('\\', '\\\\'), content, count=1)
        
    if content != original_content:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Updated {filename}")
        count += 1

print(f"Successfully updated {count} files.")
