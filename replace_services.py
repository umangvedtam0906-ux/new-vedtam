import os

# Define the root directory of your website
ROOT_DIR = os.path.abspath(r"c:\Users\Manu\Desktop\vedtam website")

def main():
    print("--- Starting Nav Bar Update ---")
    
    html_files = []
    # Walk through all directories and find .html files
    for root, dirs, files in os.walk(ROOT_DIR):
        for file in files:
            if file.endswith('.html'):
                html_files.append(os.path.join(root, file))
                
    updated_count = 0
    
    for filepath in html_files:
        try:
            with open(filepath, 'r', encoding='utf-8') as f:
                content = f.read()
                
            original_content = content
            
            # Replace for desktop nav
            content = content.replace('>Services <svg', '>Solutions <svg')
            
            # Replace for mobile nav
            content = content.replace('<div class="m-section">Services</div>', '<div class="m-section">Solutions</div>')
            
            if content != original_content:
                with open(filepath, 'w', encoding='utf-8') as f:
                    f.write(content)
                rel_path = os.path.relpath(filepath, ROOT_DIR)
                print(f"✅ Updated nav bar in {rel_path}")
                updated_count += 1
                
        except Exception as e:
            print(f"Error processing {filepath}: {e}")

    print(f"\n--- Done! Updated {updated_count} files. ---")

if __name__ == "__main__":
    main()
