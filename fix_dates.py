import json
from datetime import datetime

with open('cert-data.json', 'r', encoding='utf-8') as f:
    data = json.load(f)

for item in data:
    if item.get('date'):
        raw_date = item['date'].strip().replace(',', '')
        try:
            item['date'] = datetime.strptime(raw_date, '%B %d %Y').strftime('%Y-%m-%d')
        except ValueError:
            try:
                # also try if it has no day like 'June 2026' or abbreviated 'Jun 11 2026'
                item['date'] = datetime.strptime(raw_date, '%b %d %Y').strftime('%Y-%m-%d')
            except ValueError:
                pass

with open('cert-data.json', 'w', encoding='utf-8') as f:
    json.dump(data, f, indent=4)
