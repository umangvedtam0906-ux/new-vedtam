import re

html_files = [
    r"C:\Users\Manu\Downloads\new-vedtam-main (7)\new-vedtam\solutions.html",
    r"C:\Users\Manu\Downloads\new-vedtam-main (7)\new-vedtam\consulting.html",
    r"C:\Users\Manu\Downloads\new-vedtam-main (7)\new-vedtam\solutions-and-consulting.html"
]

pattern = r'src="file:///C:/Users/Manu/.gemini/antigravity-ide/brain/[a-zA-Z0-9\-]+/(.*?_\d+)\.png"'

def replacement(match):
    filename = match.group(1)
    # Remove the timestamp part: e.g. cybersecurity_banner_1782298175641 -> cybersecurity_banner
    clean_name = re.sub(r'_\d{13}$', '', filename)
    return f'src="images/solutions/{clean_name}.png"'

for file_path in html_files:
    try:
        with open(file_path, "r", encoding="utf-8") as f:
            content = f.read()
        
        new_content = re.sub(pattern, replacement, content)
        
        with open(file_path, "w", encoding="utf-8") as f:
            f.write(new_content)
        print(f"Updated {file_path}")
    except Exception as e:
        print(f"Error processing {file_path}: {e}")
