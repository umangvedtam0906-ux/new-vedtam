import os
import re

base_dir = r"c:\Users\Manu\Downloads\new-vedtam-main (7)\new-vedtam"

# 1. Create the new blog post
with open(os.path.join(base_dir, "blog", "iso-27001-vs-soc-2.html"), "r", encoding="utf-8") as f:
    template_html = f.read()

# Replace metadata
template_html = template_html.replace(
    "<title>ISO 27001 vs SOC 2: Which Certification Does Your Business Need? | Vedtam</title>",
    "<title>How Long Does ISO 27001 Certification Take? | Vedtam</title>"
)
template_html = template_html.replace(
    '<meta content="Compare ISO 27001 and SOC 2 certifications to determine which is right for your business  covering scope, cost, timeline, and market requirements." name="description"/>',
    '<meta content="A realistic breakdown of the ISO 27001 certification timeline for small, medium, and large Indian organisations — with key milestones and time-saving tips." name="description"/>'
)
template_html = template_html.replace(
    '<link href="https://vedtam.com/blog/iso-27001-vs-soc-2" rel="canonical"/>',
    '<link href="https://vedtam.com/blog/iso-27001-certification-timeline" rel="canonical"/>'
)
template_html = template_html.replace(
    '<meta content="https://vedtam.com/blog-iso-27001-vs-soc-2" property="og:url"/>',
    '<meta content="https://vedtam.com/blog/iso-27001-certification-timeline" property="og:url"/>'
)
template_html = template_html.replace(
    '<meta content="ISO 27001 vs SOC 2: Which Certification Does Your Business Need?" property="og:title"/>',
    '<meta content="How Long Does ISO 27001 Certification Take?" property="og:title"/>'
)
template_html = template_html.replace(
    '<meta content="Compare ISO 27001 and SOC 2 certifications to determine which is right for your business  covering scope, cost, timeline, and market requirements." property="og:description"/>',
    '<meta content="A realistic breakdown of the ISO 27001 certification timeline for small, medium, and large Indian organisations — with key milestones and time-saving tips." property="og:description"/>'
)
template_html = template_html.replace(
    '<meta content="ISO 27001 vs SOC 2: Which Certification Does Your Business Need?" name="twitter:title"/>',
    '<meta content="How Long Does ISO 27001 Certification Take?" name="twitter:title"/>'
)
template_html = template_html.replace(
    '<meta content="Compare ISO 27001 and SOC 2 certifications to determine which is right for your business  covering scope, cost, timeline, and market requirements." name="twitter:description"/>',
    '<meta content="A realistic breakdown of the ISO 27001 certification timeline for small, medium, and large Indian organisations — with key milestones and time-saving tips." name="twitter:description"/>'
)

# Replace Hero
template_html = template_html.replace(
    '<h1 class="hero-title reveal" style="margin-bottom: 1rem; font-size: 3.5rem;">ISO 27001 vs SOC 2: <span class="gradient-text">Which Certification</span> Does Your Business Need?</h1>',
    '<h1 class="hero-title reveal" style="margin-bottom: 1rem; font-size: 3.5rem;">How Long Does <span class="gradient-text">ISO 27001 Certification</span> Take?</h1>'
)
template_html = template_html.replace(
    '<span>4 Min Read</span>',
    '<span>5 Min Read</span>'
)

