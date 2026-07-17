import os
import re
base_dir = os.path.dirname(os.path.abspath(__file__))

# The FontAwesome link to add
fa_link = '  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" />\n'

for root, dirs, files in os.walk(base_dir):
    for file in files:
        if file.endswith(".html"):
            path = os.path.join(root, file)
            try:
                with open(path, 'r', encoding='utf-8') as f:
                    content = f.read()
            except UnicodeDecodeError:
                with open(path, 'r', encoding='windows-1252') as f:
                    content = f.read()
            
            modified = False
            
            # Check for Font Awesome
            if "font-awesome" not in content and "all.min.css" not in content:
                # Add before </head>
                if "</head>" in content:
                    content = content.replace("</head>", fa_link + "</head>")
                    modified = True

            # Replace footer icons
            # Location
            loc_pattern = r'<span\s+class="fc-icon">✓</span>'
            if re.search(loc_pattern, content):
                content = re.sub(loc_pattern, '<i class="fas fa-map-marker-alt fc-icon"></i>', content)
                modified = True

            # Email
            email_pattern = r'<span\s+class="fc-icon">âœ‰</span>'
            if re.search(email_pattern, content):
                content = re.sub(email_pattern, '<i class="fas fa-envelope fc-icon"></i>', content)
                modified = True

            # Phone
            phone_pattern = r'<span\s+class="fc-icon">â˜Ž</span>'
            if re.search(phone_pattern, content):
                content = re.sub(phone_pattern, '<i class="fas fa-phone fc-icon"></i>', content)
                modified = True

            if modified:
                with open(path, 'w', encoding='utf-8') as f:
                    f.write(content)
                print(f"Fixed: {path}")
