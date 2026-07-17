import os

files_to_update = [
    ("blog.html", "blog Image"),
    ("blog/index.html", "../blog Image")
]

svgs = [
    '<svg fill="none" height="48" stroke="rgba(255,255,255,0.15)" stroke-width="2" viewbox="0 0 24 24" width="48"><rect height="18" rx="2" ry="2" width="18" x="3" y="3"></rect><circle cx="8.5" cy="8.5" r="1.5"></circle><polyline points="21 15 16 10 5 21"></polyline></svg>',
    '<svg fill="none" height="48" stroke="rgba(255,255,255,0.15)" stroke-width="2" viewbox="0 0 24 24" width="48"><path d="M21 16V8a2 2 0 0 0-1-1.73l-7-4a2 2 0 0 0-2 0l-7 4A2 2 0 0 0 3 8v8a2 2 0 0 0 1 1.73l7 4a2 2 0 0 0 2 0l7-4A2 2 0 0 0 21 16z"></path><polyline points="3.27 6.96 12 12.01 20.73 6.96"></polyline><line x1="12" x2="12" y1="22.08" y2="12"></line></svg>',
    '<svg fill="none" height="48" stroke="rgba(255,255,255,0.15)" stroke-width="2" viewbox="0 0 24 24" width="48"><path d="M14 2H6a2 2 0 0 0-2 2v16a2 2 0 0 0 2 2h12a2 2 0 0 0 2-2V8z"></path><polyline points="14 2 14 8 20 8"></polyline><line x1="16" x2="8" y1="13" y2="13"></line><line x1="16" x2="8" y1="17" y2="17"></line><polyline points="10 9 9 9 8 9"></polyline></svg>',
    '<svg fill="none" height="48" stroke="rgba(255,255,255,0.15)" stroke-width="2" viewbox="0 0 24 24" width="48"><path d="M21.21 15.89A10 10 0 1 1 8 2.83"></path><path d="M22 12A10 10 0 0 0 12 2v10z"></path></svg>',
    '<svg fill="none" height="48" stroke="rgba(255,255,255,0.15)" stroke-width="2" viewbox="0 0 24 24" width="48"><rect height="14" rx="2" ry="2" width="20" x="2" y="3"></rect><line x1="8" x2="16" y1="21" y2="21"></line><line x1="12" x2="12" y1="17" y2="21"></line></svg>',
    '<svg fill="none" height="48" stroke="rgba(255,255,255,0.15)" stroke-width="2" viewbox="0 0 24 24" width="48"><path d="M12 22s8-4 8-10V5l-8-3-8 3v7c0 6 8 10 8 10z"></path></svg>'
]

images = [
    "ISO 27001 vs SOC 2.png",
    "Zero Trust Cloud Architecture.png",
    "ISO 27001 Certification Step-by-Step Guide for Indian Companies.png",
    "How to Appoint a DPO.png",
    "DPDP Act Penalties.png",
    "DPDP Act vs GDPR Key Differences.png"
]

for file_path, img_prefix in files_to_update:
    abs_path = os.path.join(r"c:\Users\Manu\Downloads\new-vedtam-main (3)\new-vedtam-main", file_path)
    if not os.path.exists(abs_path):
        print(f"File not found: {abs_path}")
        continue
    
    with open(abs_path, 'r', encoding='utf-8') as f:
        content = f.read()
        
    for i in range(len(svgs)):
        img_tag = f'<img src="{img_prefix}/{images[i]}" alt="Blog image {i}" style="width: 100%; height: 100%; object-fit: cover;" />'
        content = content.replace(svgs[i], img_tag)
        
    with open(abs_path, 'w', encoding='utf-8') as f:
        f.write(content)
        print(f"Updated {file_path}")
