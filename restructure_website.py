import os
import shutil
from bs4 import BeautifulSoup

# Define the root directory of your website
ROOT_DIR = r"c:\Users\Manu\Desktop\vedtam website"

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
    "assets": {
        "css": [
            "vedtam.css",
            "dpdp-hero.css",
            "gdpr-hero.css",
            "hipaa-hero.css",
            "network-security.css",
            "pci-hero.css",
            "soc2-hero.css",
        ],
        "js": [
            "vedtam.js",
            "force-field.js",
            "gooey-gradient.js",
            "network-security-canvas.js",
        ],
        "images": [
            "services_images", # This is a directory
            "card_logo",      # This is a directory
            "industry_images", # This is a directory
            "Vedtam Partners", # This is a directory
            "website-logo",    # This is a directory
            "vedtam TESTIMONIAL", # This is a directory
        ],
        "videos": [
            "videos", # This is a directory
        ],
        "data": [
            "cert-data.json",
        ]
    }
}

# Mapping for renames
RENAMES = {
    "software-solutions.html": "software-services.html",
    "soc-2-consulting-services.html": "soc2-consulting-services.html",
}

# List of all HTML files that will be processed for link updates
ALL_HTML_FILES = []

def create_and_move_files():
    print("--- Creating directories and moving files ---")
    for new_dir, contents in NEW_STRUCTURE.items():
        if isinstance(contents, list): # HTML files
            target_dir = os.path.join(ROOT_DIR, new_dir)
            os.makedirs(target_dir, exist_ok=True)
            for filename in contents:
                old_path = os.path.join(ROOT_DIR, filename)
                new_filename = RENAMES.get(filename, filename)
                new_path = os.path.join(target_dir, new_filename)
                if os.path.exists(old_path):
                    shutil.move(old_path, new_path)
                    print(f"Moved: {filename} -> {new_dir}/{new_filename}")
                    ALL_HTML_FILES.append(new_path)
                else:
                    print(f"Warning: {filename} not found at {old_path}")
        elif isinstance(contents, dict): # Assets
            for sub_dir, files_or_dirs in contents.items():
                target_dir = os.path.join(ROOT_DIR, new_dir, sub_dir)
                os.makedirs(target_dir, exist_ok=True)
                for item_name in files_or_dirs:
                    old_path = os.path.join(ROOT_DIR, item_name)
                    new_path = os.path.join(target_dir, item_name)
                    if os.path.exists(old_path):
                        shutil.move(old_path, new_path)
                        print(f"Moved: {item_name} -> {new_dir}/{sub_dir}/{item_name}")
                    else:
                        print(f"Warning: {item_name} not found at {old_path}")

    # Add root-level HTML files to the list for link processing
    for filename in ["index.html", "about-us.html", "contact-us.html", "client-success-portfolio.html", "privacy-policy.html", "terms-of-service.html", "cert-advisory.html", "blog.html", "cookie-preferences.html"]:
        if os.path.exists(os.path.join(ROOT_DIR, filename)):
            ALL_HTML_FILES.append(os.path.join(ROOT_DIR, filename))

