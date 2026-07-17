import re
import glob

files = [
    'Virtual CISO.html', 'ISO.html', 'QMS.html', 'HIPPA.html', 
    'PCI dss.html', 'GDPR.html', 'DPDP.html', 'Network security Audit.html'
]

for f in files:
    try:
        with open(f, 'r', encoding='utf-8') as file:
            content = file.read()
            # find first <h1 ...>...</h1>
            h1 = re.search(r'<h1[^>]*>.*?</h1>', content, re.DOTALL)
            # find first <p ...>...</p> after h1
            p = None
            if h1:
                p = re.search(r'<p[^>]*>.*?</p>', content[h1.end():], re.DOTALL)
            
            print(f"--- {f} ---")
            if h1:
                print(f"H1: {h1.group(0).strip()}")
            if p:
                print(f"P: {p.group(0).strip()}")
            print()
    except Exception as e:
        print(f"Error reading {f}: {e}")
