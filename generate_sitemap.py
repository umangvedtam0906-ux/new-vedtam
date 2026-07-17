import os
import re
import xml.etree.ElementTree as ET

def get_links():
    tree = ET.parse('sitemap.xml')
    root = tree.getroot()
    namespace = {'ns': 'http://www.sitemaps.org/schemas/sitemap/0.9'}
    
    links = []
    for url in root.findall('ns:url', namespace):
        loc = url.find('ns:loc', namespace).text
        if loc.startswith('https://www.vedtam.com/'):
            path = loc.replace('https://www.vedtam.com/', '')
            if not path or path == '/':
                path = 'index.html'
            links.append(path)
    return links

def format_title(path):
    if path == 'index.html':
        return 'Home'
    name = path.split('/')[-1].replace('.html', '').replace('-', ' ').title()
    return name

def group_links(links):
    grouped = {'Core Pages': [], 'Solutions': [], 'Consulting': []}
    for link in links:
        if link.startswith('solutions/'):
            grouped['Solutions'].append(link)
        elif link.startswith('consulting/'):
            grouped['Consulting'].append(link)
        else:
            grouped['Core Pages'].append(link)
    return grouped

def create_sitemap_html():
    with open('index.html', 'r', encoding='utf-8') as f:
        index_content = f.read()

    header_match = re.search(r'(.*?)(?:<!-- Hero -->|<section class="hero|<div class="split-modal-overlay")', index_content, re.DOTALL)
    if not header_match:
        print("Could not extract header.")
        return

    header = header_match.group(1)

    footer_match = re.search(r'(<footer class="footer">.*)', index_content, re.DOTALL)
    if not footer_match:
        print("Could not extract footer.")
        return
    
    footer = footer_match.group(1)

    links = get_links()
    grouped = group_links(links)

    sitemap_content = """
    <style>
      .sitemap-link:hover { color: var(--orange) !important; padding-left: 5px; }
    </style>
    <section class="hero" style="min-height: auto; padding-top: 120px; padding-bottom: 3rem; background: #111114;">
        <div class="container" style="text-align: center;">
            <div class="hero-badge" style="display:inline-block; padding:0.45rem 1.1rem; background:rgba(8, 68, 129, 0.15); border:1px solid rgba(8, 68, 129, 0.3); border-radius:999px; color:var(--orange); font-size:0.78rem; font-weight:700; letter-spacing:0.08em; text-transform:uppercase; margin-bottom:1.2rem;">Overview</div>
            <h1 class="hero-title" style="font-size: clamp(2rem, 5vw, 3rem); font-weight: 800; color: #ffffff; line-height: 1.2; margin-bottom: 1rem;">
                Website <span style="color:var(--cyan);">Sitemap</span>
            </h1>
            <p style="color: rgba(255, 255, 255, 0.65); font-size: 1rem; max-width: 560px; margin: 0 auto;">
                A complete overview of all pages and services on Vedtam Tech Solutions.
            </p>
        </div>
    </section>

    <section class="sitemap-section" style="padding: 4rem 0; background: #0c1524;">
        <div class="container">
            <div style="display: grid; grid-template-columns: repeat(auto-fit, minmax(300px, 1fr)); gap: 2rem;">
"""
    for category, items in grouped.items():
        if items:
            sitemap_content += f"""
                <div class="sitemap-category" style="background: rgba(12, 21, 36, 0.9); border: 1px solid rgba(8, 68, 129, 0.4); border-radius: 16px; padding: 2rem;">
                    <h2 style="color: #ffffff; font-size: 1.4rem; font-weight: 700; margin-bottom: 1.5rem; border-bottom: 1px solid rgba(255, 255, 255, 0.1); padding-bottom: 0.5rem;">{category}</h2>
                    <ul style="list-style: none; padding: 0; margin: 0; display: flex; flex-direction: column; gap: 0.8rem;">
            """
            for item in items:
                title = format_title(item)
                sitemap_content += f"""
                        <li>
                            <a href="{item}" class="sitemap-link" style="color: rgba(255, 255, 255, 0.7); text-decoration: none; font-size: 1rem; transition: all 0.3s ease; display: inline-flex; align-items: center; gap: 0.5rem;">
                                <span style="color: var(--orange); font-size: 0.8rem;">▶</span> {title}
                            </a>
                        </li>
                """
            sitemap_content += """
                    </ul>
                </div>
            """
    
    sitemap_content += """
            </div>
        </div>
    </section>
"""
    header = re.sub(r'<title>.*?</title>', '<title>Sitemap | Vedtam Tech Solutions</title>', header)
    
    full_html = header + sitemap_content + footer

    with open('sitemap.html', 'w', encoding='utf-8') as f:
        f.write(full_html)
    print("Created sitemap.html successfully.")

def update_all_footers():
    for root, dirs, files in os.walk('.'):
        for filename in files:
            if filename.endswith('.html') and filename != 'sitemap.html':
                filepath = os.path.join(root, filename)
                try:
                    with open(filepath, 'r', encoding='utf-8') as f:
                        content = f.read()
                    
                    changed = False
                    
                    # Convert existing sitemap.xml links to sitemap.html
                    if 'sitemap.xml' in content:
                        content = content.replace('"sitemap.xml"', '"sitemap.html"')
                        changed = True

                    # Find where to inject the sitemap link if it's completely missing
                    if 'sitemap.html' not in content and 'Terms of Service</a>' in content:
                        # Depending on the level of indentation in different files, use a regex
                        content = re.sub(
                            r'(<a href="([./]*)terms-of-service\.html">Terms of Service</a>)',
                            r'\1\n          <a href="\2sitemap.html">Sitemap</a>',
                            content
                        )
                        changed = True

                    if changed:
                        with open(filepath, 'w', encoding='utf-8') as f:
                            f.write(content)
                        print(f"Added/Updated Sitemap link in footer of {filepath}")
                except Exception as e:
                    pass

if __name__ == '__main__':
    create_sitemap_html()
    update_all_footers()
