import re

try:
    with open(r'c:\Users\Manu\Downloads\new-vedtam (1)\new-vedtam\assets\css\vedtam.css', 'r', encoding='utf-8') as f:
        css = f.read()

    # Find all CSS rules containing 'hero'
    rules = re.findall(r'([^{}]*?hero[^{}]*?{[^{}]*?})', css)
    
    with open('hero_rules.css', 'w', encoding='utf-8') as f:
        for rule in rules:
            f.write(rule + '\n')
            
    print("Extracted", len(rules), "rules")
except Exception as e:
    print("Error:", e)
