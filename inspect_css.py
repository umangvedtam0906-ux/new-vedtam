import re

with open("vedtam.css", "r", encoding="utf-8", errors="replace") as f:
    content = f.read()

media_queries = re.findall(r'@media[^{]+', content)
print(f"Total media queries found: {len(media_queries)}")

for mq in media_queries:
    print(mq.strip())

hero_styles = re.findall(r'\.hero[^{]*\{[^}]+\}', content)
print(f"Total hero styles found: {len(hero_styles)}")
