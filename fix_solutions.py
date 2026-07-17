import os

# Paths
root_file = "solutions.html"
index_file = "solutions/index.html"

# Make sure the source file exists
if not os.path.exists(root_file):
    print(f"Error: {root_file} not found!")
    exit(1)

with open(root_file, "r", encoding="utf-8") as f:
    content = f.read()

# List of prefixes that need to be adjusted for being one folder deep
# We are replacing root-level relative paths with ../ paths
replacements = {
    'href="assets/': 'href="../assets/',
    'src="assets/': 'src="../assets/',
    'href="card_logo/': 'href="../card_logo/',
    'src="card_logo/': 'src="../card_logo/',
    'href="services_images/': 'href="../services_images/',
    'src="services_images/': 'src="../services_images/',
    'href="consulting_images/': 'href="../consulting_images/',
    'src="consulting_images/': 'src="../consulting_images/',
    'href="industry_images/': 'href="../industry_images/',
    'src="industry_images/': 'src="../industry_images/',
    'href="Vedtam%20Logo%20favicon.png"': 'href="../Vedtam%20Logo%20favicon.png"',
    'src="Vedtam%20Logo%20favicon.png"': 'src="../Vedtam%20Logo%20favicon.png"',
    'href="index.html"': 'href="../index.html"',
    'href="about-us.html"': 'href="../about-us.html"',
    'href="why-us.html"': 'href="../why-us.html"',
    'href="client-success-portfolio.html"': 'href="../client-success-portfolio.html"',
    'href="blog.html"': 'href="../blog.html"',
    'href="careers.html"': 'href="../careers.html"',
    'href="contact-us.html"': 'href="../contact-us.html"',
    'href="solutions.html"': 'href="../solutions.html"',
    'href="cert-advisory.html"': 'href="../cert-advisory.html"',
    'href="privacy-policy.html"': 'href="../privacy-policy.html"',
    'href="terms-of-service.html"': 'href="../terms-of-service.html"',
    
    # Also adjust solutions and consulting links to correctly point to their folders
    'href="solutions/': 'href="../solutions/',
    'href="consulting/': 'href="../consulting/'
}

# Apply replacements
for old, new in replacements.items():
    content = content.replace(old, new)

# Write to solutions/index.html
with open(index_file, "w", encoding="utf-8") as f:
    f.write(content)

print(f"Successfully copied and fixed links from {root_file} into {index_file}!")
