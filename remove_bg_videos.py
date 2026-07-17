import os, re

files = [
    'virtual-ciso-services.html',
    'qms-consulting-services.html',
    'soc-2-consulting-services.html',
    'pci-dss-consulting-services.html',
    'network-security-audit-services.html',
    'iso-consulting-services.html',
    'gdpr-consulting-services.html',
    'dpdp-act-consulting-services.html',
    'hipaa-consulting-services.html'
]

pattern = re.compile(r'\s*<video[^>]*>.*?<\/video>', re.DOTALL)

for f in files:
    if os.path.exists(f):
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
            
        new_content = pattern.sub('', content)
        
        if content != new_content:
            with open(f, 'w', encoding='utf-8') as file:
                file.write(new_content)
            print(f'Updated {f}')
        else:
            print(f'No video found in {f}')
