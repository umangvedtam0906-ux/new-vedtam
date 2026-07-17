import sys
import os

filepath = r"c:\Users\Manu\Desktop\vedtam website\vedtam.css"
with open(filepath, 'r', encoding='utf-8') as f:
    lines = f.readlines()

with open(filepath, 'w', encoding='utf-8') as f:
    f.writelines(lines[:29549])

print("Reverted successfully")
