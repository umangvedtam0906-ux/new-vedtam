import os
import re

css_file = "vedtam.css"
backup_file = "vedtam.css.backup"

if not os.path.exists(css_file):
    print(f"Error: {css_file} not found!")
    exit(1)

# Create a backup just in case
with open(css_file, "r", encoding="utf-8") as f:
    css_content = f.read()

with open(backup_file, "w", encoding="utf-8") as f:
    f.write(css_content)
print(f"Created backup at {backup_file}")

# Minification Process
original_size = len(css_content)

# 1. Remove comments
css_content = re.sub(r'/\*.*?\*/', '', css_content, flags=re.DOTALL)

# 2. Remove newlines and tabs
css_content = css_content.replace('\n', '').replace('\r', '').replace('\t', '')

# 3. Remove multiple spaces
css_content = re.sub(r'\s+', ' ', css_content)

# 4. Remove spaces around special characters
css_content = re.sub(r'\s*([\{\}\:\;\,\>])\s*', r'\1', css_content)

minified_size = len(css_content)
savings = original_size - minified_size
percentage = (savings / original_size) * 100 if original_size > 0 else 0

# Write back to vedtam.css
with open(css_file, "w", encoding="utf-8") as f:
    f.write(css_content)

print(f"Minification Complete!")
print(f"Original Size: {original_size / 1024:.2f} KB")
print(f"Minified Size: {minified_size / 1024:.2f} KB")
print(f"Space Saved: {savings / 1024:.2f} KB ({percentage:.2f}%)")
