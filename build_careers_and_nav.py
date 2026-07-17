import os
import re
import glob

print("Starting to build careers.html and update global navigation...")

# 1. Read why-us.html as a template
template_file = 'why-us.html'
if not os.path.exists(template_file):
    print(f"Error: {template_file} not found!")
    exit(1)

with open(template_file, 'r', encoding='utf-8') as f:
    template_content = f.read()

# 2. Extract header and footer
# We split before the first <section class="why-us-hero">
header_split = template_content.split('<section class="why-us-hero">', 1)
if len(header_split) != 2:
    print("Error: Could not find <section class=\"why-us-hero\"> in template.")
    exit(1)
header_part = header_split[0]

# Replace title and description in header
header_part = header_part.replace('<title>Why Us | Vedtam Tech Solutions</title>', '<title>Careers | Vedtam Tech Solutions</title>')
header_part = header_part.replace('Discover why organizations trust Vedtam', 'Explore open positions and grow your career at Vedtam Tech Solutions. We put our people first and offer best-in-class benefits.')

# We split the second part to find the footer. The footer starts at <footer class="footer">
footer_split = header_split[1].split('<footer class="footer">', 1)
if len(footer_split) != 2:
    print("Error: Could not find <footer class=\"footer\"> in template.")
    exit(1)
footer_part = '<footer class="footer">' + footer_split[1]

# 3. Create the Careers specific CSS and Body Content
careers_style = """
  <style>
    /* Careers Custom Styles */
    .careers-hero {
      position: relative;
      padding: 160px 0 100px;
      overflow: hidden;
      background: #020617;
    }

    .careers-hero::before {
      content: '';
      position: absolute;
      top: -50%;
      left: -50%;
      width: 200%;
      height: 200%;
      background: radial-gradient(circle at center, rgba(0, 163, 217, 0.15) 0%, transparent 60%);
      pointer-events: none;
      animation: pulseGlow 8s infinite alternate;
    }

    @keyframes pulseGlow {
      0% { transform: scale(1); opacity: 0.8; }
      100% { transform: scale(1.1); opacity: 1; }
    }

    .careers-hero-content {
      position: relative;
      z-index: 2;
      text-align: center;
      max-width: 800px;
      margin: 0 auto;
    }

    .careers-hero-title {
      font-size: clamp(2.5rem, 5vw, 4rem);
      font-weight: 800;
      color: #fff;
      line-height: 1.1;
      margin-bottom: 1.5rem;
    }

    .careers-hero-title span {
      background: linear-gradient(90deg, #00A3D9, #2D9B4E);
      -webkit-background-clip: text;
      -webkit-text-fill-color: transparent;
    }

    .careers-hero-sub {
      font-size: 1.2rem;
      color: #cbd5e1;
      line-height: 1.6;
      margin-bottom: 2.5rem;
    }
    
    .btn-primary {
      display: inline-block;
      padding: 1rem 2rem;
      background: linear-gradient(90deg, #00A3D9, #2D9B4E);
      color: white;
      font-weight: 600;
      border-radius: 8px;
      text-decoration: none;
      transition: all 0.3s ease;
    }
    .btn-primary:hover {
      box-shadow: 0 10px 20px rgba(0, 163, 217, 0.3);
      transform: translateY(-2px);
      color: white;
    }

    .values-section {
      padding: 5rem 0;
      background: #050b14;
      border-top: 1px solid rgba(255,255,255,0.05);
    }
    
    .benefits-grid {
      display: grid;
      grid-template-columns: repeat(auto-fit, minmax(280px, 1fr));
      gap: 2rem;
      padding: 4rem 0;
    }

    .benefit-card {
      background: rgba(15, 23, 42, 0.6);
      border: 1px solid rgba(255, 255, 255, 0.05);
      border-radius: 16px;
      padding: 2.5rem;
      backdrop-filter: blur(12px);
      transition: all 0.4s ease;
      position: relative;
      overflow: hidden;
    }

    .benefit-card::before {
      content: '';
      position: absolute;
      top: 0;
      left: 0;
      width: 100%;
      height: 4px;
      background: linear-gradient(90deg, #00A3D9, #2D9B4E);
      transform: scaleX(0);
      transform-origin: left;
      transition: transform 0.4s ease;
    }

    .benefit-card:hover {
      transform: translateY(-5px);
      box-shadow: 0 20px 40px rgba(0, 0, 0, 0.3);
      border-color: rgba(0, 163, 217, 0.3);
    }
    .benefit-card:hover::before { transform: scaleX(1); }
    
    .benefit-title {
      font-size: 1.3rem;
      color: #fff;
      font-weight: 700;
      margin-bottom: 1rem;
    }

    .benefit-desc {
      color: #94a3b8;
      line-height: 1.6;
    }
    
    .cta-section {
      padding: 6rem 0;
      background: linear-gradient(rgba(2, 6, 23, 0.9), rgba(2, 6, 23, 0.9)), url('services_images/contact.jpg') center/cover;
      text-align: center;
      border-top: 1px solid rgba(255,255,255,0.05);
    }
  </style>
"""

