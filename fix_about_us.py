import os

filepath = r"c:\Users\Manu\Desktop\vedtam website\about-us.html" # This file is in the root
with open(filepath, "r", encoding="utf-8") as f:
    lines = f.readlines()

# find exactly where the first <body> tag starts after </head>
head_end = -1
for i, line in enumerate(lines):
    if "</head>" in line: # This is the correct </head>
        head_end = i
        break

# The messed up part starts at line 268 (index 267) and ends right before the real <body> (line 463, index 462)
# But let's verify programmatically to avoid line number shifting.
# Let's just find the second <body class="about-page home-page">
body_indices = []
for i, line in enumerate(lines):
    if "<body class=\"about-page home-page\">" in line: # This is the correct <body>
        body_indices.append(i)

if len(body_indices) == 2:
    start_del = body_indices[0]
    end_del = body_indices[1]
    
    new_lines = lines[:start_del] + lines[end_del:]
    with open(filepath, "w", encoding="utf-8") as f:
        f.writelines(new_lines)
    print(f"Fixed about-us.html by deleting {end_del - start_del} lines.")
else:
    print(f"Found {len(body_indices)} body tags. Did not modify.")
