import os
import re

files = [f for f in os.listdir('.') if f.endswith('.html')]

patterns_to_remove = [
    # Desktop and Mobile link
    r'<a href="Hardware\.html">Hardware Solutions</a>',
    # Footer list item
    r'<li><a href="Hardware\.html">Hardware Solutions</a></li>',
    # Sometimes there's a space or slightly different attribute order
    r'<a href="Hardware\.html"[^>]*>Hardware Solutions</a>',
    r'<li><a href="Hardware\.html"[^>]*>Hardware Solutions</a></li>'
]

for filename in files:
    with open(filename, 'r', encoding='utf-8') as f:
        content = f.read()
    
    new_content = content
    for pattern in patterns_to_remove:
        # We also want to remove potential surrounding whitespace if it leaves a blank line
        new_content = re.sub(r'^\s*' + pattern + r'\s*$', '', new_content, flags=re.MULTILINE)
        new_content = re.sub(pattern, '', new_content)
    
    if new_content != content:
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(new_content)
        print(f"Updated {filename}")
    else:
        print(f"No changes for {filename}")
