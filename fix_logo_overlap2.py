import os
import re

directory = r"c:\Users\Manu\Desktop\vedtam website"
html_files = [f for f in os.listdir(directory) if f.endswith('.html')]

# We want to replace these specific <img> tags inside nav-logo
# English logo:
old_en_nav = r'<img src="website-logo/VEDTAM%20TECH%20SOLUTIONS%20en.png" alt="Vedtam Tech Solutions logo English"\s*class="logo-en" decoding="async">'
new_en_nav = r'<img src="website-logo/VEDTAM%20TECH%20SOLUTIONS%20en.png" alt="Vedtam Tech Solutions logo English"\n          class="logo-en" decoding="async" style="position: relative;">'

old_hi_nav = r'<img src="website-logo/VEDTAM%20TECH%20SOLUTIONS%20hn.png" alt="Vedtam Tech Solutions logo Hindi"\s*class="logo-hi" decoding="async">'
new_hi_nav = r'<img src="website-logo/VEDTAM%20TECH%20SOLUTIONS%20hn.png" alt="Vedtam Tech Solutions logo Hindi"\n          class="logo-hi" decoding="async" style="opacity: 0; position: absolute;">'

# Footer logo (single image to dual image)
old_footer = r'<a href="index\.html" class="nav-logo footer-logo" aria-label="Vedtam Tech Solutions">\s*<img src="website-logo/VEDTAM%20TECH%20SOLUTIONS%20en\.png" alt="Vedtam Tech Solutions logo"([^>]+)>\s*</a>'
new_footer = r'''<a href="index.html" class="nav-logo footer-logo" aria-label="Vedtam Tech Solutions">
            <img src="website-logo/VEDTAM%20TECH%20SOLUTIONS%20en.png" alt="Vedtam Tech Solutions logo English"
              class="logo-en" decoding="async" style="position: relative;">
            <img src="website-logo/VEDTAM%20TECH%20SOLUTIONS%20hn.png" alt="Vedtam Tech Solutions logo Hindi"
              class="logo-hi" decoding="async" style="opacity: 0; position: absolute;">
          </a>'''

count = 0
for filename in html_files:
    if filename in ["index.html", "about-us.html", "cyber-security-services.html"]:
        continue
        
    filepath = os.path.join(directory, filename)
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
    
    original = content
    
    # Nav Logo Replace
    content = re.sub(old_en_nav, new_en_nav, content)
    content = re.sub(old_hi_nav, new_hi_nav, content)
    
    # Footer Logo Replace
    content = re.sub(old_footer, new_footer, content)
    
    if content != original:
        with open(filepath, "w", encoding="utf-8") as f:
            f.write(content)
        print(f"Fixed {filename}")
        count += 1

print(f"Fixed logo overlap in {count} files.")
