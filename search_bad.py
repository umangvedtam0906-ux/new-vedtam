import os

base_dir = r"c:\Users\Manu\Downloads\new-vedtam\new-vedtam"

for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(root, file)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception:
                try:
                    with open(path, 'r', encoding='windows-1252') as f:
                        content = f.read()
                except:
                    continue
            
            # Check for different broken characters
            if "âœ‰" in content or "â˜Ž" in content or "fc-icon" in content:
                print(f"MATCH IN {path}")
                
                # Try replacing with regex for anything matching the pattern
                import re
                
                # Location
                new_content = re.sub(r'<span[^>]*class="fc-icon"[^>]*>.*?✓.*?</span>', '<i class="fas fa-map-marker-alt fc-icon"></i>', content, flags=re.DOTALL)
                
                # Email
                new_content = re.sub(r'<span[^>]*class="fc-icon"[^>]*>.*?âœ‰.*?</span>', '<i class="fas fa-envelope fc-icon"></i>', new_content, flags=re.DOTALL)
                
                # Phone
                new_content = re.sub(r'<span[^>]*class="fc-icon"[^>]*>.*?â˜Ž.*?</span>', '<i class="fas fa-phone fc-icon"></i>', new_content, flags=re.DOTALL)
                
                # Add font-awesome
                if "font-awesome" not in new_content and "all.min.css" not in new_content:
                    new_content = new_content.replace("</head>", '  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" />\n</head>')

                if new_content != content:
                    with open(path, 'w', encoding='utf-8') as f:
                        f.write(new_content)
                    print(f"FIXED {path}")