# Replace the Custom Why Us Styles with Careers Styles
header_part = header_part.replace('/* Custom Why Us Styles */', '/* Careers Custom Styles */\n' + careers_style.split('/* Careers Custom Styles */')[1])

careers_body = """
  <section class="careers-hero">
    <div class="container">
      <div class="careers-hero-content">
        <h1 class="careers-hero-title">Start your journey. <br/><span>Grow your career</span> as we grow.</h1>
        <p class="careers-hero-sub">
          Join the team that’s changing IT services and securing the future of digital infrastructure.
        </p>
        <a class="btn-primary" href="#open-positions">Explore Open Positions</a>
      </div>
    </div>
  </section>

  <section class="values-section">
    <div class="container">
      <div style="max-width: 800px; margin: 0 auto; text-align: center;">
        <h2 style="font-size: 2.5rem; color: #fff; margin-bottom: 1.5rem;">People First</h2>
        <p style="color: #cbd5e1; font-size: 1.2rem; line-height: 1.8; margin-bottom: 1.5rem;">
          “We put our people first.” It’s something a lot of companies say, but not a lot of companies do. Here at Vedtam Tech Solutions, it’s our most important core value.
        </p>
        <p style="color: #94a3b8; font-size: 1.1rem; line-height: 1.6;">
          We believe when we place a high value on our team’s happiness, work/life balance, and professional development, everybody wins—clients included.
        </p>
      </div>
    </div>
  </section>

  <section class="values-section" style="background: #020617;">
    <div class="container">
      <div style="text-align: center; margin-bottom: 3rem;">
        <h2 style="font-size: 2.5rem; color: #fff; margin-bottom: 1rem;">Vedtam is a place to grow</h2>
        <p style="color: #94a3b8; max-width: 700px; margin: 0 auto; line-height: 1.6;">
          Vedtam Tech Solutions is rapidly growing across the globe, providing exceptional levels of service to our clients. 
          You’ll work in smaller, fast-paced teams—making a difference to our clients and our company, every day. 
          When you’re ready to grow your career, we have a place for you here.
        </p>
      </div>
    </div>
  </section>

  <section class="values-section">
    <div class="container">
      <div style="text-align: center;">
        <h2 style="font-size: 2.5rem; color: #fff;">Best-in-class Benefits</h2>
      </div>
      <div class="benefits-grid">
        <div class="benefit-card">
          <h3 class="benefit-title">Paid Vacation</h3>
          <p class="benefit-desc">Four weeks paid vacation as a baseline for all employees, increasing with tenure.</p>
        </div>
        <div class="benefit-card">
          <h3 class="benefit-title">Competitive Insurance</h3>
          <p class="benefit-desc">Comprehensive coverage including vision, dental, disability, and life insurance options.</p>
        </div>
        <div class="benefit-card">
          <h3 class="benefit-title">Performance Bonuses</h3>
          <p class="benefit-desc">Company wide. Do great work, be rewarded for it—it’s that simple.</p>
        </div>
        <div class="benefit-card">
          <h3 class="benefit-title">401k & Retirement</h3>
          <p class="benefit-desc">We provide competitive company matching to help you save for the future.</p>
        </div>
        <div class="benefit-card">
          <h3 class="benefit-title">Training & Education</h3>
          <p class="benefit-desc">Internships, reimbursement for certs, a leadership training track, and continuous learning.</p>
        </div>
        <div class="benefit-card">
          <h3 class="benefit-title">Fun Events</h3>
          <p class="benefit-desc">Happy hours, get-togethers, and other fun team-building events throughout the year.</p>
        </div>
      </div>
    </div>
  </section>

  <section class="cta-section" id="open-positions">
    <div class="container">
      <h2 style="font-size: 3rem; color: #fff; margin-bottom: 1rem;">Explore Open Positions</h2>
      <p style="color: #cbd5e1; font-size: 1.2rem; margin-bottom: 2.5rem; max-width: 600px; margin-left: auto; margin-right: auto;">
        Come on board! Check out our current openings and take the next step in your career journey.
      </p>
      <a class="btn-primary" href="contact-us.html">Contact Us to Apply</a>
    </div>
  </section>

"""