# Replace Content
content_pattern = r'<div class="article-container reveal">.*?</div>\s*</div>\s*</section>'
new_content = """<div class="article-container reveal">
<p>One of the most common questions organisations ask before embarking on ISO 27001 certification is: how long will this take? The honest answer is: it depends — but most Indian SMEs should plan for 6–12 months for a first certification, while larger enterprises with complex environments may take 12–18 months.</p>
<p>This article breaks down the timeline realistically, milestone by milestone, and explains the key factors that determine how fast or slow your certification journey will be.</p>

<h2>Typical ISO 27001 Timeline by Organisation Size</h2>
<table class="article-table">
  <thead>
    <tr>
      <th>Phase</th>
      <th>Small Org (≤50 staff)</th>
      <th>Medium Org (50–500 staff)</th>
      <th>Large Org (500+ staff)</th>
    </tr>
  </thead>
  <tbody>
    <tr>
      <td>Gap Assessment</td>
      <td>1–2 weeks</td>
      <td>2–4 weeks</td>
      <td>4–6 weeks</td>
    </tr>
    <tr>
      <td>Risk Assessment</td>
      <td>2–3 weeks</td>
      <td>3–5 weeks</td>
      <td>5–8 weeks</td>
    </tr>
    <tr>
      <td>Control Implementation</td>
      <td>4–8 weeks</td>
      <td>8–16 weeks</td>
      <td>16–24 weeks</td>
    </tr>
    <tr>
      <td>Documentation</td>
      <td>3–5 weeks</td>
      <td>5–8 weeks</td>
      <td>8–12 weeks</td>
    </tr>
    <tr>
      <td>Training &amp; Awareness</td>
      <td>1–2 weeks</td>
      <td>2–4 weeks</td>
      <td>4–6 weeks</td>
    </tr>
    <tr>
      <td>Internal Audit</td>
      <td>1–2 weeks</td>
      <td>2–3 weeks</td>
      <td>3–4 weeks</td>
    </tr>
    <tr>
      <td>Management Review</td>
      <td>1 week</td>
      <td>1 week</td>
      <td>1–2 weeks</td>
    </tr>
    <tr>
      <td>Stage 1 External Audit</td>
      <td>1–2 weeks</td>
      <td>1–2 weeks</td>
      <td>2–3 weeks</td>
    </tr>
    <tr>
      <td>Stage 2 External Audit</td>
      <td>1–2 weeks</td>
      <td>2–3 weeks</td>
      <td>3–4 weeks</td>
    </tr>
    <tr>
      <td><strong>TOTAL (typical)</strong></td>
      <td><strong>3–6 months</strong></td>
      <td><strong>6–12 months</strong></td>
      <td><strong>12–18 months</strong></td>
    </tr>
  </tbody>
</table>

<h2>Phase-by-Phase Timeline Breakdown</h2>
<h3>Phase 1: Project Initiation (Weeks 1–2)</h3>
<p>Obtain management commitment, appoint an ISMS project lead, define the certification scope, select a certification body, and build the project plan. This phase is often underestimated — aligning stakeholders and defining scope can take longer than expected in large organisations.</p>

<h3>Phase 2: Gap Assessment (Weeks 2–4)</h3>
<p>Conduct a gap assessment against ISO 27001 clauses 4–10 and all 93 Annex A controls. Document current state, identify gaps, and produce a prioritised remediation roadmap. The output drives the entire implementation plan.</p>

<h3>Phase 3: Risk Assessment (Weeks 4–8)</h3>
<p>This is the analytical core of ISO 27001. Identify information assets, assess threats and vulnerabilities, calculate risk levels, and document risk treatment decisions. The risk assessment must be completed before control selection can be finalised.</p>

<h3>Phase 4: Control Implementation (Weeks 6–20)</h3>
<p>The longest phase — implementing or strengthening security controls across organisational, people, physical, and technological domains. Common controls that take time include: access management, vulnerability management, supplier security assessment, and security monitoring. This phase often runs in parallel with documentation.</p>

<h3>Phase 5: Documentation (Weeks 8–18)</h3>
<p>ISO 27001 requires documented policies, procedures, and records. Mandatory documentation includes the ISMS scope, information security policy, risk assessment methodology, Statement of Applicability, risk treatment plan, and control implementation evidence. Quality matters more than quantity — auditors want evidence of actual practice, not paper policies.</p>

<h3>Phase 6: Training and Internal Audit (Weeks 14–20)</h3>
<p>Train all employees on relevant security policies and procedures. Conduct a formal internal audit against the standard — ideally led by someone independent of the ISMS implementation team. Resolve all identified non-conformities before the external audit.</p>

<h3>Phase 7: External Audit (Weeks 18–24+)</h3>
<p>Stage 1 (document review) typically takes 1–2 days. Stage 2 (implementation audit) takes 1–5 days depending on organisation size. Allow 4–8 weeks between Stage 1 and Stage 2 to address any Stage 1 findings.</p>

<h2>Key Factors That Affect Your Timeline</h2>
<h3>Factors That Speed Up Certification</h3>
<ul>
  <li><strong>Existing security maturity</strong> — if you already have strong security practices, the gap is smaller</li>
  <li><strong>Dedicated project team</strong> — having people focused on ISO 27001 rather than fitting it around day jobs</li>
  <li><strong>Experienced consultant</strong> — a consultant who has run many certifications knows exactly what auditors want</li>
  <li><strong>Narrow scope</strong> — certifying a specific service or system rather than the entire organisation</li>
  <li><strong>Management commitment</strong> — quick decision-making at the top eliminates delays</li>
</ul>

<h3>Factors That Slow Down Certification</h3>
<ul>
  <li><strong>Limited internal resources</strong> — most organisations underestimate the effort required from staff</li>
  <li><strong>Complex IT environment</strong> — more systems mean more controls to implement and more evidence to collect</li>
  <li><strong>Multiple locations</strong> — additional audit time and logistics</li>
  <li><strong>High staff turnover during the project</strong> — losing key personnel mid-implementation is common and costly</li>
  <li><strong>Audit scheduling delays</strong> — certification bodies often have 4–8 week waiting lists</li>
</ul>

<h2>Can You Fast-Track ISO 27001 Certification?</h2>
<p>Some organisations ask about achieving ISO 27001 certification in 90 days or less. This is technically possible in very specific circumstances — a small organisation with a narrow scope, strong existing security controls, and a consultant who can drive the process intensively. But for most Indian enterprises, it is not realistic and attempting to rush the process risks creating a paper ISMS that fails the audit or fails to improve actual security.</p>
<p>The fastest path to certification is not rushing — it is starting with a high-quality gap assessment that creates a focused, achievable implementation plan. Vedtam's structured approach typically reduces certification timelines by 20–30% compared to unguided efforts.</p>

<div style="margin-top: 3rem; padding: 2rem; background: rgba(0, 163, 217, 0.1); border-left: 4px solid #00a3d9; border-radius: 4px;">
  <h3 style="margin-top: 0;">How Vedtam Can Help</h3>
  <p style="margin-bottom: 1rem;">Vedtam's ISO 27001 consultants have guided organisations of all sizes through certification. We provide a realistic timeline assessment, manage the project plan, build the documentation framework, prepare you for auditor questions, and support you through both stages of the external audit.</p>
  <a href="../consulting/iso-consulting-services.html" style="color: #00a3d9; font-weight: bold; text-decoration: none;">Explore ISO Consulting Services &rarr;</a>
  <br><br>
  <p style="margin-bottom: 0;">Get a realistic ISO 27001 timeline for your organisation. Free consultation: <a href="../contact-us.html" style="color: #00a3d9; text-decoration: none;">vedtam.com/contact-us</a> | <a href="tel:+917065111015" style="color: #00a3d9; text-decoration: none;">+91 70651 11015</a></p>
</div>
</div>
</div>
</section>"""

