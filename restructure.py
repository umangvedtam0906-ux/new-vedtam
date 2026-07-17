
import os
import shutil
from bs4 import BeautifulSoup
import urllib.parse

# Define the root directory of your website
ROOT_DIR = os.path.abspath(r"c:\Users\Manu\Desktop\vedtam website")

# Define the new directory structure
NEW_STRUCTURE = {
    "solutions": [
        "cyber-security-services.html",
        "network-security-solutions.html",
        "devops-solutions.html",
        "ot-security-services.html",
        "cloud-services.html",
        "it-managed-services.html",
        "software-solutions.html", # Will be renamed to software-services.html
    ],
    "consulting": [
        "virtual-ciso-services.html",
        "iso-consulting-services.html",
        "qms-consulting-services.html",
        "hipaa-consulting-services.html",
        "pci-dss-consulting-services.html",
        "gdpr-consulting-services.html",
        "soc-2-consulting-services.html", # Will be renamed to soc2-consulting-services.html
        "dpdp-act-consulting-services.html",
        "network-security-consulting-services.html",
        "network-security-audit-services.html",
    ],
    "blog": [
        "blog-data-protection-officer-dpdp-act.html",
        "blog-dpdp-act-penalties-non-compliance.html",
        "blog-dpdp-act-vs-gdpr-differences.html",
        "blog-iso-27001-certification-guide-india.html",
        "blog-iso-27001-vs-soc-2.html",
        "blog-zero-trust-cloud-architecture.html",
    ],
    "assets/css": [
        "vedtam.css",
        "dpdp-hero.css",
        "gdpr-hero.css",
        "hipaa-hero.css",
        "network-security.css",
        "pci-hero.css",
        "soc2-hero.css",
    ],
    "assets/js": [
        "vedtam.js",
        "force-field.js",
        "gooey-gradient.js",
        "network-security-canvas.js",
        "ghost-cursor.js",
        "chart.js",
        "extract.js",
        "test.js",
    ],
    "assets/videos": [
        "videos", # This is a directory
    ]
}

# Mapping for renames
RENAMES = {
    "software-solutions.html": "software-services.html",
    "soc-2-consulting-services.html": "soc2-consulting-services.html",
}

def main():
    print("--- Starting Website Restructure ---")
    
    # Store old_abs_path -> new_abs_path mapping
    path_mapping = {}
    
    # We also need to map the old HTML absolute paths to new HTML absolute paths 
    # to know which files to process and where they are now.
    html_files_to_process = []
    
    # 1. First find all HTML files currently in ROOT_DIR
    all_old_files = os.listdir(ROOT_DIR)
    for filename in all_old_files:
        old_path = os.path.join(ROOT_DIR, filename)
        if os.path.isfile(old_path) and filename.endswith(".html"):
            html_files_to_process.append(old_path)
    
    # 2. Perform moves and build path_mapping
    for new_dir_rel, items in NEW_STRUCTURE.items():
        new_dir_abs = os.path.join(ROOT_DIR, new_dir_rel.replace('/', os.sep))
        os.makedirs(new_dir_abs, exist_ok=True)
        
        for item_name in items:
            old_path = os.path.join(ROOT_DIR, item_name)
            new_item_name = RENAMES.get(item_name, item_name)
            new_path = os.path.join(new_dir_abs, new_item_name)
            
            if os.path.exists(old_path):
                # Only move if the source and destination are different
                if os.path.abspath(old_path) != os.path.abspath(new_path):
                    shutil.move(old_path, new_path)
                    print(f"Moved: {item_name} -> {os.path.relpath(new_path, ROOT_DIR)}")
                path_mapping[os.path.abspath(old_path)] = os.path.abspath(new_path)
            else:
                print(f"Warning: {item_name} not found at {old_path}")

    # Now handle mapping for HTML files that didn't move (e.g. index.html)
    new_html_files = []
    for old_html_path in html_files_to_process:
        old_abs = os.path.abspath(old_html_path)
        if old_abs in path_mapping:
            new_html_files.append((old_abs, path_mapping[old_abs]))
        else:
            # File didn't move
            new_html_files.append((old_abs, old_abs))
    
    # Also build a directory mapping for moved directories (like videos)
    dir_mapping = {}
    for old_path, new_path in path_mapping.items():
        if os.path.isdir(new_path):
            dir_mapping[old_path] = new_path

    # 3. Process all HTML files
    print("\n--- Updating links in HTML files ---")
    for old_html_path, new_html_path in new_html_files:
        if not os.path.exists(new_html_path):
            continue
            
        with open(new_html_path, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")
            
        original_content = str(soup)
        old_html_dir = os.path.dirname(old_html_path)
        new_html_dir = os.path.dirname(new_html_path)
        
        for tag in soup.find_all(['a', 'link', 'script', 'img', 'source']):
            for attr in ['href', 'src']:
                if tag.has_attr(attr):
                    old_rel_url = tag[attr]
                    
                    # Skip external links, fragments, data URIs, absolute paths
                    if old_rel_url.startswith(('http://', 'https://', 'mailto:', 'tel:', '#', 'data:')) or old_rel_url.startswith('/'):
                        continue
                        
                    # Remove query params or fragments for path resolution, then append them back later
                    parsed = urllib.parse.urlparse(old_rel_url)
                    url_path = urllib.parse.unquote(parsed.path)
                    
                    if not url_path:
                        continue
                        
                    # Resolve old target absolute path
                    old_target_abs = os.path.abspath(os.path.join(old_html_dir, url_path.replace('/', os.sep)))
                    
                    # Determine new target absolute path
                    new_target_abs = old_target_abs
                    if old_target_abs in path_mapping:
                        new_target_abs = path_mapping[old_target_abs]
                    else:
                        # Check if it falls under a moved directory
                        for old_dir, new_dir in dir_mapping.items():
                            if old_target_abs.startswith(old_dir + os.sep):
                                rel_to_dir = os.path.relpath(old_target_abs, old_dir)
                                new_target_abs = os.path.join(new_dir, rel_to_dir)
                                break
                    
                    # Calculate new relative path
                    new_rel_path = os.path.relpath(new_target_abs, new_html_dir)
                    # Use forward slashes for URLs
                    new_rel_url_path = new_rel_path.replace(os.sep, '/')
                    
                    # Reconstruct URL with query params / fragments
                    new_rel_url = urllib.parse.urlunparse(('', '', urllib.parse.quote(new_rel_url_path), parsed.params, parsed.query, parsed.fragment))
                    
                    if old_rel_url != new_rel_url:
                        tag[attr] = new_rel_url

        updated_content = str(soup)
        if updated_content != original_content:
            with open(new_html_path, "w", encoding="utf-8") as f:
                f.write(updated_content)
            print(f"✅ Updated links in {os.path.relpath(new_html_path, ROOT_DIR)}")

    print("\n--- Done ---")

if __name__ == "__main__":
    main()