# Write to careers.html
careers_full = header_part + careers_body + footer_part
with open('careers.html', 'w', encoding='utf-8') as f:
    f.write(careers_full)
print("Created careers.html successfully.")

# 4. Update the Company Mega-Menu in all .html files
html_files = glob.glob('**/*.html', recursive=True)

# The pattern to find the end of the Company mega-links-grid
# It contains:
# <a href="about-us.html">About Us</a>
# <a class="active" href="why-us.html">Why Us</a>
# ...
# We want to insert the Careers link right before the closing </div> of that specific grid, or right after "blog.html"
link_to_insert = '\n                    <a href="careers.html">Careers</a>'
link_to_insert_active = '\n                    <a class="active" href="careers.html">Careers</a>'

# Adjusted link paths for nested files based on depth
def get_link_path(filepath):
    depth = len(os.path.normpath(filepath).split(os.sep)) - 1
    prefix = '../' * depth
    return f'\n                    <a href="{prefix}careers.html">Careers</a>'

updated_count = 0
for filepath in html_files:
    if os.path.basename(filepath) == 'careers.html':
        continue
    
    with open(filepath, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # We look for the blog link in the Company mega-menu to inject after it.
    # The blog link might look like: <a href="blog.html">Blog</a>
    # Or in a subfolder: <a href="../blog.html">Blog</a>
    # It is right before the closing </div> of the mega-links-grid.
    # To be safe, we use a regex to match the Blog link in the mega menu
    blog_pattern = re.compile(r'(<a[^>]*href="(?:\.\./)*blog\.html"[^>]*>Blog</a>)')
    
    # Check if careers is already added
    if 'Careers</a>' in content:
        continue
        
    depth = len(os.path.normpath(filepath).split(os.sep)) - 1
    prefix = '../' * depth
    new_link = f'\n                    <a href="{prefix}careers.html">Careers</a>'
    
    if blog_pattern.search(content):
        new_content = blog_pattern.sub(r'\1' + new_link, content)
        with open(filepath, 'w', encoding='utf-8') as f:
            f.write(new_content)
        updated_count += 1
        print(f"Updated {filepath}")

# Finally, for careers.html, we need to make its own link active!
with open('careers.html', 'r', encoding='utf-8') as f:
    careers_content = f.read()

# Since we generated it from why-us.html, we need to:
# 1. Add Careers link
# 2. Move .active from why-us.html to careers.html
careers_content = re.sub(r'<a class="active" href="why-us\.html">', r'<a href="why-us.html">', careers_content)
# Add active careers link after blog
careers_content = re.sub(r'(<a[^>]*href="(?:\.\./)*blog\.html"[^>]*>Blog</a>)', r'\1' + '\n                    <a class="active" href="careers.html">Careers</a>', careers_content)

with open('careers.html', 'w', encoding='utf-8') as f:
    f.write(careers_content)

print(f"\\nAll done! Successfully created careers.html and updated {updated_count} files with the navigation link.")
