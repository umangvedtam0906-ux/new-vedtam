import os
import re

base_dir = r"c:\Users\Manu\Downloads\new-vedtam\new-vedtam"
fa_link = '  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" />\n'

for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(root, file)
            with open(path, 'r', encoding='utf-8', errors='ignore') as f:
                content = f.read()
            
            orig_content = content
            
            # Simple replace instead of regex lookaheads which might be tricky
            content = content.replace('<span class="fc-icon">✓</span> Location:', '<i class="fas fa-map-marker-alt fc-icon"></i> Location:')
            content = content.replace('<span class="fc-icon">âœ‰</span> Email:', '<i class="fas fa-envelope fc-icon"></i> Email:')
            content = content.replace('<span class="fc-icon">â˜Ž</span> Phone:', '<i class="fas fa-phone fc-icon"></i> Phone:')
            
            # Variations with spaces
            content = re.sub(r'<span\s+class="fc-icon">\s*✓\s*</span>\s*Location:', '<i class="fas fa-map-marker-alt fc-icon"></i> Location:', content)
            content = re.sub(r'<span\s+class="fc-icon">\s*âœ‰\s*</span>\s*Email:', '<i class="fas fa-envelope fc-icon"></i> Email:', content)
            content = re.sub(r'<span\s+class="fc-icon">\s*â˜Ž\s*</span>\s*Phone:', '<i class="fas fa-phone fc-icon"></i> Phone:', content)

            if "font-awesome" not in content and "all.min.css" not in content:
                if "</head>" in content:
                    content = content.replace("</head>", fa_link + "</head>")
            
            if content != orig_content:
                with open(path, 'w', encoding='utf-8', errors='ignore') as f:
                    f.write(content)
                print(f"Fixed {file}")

