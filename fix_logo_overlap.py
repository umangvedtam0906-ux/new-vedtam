import os
import re

def fix_logos(content):
    # Regex to find the nav-logo block
    # It might span multiple lines
    # We will specifically target the .logo-hi image tag and add opacity:0
    # First, let's inject styles into logo-hi
    # Match: class="logo-hi" or class="logo-hi" ...
    # We want to replace <img ... class="logo-hi" ...> with <img ... class="logo-hi" style="opacity: 0; position: absolute;" ...>
    
    # Simple replace:
    new_content = re.sub(
        r'(<img[^>]+class=["\'][^"\']*logo-hi[^"\']*["\'][^>]*?)>',
        r'\1 style="opacity: 0; position: absolute;">',
        content
    )
    
    # Just in case it already has a style attribute, we should be careful, but we know it likely doesn't based on our view.
    # We also want to ensure the English logo stays visible and relative
    new_content = re.sub(
        r'(<img[^>]+class=["\'][^"\']*logo-en[^"\']*["\'][^>]*?)>',
        r'\1 style="position: relative;">',
        new_content
    )
    
    return new_content

updated_files = 0
for filename in os.listdir('.'):
    if filename.endswith('.html'):
        with open(filename, 'r', encoding='utf-8') as f:
            content = f.read()
            
        new_content = fix_logos(content)
        
        # We only want to inject if it's not already injected
        if 'style="opacity: 0; position: absolute;"' not in content and new_content != content:
            with open(filename, 'w', encoding='utf-8') as f:
                f.write(new_content)
            updated_files += 1
            print(f"Updated {filename}")

print(f"Done! Updated {updated_files} files.")
