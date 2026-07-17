import os

base_dir = r"c:\Users\Manu\Downloads\new-vedtam\new-vedtam"

fa_link = '  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" />\n'

for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(root, file)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except Exception as e:
                try:
                    with open(path, 'r', encoding='windows-1252') as f:
                        content = f.read()
                except Exception as e2:
                    print(f"Skipping {path} due to read error.")
                    continue
            
            modified = False
            
            if "font-awesome" not in content and "all.min.css" not in content:
                if "</head>" in content:
                    content = content.replace("</head>", fa_link + "</head>")
                    modified = True

            # Use generic string replacement to handle variations
            replacements = [
                ('<span class="fc-icon">✓</span>', '<i class="fas fa-map-marker-alt fc-icon"></i>'),
                ('<span class="fc-icon">âœ‰</span>', '<i class="fas fa-envelope fc-icon"></i>'),
                ('<span class="fc-icon">â˜Ž</span>', '<i class="fas fa-phone fc-icon"></i>'),
                ('<span\n                class="fc-icon">✓</span>', '<i class="fas fa-map-marker-alt fc-icon"></i>'),
                ('<span\n                class="fc-icon">âœ‰</span>', '<i class="fas fa-envelope fc-icon"></i>'),
                ('<span\n                class="fc-icon">â˜Ž</span>', '<i class="fas fa-phone fc-icon"></i>'),
                ('<span\r\n                class="fc-icon">✓</span>', '<i class="fas fa-map-marker-alt fc-icon"></i>'),
                ('<span\r\n                class="fc-icon">âœ‰</span>', '<i class="fas fa-envelope fc-icon"></i>'),
                ('<span\r\n                class="fc-icon">â˜Ž</span>', '<i class="fas fa-phone fc-icon"></i>')
            ]

            for old_str, new_str in replacements:
                if old_str in content:
                    content = content.replace(old_str, new_str)
                    modified = True

            if modified:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Fixed: {path}")
