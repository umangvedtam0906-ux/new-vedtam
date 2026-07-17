import re
import sys

try:
    with open("vedtam.css", "r", encoding="utf-16") as f:
        content = f.read()
except:
    with open("vedtam.css", "r", encoding="utf-8", errors="replace") as f:
        content = f.read()

# Find all blocks of code that start with @media and end with the matching closing brace.
# CSS can have nested braces, so we need a slightly more complex parser or we just find @media and grab next 10 lines.

def extract_media_queries(css):
    results = []
    lines = css.splitlines()
    inside_media = False
    brace_count = 0
    current_mq = []
    
    for line in lines:
        if "@media" in line:
            inside_media = True
            
        if inside_media:
            current_mq.append(line)
            brace_count += line.count('{')
            brace_count -= line.count('}')
            
            if brace_count == 0 and len(current_mq) > 1:
                inside_media = False
                results.append('\n'.join(current_mq))
                current_mq = []
                
    return results

mqs = extract_media_queries(content)
with open("media_queries_extracted.css", "w", encoding="utf-8") as out:
    for mq in mqs:
        out.write(mq + "\n\n")

print(f"Extracted {len(mqs)} media queries to media_queries_extracted.css")
