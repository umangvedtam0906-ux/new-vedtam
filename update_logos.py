import os
import re

dir_path = r"c:\Users\Manu\Downloads\new-vedtam-main (3)\new-vedtam-main"

pattern = re.compile(
    r'(<a[^>]*class="[^"]*nav-logo[^"]*"[^>]*>)\s*<img[^>]*class="logo-en"[^>]*src="([^"]*?)website-logo/VEDTAM%20TECH%20SOLUTIONS%20en\.png"[^>]*>\s*<img[^>]*class="logo-hi"[^>]*src="([^"]*?)website-logo/VEDTAM%20TECH%20SOLUTIONS%20hn\.png"[^>]*>\s*</a>',
    re.DOTALL | re.IGNORECASE
)

count = 0
for root, dirs, files in os.walk(dir_path):
    for file in files:
        if file.endswith('.html'):
            filepath = os.path.join(root, file)
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
            
            def replacer(match):
                a_tag = match.group(1)
                prefix = match.group(2)
                
                new_content = f"""{a_tag}
        <img alt="Vedtam Tech Solutions logo" decoding="async"
          src="{prefix}website-logo/VEDTAM%20TECH%20SOLUTIONS%20en.png" 
          data-logo-switcher 
          data-logos="{prefix}website-logo/VEDTAM%20TECH%20SOLUTIONS%20en.png, {prefix}website-logo/VEDTAM%20TECH%20SOLUTIONS%20hn.png" />
      </a>"""
                return new_content
            
            new_content, num_replacements = pattern.subn(replacer, content)
            if num_replacements > 0:
                count += num_replacements
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(new_content)

print(f"Replaced {count} instances of the old logo tags.")
