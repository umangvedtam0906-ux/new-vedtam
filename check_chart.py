import os

html_path = r"c:\Users\Manu\Downloads\vedtam-main (2) (1)\vedtam-main (9)\vedtam-main\index.html"
with open(html_path, "r", encoding="utf-8") as f:
    content = f.read()

print("chart in index?", "id=\"chart\"" in content)
print("latestSummary in index?", "latestSummary" in content)

