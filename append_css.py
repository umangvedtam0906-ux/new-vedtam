import sys
css_to_append = """
.vciso-dashboard .dash-header {
  display: flex;
  align-items: center;
  width: 100%;
}

.vciso-dashboard .dash-header .dash-status,
.vciso-dashboard .dash-header .dash-meta {
  flex: 0 0 50%;
  width: 50%;
  display: flex;
  align-items: center;
}

.vciso-dashboard .dash-header .dash-meta {
  justify-content: flex-end;
  text-align: right;
}
"""

with open(r"c:\Users\Manu\Desktop\vedtam website\vedtam.css", "a", encoding="utf-8") as f:
    f.write(css_to_append)

print("CSS appended.")
