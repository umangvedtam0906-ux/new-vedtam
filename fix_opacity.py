import os
import glob

base_dir = r"c:\Users\Manu\Downloads\new-vedtam-main (3)\new-vedtam-main"
html_files = glob.glob(os.path.join(base_dir, '**', '*.html'), recursive=True)

updated_count = 0
for file in html_files:
    try:
        with open(file, 'r', encoding='utf-8') as f:
            content = f.read()
            
        if 'opacity: 0; position: absolute;' in content:
            new_content = content.replace('opacity: 0; position: absolute;', 'position: absolute;')
            with open(file, 'w', encoding='utf-8') as f:
                f.write(new_content)
            print(f'Updated {file}')
            updated_count += 1
    except Exception as e:
        print(f"Error processing {file}: {e}")

print(f"Total files updated: {updated_count}")
