import json
from bs4 import BeautifulSoup

html_path = r'C:\Users\Manu\.gemini\antigravity-ide\brain\c51cc468-df70-481b-afd3-cc5ca5b5639d\.system_generated\steps\5\content.md'
html_content = open(html_path, 'r', encoding='utf-8').read()

soup = BeautifulSoup(html_content, 'html.parser')

text = soup.get_text(separator='\n', strip=True)

with open(r'c:\Users\Manu\Desktop\vedtam website\extracted_text.txt', 'w', encoding='utf-8') as f:
    f.write(text)
