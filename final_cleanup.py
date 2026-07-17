import os
import re

files = [f for f in os.listdir('.') if f.endswith('.html') or f.endswith('.css') or f.endswith('.js')]

patterns_to_remove = [
    r'<li><a href="Hardware\.html"> Hardware Solutions</a></li>',
    r'<li><a href="Hardware\.html">Hardware Solutions</a></li>',
    r'<a href="Hardware\.html">Hardware Solutions</a>',
    r'<a href="Hardware\.html">Hardware Services</a>',
    r'\.hardware-hero\s*,\s*', # Removing from comma separated lists in CSS
    r',\s*\.hardware-hero',
    r'\.hardware-hero\s*{[^}]*}', # Removing individual CSS blocks
]

for filename in files:
    if filename == 'remove_hardware.py' or filename == 'update_links.py':
        continue
        
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = content
    for pattern in patterns_to_remove:
        new_content = re.sub(pattern, '', new_content)
    
    if new_content != content:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filename}")
    else:
        print(f"No changes for {filename}")
