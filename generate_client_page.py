import os

target_file = 'c:/Users/Manu/Desktop/vedtam website/client-success-portfolio.html' # This file is in the root
template_source = 'c:/Users/Manu/Desktop/vedtam website/about-us.html' # This file is in the root

with open(template_source, 'r', encoding='utf-8') as f:
    template = f.read()

# Extract header (up to <nav... )
head_end = template.find('</head>')
nav_start = template.find('<nav class="navbar"')
nav_end = template.find('<section class="hero')

# Extract footer
footer_start = template.find('<footer class="footer">')
contact_start = template.find('<section class="contact-premium-section"')
if contact_start == -1:
    contact_start = template.find('<section class="contact-section"')

# Generate head, replacing titles
head_section = template[:nav_start]
head_section = head_section.replace('<title>About Us - Vedtam Tech Solutions</title>', '<title>Client Success & Portfolio - Vedtam Tech Solutions</title>')
head_section = head_section.replace('content="Learn about Vedtam Tech Solutions', 'content="Client Success & Portfolio - Vedtam Tech Solutions')
head_section = head_section.replace('About Us — Vedtam Tech Solutions', 'Client Success & Portfolio — Vedtam Tech Solutions')
head_section = head_section.replace('about-us.html', 'client-success-portfolio.html')

# Generate nav
nav_section = template[nav_start:nav_end]
nav_section = nav_section.replace('class="active">About Us', '>About Us')

# Generate Hero
hero_section = """
  <section class="hero about-hero" style="min-height: 50vh; display: flex; align-items: center; justify-content: center; text-align: center; padding-top: 120px; padding-bottom: 60px;">
    <div class="hero-bg"></div>
    <div class="hero-grid"></div>
    <div class="hero-glow"></div>
    <div class="container">
      <div class="hero-shell" style="flex-direction: column; align-items: center;">
        <div class="hero-content" style="max-width: 900px; text-align: center; margin: 0 auto; display: flex; flex-direction: column; align-items: center;">
          <h1 class="hero-title" style="font-size: clamp(2.5rem, 5vw, 4.375rem); line-height: 1.1; margin-bottom: 24px;">Client Success & <span class="line2">Portfolio</span></h1>
          <p class="hero-sub" style="font-size: 1.125rem; line-height: 1.6; max-width: 800px; margin: 0 auto;">Delivering measurable results for enterprises, startups, and public sector organizations through innovative IT, cybersecurity, and digital solutions.</p>
        </div>
      </div>
    </div>
  </section>
"""

# Generate Portfolio Grid
logos_dir = 'c:/Users/Manu/Desktop/vedtam website/assets/images/vedtam TESTIMONIAL'
logos = [f for f in os.listdir(logos_dir) if f.endswith(('.png', '.jpg', '.jpeg', '.webp'))]
# Sort numerically if possible
def sort_key(x):
    try:
        return int(x.split('.')[0])
    except ValueError:
        return x
logos.sort(key=sort_key)

grid_items = ""
for logo in logos:
    grid_items += f'''
        <div class="client-logo-item" style="background: rgba(12, 21, 36, 0.6); border: 1px solid rgba(8, 68, 129, 0.3); border-radius: 16px; padding: 2rem; display: flex; align-items: center; justify-content: center; transition: all 0.3s ease;" onmouseover="this.style.transform='translateY(-5px)'; this.style.borderColor='rgba(0, 163, 217, 0.8)';" onmouseout="this.style.transform='none'; this.style.borderColor='rgba(8, 68, 129, 0.3)';">
            <img src="vedtam TESTIMONIAL/{logo}" alt="Client Logo" style="max-width: 100%; max-height: 100px; object-fit: contain;">
        </div>
'''

portfolio_section = f"""
  <section class="portfolio-section" style="padding: 5rem 0; background: var(--black);">
    <div class="container">
      <div class="portfolio-header text-center" style="max-width: 800px; margin: 0 auto 4rem; text-align: center;">
        <div class="section-label" style="display:inline-block; padding:0.4rem 1.2rem; background:rgba(0, 163, 217, 0.1); border:1px solid rgba(0, 163, 217, 0.3); border-radius:50px; color:var(--cyan); font-weight:700; font-size:0.85rem; text-transform:uppercase; letter-spacing:1px; margin-bottom:1rem;">Client Portfolio</div>
        <h2 class="section-heading" style="font-size:clamp(1.6rem, 3.2vw, 2.4rem); margin-bottom:1rem; line-height:1.2;">Trusted by <span style="background:linear-gradient(135deg, #00A3D9 0%, #2D9B4E 100%); -webkit-background-clip:text; background-clip:text; color:transparent">Visionary Organizations</span></h2>
        <p class="section-sub" style="font-size:1.05rem; color:var(--off); margin:0; line-height:1.7;">From ambitious startups to global enterprises, we partner with visionary organizations across industries to drive digital transformation and sustainable growth.</p>
      </div>

      <div class="portfolio-grid" style="display: grid; grid-template-columns: repeat(auto-fill, minmax(200px, 1fr)); gap: 2rem;">
{grid_items}
      </div>
    </div>
  </section>
"""

# Extract contact and footer from template
contact_and_footer = template[contact_start:] if contact_start != -1 else template[footer_start:]

html_content = head_section + nav_section + hero_section + portfolio_section + contact_and_footer

with open(target_file, 'w', encoding='utf-8') as f:
    f.write(html_content)

print(f"Successfully created {target_file}")
