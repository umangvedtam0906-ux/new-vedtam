import os
import re

base_dir = r"c:\Users\Manu\Downloads\new-vedtam\new-vedtam"
fa_link = '  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" />\n'

fixed_count = 0

for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(root, file)
            with open(path, 'rb') as f:
                content_bytes = f.read()
            
            # Read as UTF-8 ignoring errors
            content = content_bytes.decode('utf-8', errors='ignore')
            orig = content
            
            # Regex replacements
            content = re.sub(r'<span[^>]*class="fc-icon"[^>]*>.*?</span>(?=\s*Location:)', '<i class="fas fa-map-marker-alt fc-icon"></i>', content, flags=re.DOTALL)
            content = re.sub(r'<span[^>]*class="fc-icon"[^>]*>.*?</span>(?=\s*Email:)', '<i class="fas fa-envelope fc-icon"></i>', content, flags=re.DOTALL)
            content = re.sub(r'<span[^>]*class="fc-icon"[^>]*>.*?</span>(?=\s*Phone:)', '<i class="fas fa-phone fc-icon"></i>', content, flags=re.DOTALL)
            
            # Also try without the colon just in case
            content = re.sub(r'<span[^>]*class="fc-icon"[^>]*>.*?</span>(?=\s*Location)', '<i class="fas fa-map-marker-alt fc-icon"></i>', content, flags=re.DOTALL)
            content = re.sub(r'<span[^>]*class="fc-icon"[^>]*>.*?</span>(?=\s*Email)', '<i class="fas fa-envelope fc-icon"></i>', content, flags=re.DOTALL)
            content = re.sub(r'<span[^>]*class="fc-icon"[^>]*>.*?</span>(?=\s*Phone)', '<i class="fas fa-phone fc-icon"></i>', content, flags=re.DOTALL)

            if "font-awesome" not in content and "all.min.css" not in content:
                content = content.replace("</head>", fa_link + "</head>")
            
            if content != orig:
                with open(path, 'wb') as f:
                    f.write(content.encode('utf-8'))
                print("FIXED", path)
                fixed_count += 1

print(f"Total files fixed: {fixed_count}")
