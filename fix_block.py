import os
import re

base_dir = r"c:\Users\Manu\Downloads\new-vedtam\new-vedtam"
fa_link = '  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" />\n'

new_block = '''<div class="footer-contact">
            <a href="https://maps.google.com/?q=Noida%2C+Uttar+Pradesh%2C+India" target="_blank" rel="noopener"><i class="fas fa-map-marker-alt fc-icon"></i> Location: Noida, Uttar Pradesh, India</a>
            <a href="mailto:info@vedtam.com"><i class="fas fa-envelope fc-icon"></i> Email: info@vedtam.com</a>
            <a href="tel:+917065111015"><i class="fas fa-phone fc-icon"></i> Phone: +91 70651 11015</a>
          </div>'''

fixed = 0
for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(root, file)
            with open(path, 'rb') as f:
                content = f.read().decode('utf-8', errors='ignore')
            
            orig = content
            
            # Replace the entire footer-contact block
            # Match <div class="footer-contact">...</div>
            content = re.sub(r'<div class="footer-contact">.*?</div>', new_block, content, flags=re.DOTALL)
            
            if "font-awesome" not in content and "all.min.css" not in content:
                content = content.replace("</head>", fa_link + "</head>")
            
            if content != orig:
                with open(path, 'wb') as f:
                    f.write(content.encode('utf-8'))
                print("FIXED", path)
                fixed += 1

print(f"Total fixed: {fixed}")
