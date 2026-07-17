import os
import re

base_dir = r"c:\Users\Manu\Downloads\new-vedtam\new-vedtam"
fa_link = '  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" />\n'

count = 0
for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()

            modified = False

            # Replace location span
            pattern1 = re.compile(r'<span[^>]*class="fc-icon"[^>]*>.*?✓.*?</span>', re.DOTALL)
            if pattern1.search(content):
                content = pattern1.sub('<i class="fas fa-map-marker-alt fc-icon"></i>', content)
                modified = True

            # Replace email span (match any span containing an envelope mojibake or similar)
            # The mojibake is "âœ‰" but it might be read differently. Let's just match any span with fc-icon that's right before " Email:"
            pattern2 = re.compile(r'<span[^>]*class="fc-icon"[^>]*>.*?</span>(?=\s*Email:)', re.DOTALL)
            if pattern2.search(content):
                content = pattern2.sub('<i class="fas fa-envelope fc-icon"></i>', content)
                modified = True

            # Replace phone span
            pattern3 = re.compile(r'<span[^>]*class="fc-icon"[^>]*>.*?</span>(?=\s*Phone:)', re.DOTALL)
            if pattern3.search(content):
                content = pattern3.sub('<i class="fas fa-phone fc-icon"></i>', content)
                modified = True

            # Also replace location span if it's before " Location:"
            pattern4 = re.compile(r'<span[^>]*class="fc-icon"[^>]*>.*?</span>(?=\s*Location:)', re.DOTALL)
            if pattern4.search(content):
                content = pattern4.sub('<i class="fas fa-map-marker-alt fc-icon"></i>', content)
                modified = True

            # Font-awesome
            if "font-awesome" not in content and "all.min.css" not in content:
                if "</head>" in content:
                    content = content.replace("</head>", fa_link + "</head>")
                    modified = True

            if modified:
                with open(path, 'w', encoding='utf-8', errors='ignore') as f:
                    f.write(content)
                count += 1
                print(f"Fixed {file}")

print(f"Total fixed: {count}")