template_html = re.sub(content_pattern, new_content, template_html, flags=re.DOTALL)

with open(os.path.join(base_dir, "blog", "iso-27001-certification-timeline.html"), "w", encoding="utf-8") as f:
    f.write(template_html)

print("Blog post created successfully!")

# 2. Add blog post to blog.html and blog/index.html
def add_to_blog_index(file_path, image_prefix):
    with open(file_path, "r", encoding="utf-8") as f:
        content = f.read()
    
    new_card = f"""<!-- Post New -->
<article class="tm-card-premium" style="text-align: left; padding: 2rem; display: flex; flex-direction: column;">
<div style="height: 200px; background: rgba(0,0,0,0.3); border-radius: 8px; margin-bottom: 1.5rem; overflow: hidden; display: flex; align-items: center; justify-content: center; border: 1px solid rgba(255,255,255,0.05);">
<img src="{image_prefix}blog Image/ISO 27001 Timeline.png" alt="ISO 27001 Timeline" style="width: 100%; height: 100%; object-fit: cover;" />
</div>
<div style="font-size: 0.85rem; color: #64748b; margin-bottom: 0.5rem; text-transform: uppercase; letter-spacing: 1px;">Compliance  | Apr 12, 2026</div>
<h3 style="font-size: 1.5rem; color: #fff; margin-bottom: 1rem; line-height: 1.3;">How Long Does ISO 27001 Certification Take?</h3>
<p class="tm-text" style="text-align: left; margin-bottom: 1.5rem; flex-grow: 1;">A realistic breakdown of the ISO 27001 certification timeline for small, medium, and large Indian organisations — with key milestones and time-saving tips.</p>
<a class="tm-name" href="{'' if image_prefix == '../' else 'blog/'}iso-27001-certification-timeline.html" style="text-decoration: none; display: inline-flex; align-items: center; gap: 0.5rem; padding-top: 1rem; border-top: 1px solid rgba(255,255,255,0.1); width: 100%;">Read Article <span style="font-size:1.2rem;">&rarr;</span></a>
</article>
"""
    # Find where to insert (before <!-- Post 1 -->)
    content = content.replace("<!-- Post 1 -->", new_card + "<!-- Post 1 -->")
    
    with open(file_path, "w", encoding="utf-8") as f:
        f.write(content)

add_to_blog_index(os.path.join(base_dir, "blog.html"), "")
add_to_blog_index(os.path.join(base_dir, "blog", "index.html"), "../")

print("Blog indexes updated successfully!")
