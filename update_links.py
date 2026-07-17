import os
import re

directory = r"c:\Users\Manu\Desktop\vedtam website"
target_file = "network-security-consulting-services.html"

desktop_nav_pattern = re.compile(r'(^[ \t]*)(<a href="network-security-audit-services\.html"(?: class="active")?>Network Security Audit</a>)', re.MULTILINE)
footer_nav_pattern = re.compile(r'(^[ \t]*)(<li><a href="network-security-audit-services\.html"(?: class="active")?>Network Security Audit</a></li>)', re.MULTILINE)

desktop_repl = r'\1<a href="network-security-consulting-services.html">Network Security Consulting</a>\n\1\2'
footer_repl = r'\1<li><a href="network-security-consulting-services.html">Network Security Consulting</a></li>\n\1\2'

for filename in os.listdir(directory):
    if filename.endswith(".html") and filename != target_file:
        filepath = os.path.join(directory, filename)
        with open(filepath, 'rb') as f:
            content_bytes = f.read()
            
        try:
            content = content_bytes.decode('utf-8')
        except UnicodeDecodeError:
            print(f"Skipping {filename} due to encoding issue")
            continue
            
        if "network-security-consulting-services.html" not in content:
            new_content = desktop_nav_pattern.sub(desktop_repl, content)
            new_content = footer_nav_pattern.sub(footer_repl, new_content)
            
            if new_content != content:
                if b'\r\n' in content_bytes:
                    new_content = new_content.replace('\n', '\r\n').replace('\r\r\n', '\r\n')
                
                with open(filepath, 'wb') as f:
                    f.write(new_content.encode('utf-8'))
                print(f"Updated {filename}")
