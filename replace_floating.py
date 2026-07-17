import os
import re

directory = r"c:\Users\Manu\Downloads\new-vedtam-main (7)\new-vedtam"

# 1. Extract the perfect floating button from index.html
with open(os.path.join(directory, "index.html"), "r", encoding="utf-8") as f:
    content = f.read()

s_idx = content.find('<div aria-label="Quick actions" class="floating-actions">')
e_idx = content.find('</div>', s_idx) + 6
new_button = content[s_idx:e_idx]

print("Extracted button length:", len(new_button))

count = 0
for root, dirs, files in os.walk(directory):
    for file in files:
        if file.endswith(".html") and file != "index.html":
            path = os.path.join(root, file)
            # Skip backups
            if "backups" in root:
                continue
                
            try:
                with open(path, "r", encoding="utf-8", errors="ignore") as f:
                    html = f.read()
                
                orig_html = html
                
                # Strip out any existing floating-actions div
                html = re.sub(r'<div[^>]*class="[^"]*floating-actions[^"]*"[^>]*>.*?</div>', '', html, flags=re.DOTALL)
                
                # Strip out any old stray whatsapp buttons
                html = re.sub(r'<a[^>]*class="[^"]*whatsapp-float[^"]*"[^>]*>.*?</a>', '', html, flags=re.DOTALL)
                
                # Strip out any old stray scroll-top buttons
                html = re.sub(r'<button[^>]*class="[^"]*scroll-top[^"]*"[^>]*>.*?</button>', '', html, flags=re.DOTALL)
                
                # Now inject the new button right before </body>
                if "</body>" in html:
                    html = html.replace("</body>", new_button + "\n</body>")
                
                if html != orig_html:
                    with open(path, "w", encoding="utf-8") as fw:
                        fw.write(html)
                    count += 1
                    print(f"Updated {file}")
            except Exception as e:
                print(f"Error on {file}: {e}")

print(f"Done! Perfectly updated {count} files.")
