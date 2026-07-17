import re

with open('vedtam.css', 'r', encoding='utf-8') as f:
    content = f.read()

# regex to find .hero-shell or anything ending in .hero-shell and its block
# and replace align-items: center with align-items: flex-start
# and ensure gap is at least 4rem or 5rem

# Function to replace properties inside a CSS block
def update_block(match):
    block = match.group(0)
    # Replace align-items
    block = re.sub(r'align-items:\s*center\b', 'align-items: flex-start', block)
    
    # Check if there's a gap. If gap is small, increase it
    # Just to be safe, replace gap: 2rem or 3rem or 3.5rem with gap: 4rem
    block = re.sub(r'gap:\s*(?:[1-3](?:\.\d+)?rem|15px|20px)', 'gap: 4rem', block)
    
    return block

# Find all blocks that target .hero-shell
# Pattern: selectors { rules }
pattern = re.compile(r'(?:[^{}]*?\.hero-shell[^{}]*?)\s*\{[^{}]*\}')

new_content = pattern.sub(update_block, content)

with open('vedtam.css', 'w', encoding='utf-8') as f:
    f.write(new_content)

print("Updated vedtam.css using regex for all hero-shell blocks.")
