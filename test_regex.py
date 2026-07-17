import re

YEAR_FILTER = ""
url_pattern = re.compile(
    rf"(?:href|HREF)\s*=\s*[\"']([^\"']*(?:s2cMainServlet\?[^\"']*(?:CIVN|CIAD|CICA)-\d{{4}}-|(?:CIVN|CIAD|CICA)-\d{{4}}-)[^\"']+)[\"']",
    re.IGNORECASE
)

test_html = '''<a href="s2cMainServlet?pageid=PUBWEL01&year=2026&CIVN=CIVN-2026-0001">Test</a>
<a href="javascript:callPage('VulnerabilityNote', 'CIVN-2026-0001')">Test2</a>
'''

print(url_pattern.findall(test_html))

js_pattern = re.compile(
    rf"callPage\s*\(\s*['\"](VulnerabilityNote|Advisory|CurrentActivities)['\"]\s*,\s*['\"]((?:CIVN|CIAD|CICA)-\d{{4}}-[^'\"]+)['\"]\s*\)",
    re.IGNORECASE
)
print(js_pattern.findall(test_html))
