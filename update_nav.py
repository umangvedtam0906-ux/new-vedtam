import os
import re

def update_navbar_in_file(filepath):
    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        original_content = content
        
        # --- DESKTOP NAV CHANGES ---
        # 1. Remove Top-Level About Us
        content = re.sub(
            r'<li>\s*<a\s+href="about-us\.html"[^>]*>.*?</a>\s*</li>', 
            '', 
            content, 
            flags=re.IGNORECASE | re.DOTALL
        )
        
        # 2. Remove Top-Level Client Success (if any)
        content = re.sub(
            r'<li>\s*<a\s+href="client-success-portfolio\.html"[^>]*>.*?</a>\s*</li>', 
            '', 
            content, 
            flags=re.IGNORECASE | re.DOTALL
        )
        
        # 3. Remove Top-Level Software Solutions
        content = re.sub(
            r'<li>\s*<a\s+href="software-solutions\.html"[^>]*>.*?</a>\s*</li>', 
            '', 
            content, 
            flags=re.IGNORECASE | re.DOTALL
        )
        
        # 4. Insert Company Dropdown after Home
        company_dropdown = """
        <li>
          <a href="about-us.html">Company <svg viewBox="0 0 10 6" fill="none">
              <path d="M1 1l4 4 4-4" stroke="currentColor" stroke-width="1.5" stroke-linecap="round" />
            </svg></a>
          <div class="mega-menu">
            <div class="container">
              <div class="mega-inner">
                <div class="mega-col mega-info">
                  <h3>About Vedtam</h3>
                  <h2>Who We Are</h2>
                  <p>A trusted cybersecurity and IT services partner.</p>
                  <a href="about-us.html" class="mega-cta">Read Our Story &rarr;</a>
                </div>
                <div class="mega-col mega-links">
                  <h3>Company Pages</h3>
                  <div class="mega-links-grid">
                    <a href="about-us.html">About Us</a>
                    <a href="client-success-portfolio.html">Client Success & Portfolio</a>
                  </div>
                </div>
              </div>
            </div>
          </div>
        </li>"""
        
        # Check if Company dropdown is already there to prevent duplicates
        if "<h3>Company Pages</h3>" not in content:
            # Insert after Home
            content = re.sub(
                r'(<li>\s*<a\s+href="index\.html"[^>]*>.*?</a>\s*</li>)', 
                r'\1\n' + company_dropdown, 
                content, 
                count=1, 
                flags=re.IGNORECASE | re.DOTALL
            )
            
        # 5. Add Software Solutions to Services mega menu
        if '<a href="software-solutions.html">Software Solutions</a>' not in content:
            content = content.replace(
                '<a href="it-managed-services.html">IT Managed Services</a>', 
                '<a href="it-managed-services.html">IT Managed Services</a>\n                    <a href="software-solutions.html">Software Solutions</a>'
            )
            
        # --- MOBILE NAV CHANGES ---
        # 1. Delete old Company section at bottom
        content = re.sub(
            r'<div class="m-section">Company</div>\s*<a href="software-solutions\.html"[^>]*>.*?</a>\s*<a href="cert-advisory\.html"[^>]*>.*?</a>\s*<a href="contact-us\.html"[^>]*>.*?</a>', 
            '', 
            content, 
            flags=re.IGNORECASE | re.DOTALL
        )
        
        if content != original_content:
            with open(filepath, 'w', encoding='utf-8') as f:
                f.write(content)
            print(f"Updated navbar in {filepath}")
        else:
            print(f"No changes needed for {filepath}")
            
    except Exception as e:
        print(f"Error processing {filepath}: {e}")

if __name__ == "__main__":
    skip_files = ['index.html', 'about-us.html', 'software-solutions.html', 'client-success-portfolio.html']
    html_files = [f for f in os.listdir('.') if f.endswith('.html')]
    
    print(f"Found {len(html_files)} HTML files. Updating navigation...")
    for file in html_files:
        if file in skip_files:
            continue
        update_navbar_in_file(file)
    print("Done!")
