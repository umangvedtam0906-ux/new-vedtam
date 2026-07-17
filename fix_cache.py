import os
import glob

def bust_cache():
    # Define the directory to search
    target_dir = r"c:\Users\Manu\Desktop\vedtam website"
    
    # Find all HTML files recursively
    html_files = glob.glob(os.path.join(target_dir, "**", "*.html"), recursive=True)
    
    count = 0
    for file_path in html_files:
        try:
            with open(file_path, 'r', encoding='utf-8') as f:
                content = f.read()
            
            # Check if it contains the script tag
            if 'src="assets/js/vedtam.js"' in content:
                new_content = content.replace('src="assets/js/vedtam.js"', 'src="assets/js/vedtam.js?v=2"')
                
                # Check for absolute paths too (just in case)
                new_content = new_content.replace('src="/assets/js/vedtam.js"', 'src="/assets/js/vedtam.js?v=2"')
                new_content = new_content.replace('src="../assets/js/vedtam.js"', 'src="../assets/js/vedtam.js?v=2"')
                
                with open(file_path, 'w', encoding='utf-8') as f:
                    f.write(new_content)
                count += 1
                
        except Exception as e:
            print(f"Error processing {file_path}: {e}")
            
    print(f"Successfully updated script tags in {count} HTML files to fix the cache issue.")

if __name__ == "__main__":
    bust_cache()