def update_links_in_html_files():
    print("\n--- Updating links in HTML files ---")
    
    # Build a comprehensive mapping of old relative paths to new relative paths
    # This is crucial for resolving links correctly
    path_map = {}
    
    # HTML files
    for new_dir, files in NEW_STRUCTURE.items():
        if isinstance(files, list):
            for old_filename in files:
                new_filename = RENAMES.get(old_filename, old_filename)
                path_map[old_filename] = os.path.join(new_dir, new_filename)
    
    # Asset files/directories
    for asset_type, items in NEW_STRUCTURE["assets"].items():
        for item_name in items:
            path_map[item_name] = os.path.join("assets", asset_type, item_name)
            # Handle specific files within moved directories if they were referenced directly
            if item_name in ["services_images", "card_logo", "industry_images", "Vedtam Partners", "website-logo", "videos", "vedtam TESTIMONIAL"]:
                # This is a directory, so direct file references need to be updated
                # e.g., "services_images/image.png" -> "assets/images/services_images/image.png"
                # This is a more complex rewrite, handled by checking if the path starts with the old dir name
                pass

    # Add root level files that don't move but might link to moved files
    root_html_files = ["index.html", "about-us.html", "contact-us.html", "client-success-portfolio.html", "privacy-policy.html", "terms-of-service.html", "cert-advisory.html", "blog.html", "cookie-preferences.html"]
    for filename in root_html_files:
        path_map[filename] = filename # They stay in the root

    for html_filepath in ALL_HTML_FILES:
        with open(html_filepath, "r", encoding="utf-8") as f:
            soup = BeautifulSoup(f, "html.parser")

        original_content = str(soup)
        current_dir = os.path.dirname(html_filepath)
        
        for tag in soup.find_all(['a', 'link', 'script', 'img', 'source']):
            for attr in ['href', 'src']:
                if tag.has_attr(attr):
                    old_relative_path = tag[attr]

                    # Skip external links, anchors, and absolute paths
                    if old_relative_path.startswith(('http', '#', '/', 'data:')):
                        continue

                    # Determine the base filename or directory name for lookup
                    base_name = old_relative_path.split('/')[0]
                    
                    new_relative_path = None

                    # Check if it's a direct file move
                    if base_name in path_map:
                        if '/' in old_relative_path: # e.g., services_images/image.png
                            # Reconstruct path with new base directory
                            new_relative_path = os.path.join(path_map[base_name], *old_relative_path.split('/')[1:])
                        else: # e.g., cybersecurity-services.html
                            new_relative_path = path_map[base_name]
                    else:
                        # Handle cases where the file itself is not a key in path_map,
                        # but its parent directory might have moved (e.g., assets/css/vedtam.css)
                        # This requires a more generic check against the NEW_STRUCTURE
                        for new_top_dir, contents in NEW_STRUCTURE.items():
                            if isinstance(contents, dict): # Assets
                                for sub_dir, items_list in contents.items():
                                    for item_name_in_list in items_list: # Iterate through the list of items
                                        if normalized_old_path.startswith(item_name_in_list + '/') or normalized_old_path == item_name_in_list: # Handle files within moved dirs or direct file matches
                                            new_relative_path = os.path.join(new_top_dir, sub_dir, old_relative_path).replace('\\', '/')
                                            break
                                    if new_relative_path: break
                            elif isinstance(contents, list): # HTML files
                                if old_relative_path in contents or RENAMES.get(old_relative_path) in contents:
                                    new_relative_path = os.path.join(new_top_dir, RENAMES.get(old_relative_path, old_relative_path))
                                    break

                    if new_relative_path:
                        # Calculate the correct relative path from the current HTML file's location
                        # to the target's new location
                        target_absolute_path = os.path.join(ROOT_DIR, new_relative_path)
                        final_relative_path = os.path.relpath(target_absolute_path, current_dir)
                        
                        # Normalize backslashes for web paths
                        final_relative_path = final_relative_path.replace('\\', '/')
                        
                        tag[attr] = final_relative_path
                        # print(f"  Updated {old_relative_path} -> {final_relative_path} in {os.path.basename(html_filepath)}")

        updated_content = str(soup)
        if updated_content != original_content:
            with open(html_filepath, "w", encoding="utf-8") as f:
                f.write(updated_content)
            print(f"✅ Links updated in: {os.path.relpath(html_filepath, ROOT_DIR)}")
        # else:
            # print(f"  No link changes needed in: {os.path.relpath(html_filepath, ROOT_DIR)}")

def main():
    # Ensure BeautifulSoup is installed
    try:
        import bs4
    except ImportError:
        print("BeautifulSoup4 is not installed. Please install it using: pip install beautifulsoup4")
        return

    # Create directories and move files
    create_and_move_files()

    # Update links in all HTML files
    update_links_in_html_files()

    print("\n--- Website restructuring and link updating complete ---")

if __name__ == "__main__":
    main()