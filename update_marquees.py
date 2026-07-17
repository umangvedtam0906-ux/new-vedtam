import sys

filepath = r"c:\Users\Manu\Downloads\new-vedtam\new-vedtam\index.html"

try:
    with open(filepath, "r", encoding="utf-8") as f:
        content = f.read()
except FileNotFoundError:
    print("File not found.")
    sys.exit(1)

new_css = """
<style>
/* Modern Glass Marquee for Technology Partners */
.premium-tech-container {
    position: relative;
    padding: 6rem 0;
    background: radial-gradient(circle at center, #0a0a0f 0%, #050508 100%);
    overflow: hidden;
    border-top: 1px solid rgba(0, 195, 255, 0.1);
    border-bottom: 1px solid rgba(0, 195, 255, 0.1);
}

.premium-tech-container::before {
    content: '';
    position: absolute;
    top: -50%; left: -50%; width: 200%; height: 200%;
    background: radial-gradient(circle, rgba(0, 195, 255, 0.03) 0%, transparent 60%);
    pointer-events: none;
}

.premium-tech-header {
    text-align: center;
    margin-bottom: 3rem;
    position: relative;
    z-index: 2;
}

.premium-tech-header .section-label {
    color: #00c3ff;
    font-weight: 700;
    letter-spacing: 3px;
    text-transform: uppercase;
    font-size: 0.85rem;
}

.tech-marquee-wrapper {
    position: relative;
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    z-index: 2;
    transform: rotate(-1deg) scale(1.05);
}

.tech-marquee-track {
    display: flex;
    width: max-content;
    animation: scrollTech 40s linear infinite;
    gap: 1.5rem;
}

.tech-marquee-track.reverse {
    animation: scrollTechReverse 45s linear infinite;
}

.tech-marquee-wrapper:hover .tech-marquee-track {
    animation-play-state: paused;
}

.tech-item {
    background: rgba(15, 23, 42, 0.4);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.05);
    border-radius: 16px;
    padding: 1.5rem 2.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
    min-width: 200px;
    height: 90px;
    transition: all 0.4s ease;
    cursor: pointer;
}

.tech-item img {
    max-height: 40px;
    max-width: 140px;
    filter: grayscale(100%) brightness(200%);
    transition: all 0.4s ease;
    opacity: 0.6;
}

.tech-item:hover {
    border-color: rgba(0, 195, 255, 0.5);
    background: rgba(0, 195, 255, 0.05);
    box-shadow: 0 0 30px rgba(0, 195, 255, 0.15), inset 0 0 10px rgba(0, 195, 255, 0.1);
    transform: translateY(-5px);
}

.tech-item:hover img {
    filter: grayscale(0%) brightness(100%);
    opacity: 1;
}

@keyframes scrollTech {
    0% { transform: translateX(0); }
    100% { transform: translateX(-50%); }
}

@keyframes scrollTechReverse {
    0% { transform: translateX(-50%); }
    100% { transform: translateX(0); }
}

/* Wall of Trust for Clients */
.premium-client-container {
    padding: 6rem 0;
    background: #050b14;
    position: relative;
    overflow: hidden;
}

.client-cloud-wrapper {
    position: relative;
    max-width: 1200px;
    margin: 0 auto;
    padding: 2rem 0;
}

.client-cloud-grid {
    display: flex;
    flex-wrap: wrap;
    justify-content: center;
    gap: 1.5rem;
    padding: 0 1rem;
}

.client-cloud-item {
    background: #ffffff;
    border-radius: 12px;
    padding: 1.5rem;
    display: flex;
    align-items: center;
    justify-content: center;
    width: 180px;
    height: 100px;
    box-shadow: 0 4px 20px rgba(0,0,0,0.2);
    transition: all 0.5s cubic-bezier(0.4, 0, 0.2, 1);
    animation: floatClient 6s ease-in-out infinite;
}

/* Add delays to make them float randomly */
.client-cloud-item:nth-child(even) { animation-delay: 1s; animation-duration: 7s; }
.client-cloud-item:nth-child(3n) { animation-delay: 2s; animation-duration: 5s; }
.client-cloud-item:nth-child(4n) { animation-delay: 0.5s; animation-duration: 8s; }

.client-cloud-item img {
    max-width: 100%;
    max-height: 100%;
    object-fit: contain;
    transition: transform 0.4s ease;
}

.client-cloud-item:hover {
    transform: scale(1.1) translateY(-10px) !important;
    box-shadow: 0 15px 30px rgba(16, 185, 129, 0.2);
    animation-play-state: paused;
    z-index: 10;
}

.client-cloud-item:hover img {
    transform: scale(1.1);
}

@keyframes floatClient {
    0%, 100% { transform: translateY(0); }
    50% { transform: translateY(-10px); }
}
</style>
"""

tech_partners_html = """
      <!-- Premium Technology Partners Section -->
      <div class="premium-tech-container">
        <div class="premium-tech-header">
          <div class="section-label">Trusted Technology Partners</div>
        </div>
        <div class="tech-marquee-wrapper">
          <div class="tech-marquee-track">
            <!-- Track 1 Set 1 -->
            <div class="tech-item"><img alt="Microsoft" loading="lazy" src="Vedtam%20Partners/Microsoft.png" /></div>
            <div class="tech-item"><img alt="Lenovo" loading="lazy" src="Vedtam%20Partners/lenovo.png" /></div>
            <div class="tech-item"><img alt="HP" loading="lazy" src="Vedtam%20Partners/hp.png" /></div>
            <div class="tech-item"><img alt="Sophos" loading="lazy" src="Vedtam%20Partners/sophos.png" /></div>
            <div class="tech-item"><img alt="Dell" loading="lazy" src="Vedtam%20Partners/dell.png" /></div>
            <div class="tech-item"><img alt="Cisco" loading="lazy" src="Vedtam%20Partners/cisco.png" /></div>
            <div class="tech-item"><img alt="AWS" loading="lazy" src="Vedtam%20Partners/aws.png" /></div>
            <div class="tech-item"><img alt="Red Hat" loading="lazy" src="Vedtam%20Partners/red%20hat.png" /></div>
            <div class="tech-item"><img alt="Azure" loading="lazy" src="Vedtam%20Partners/azura.png" /></div>
            <div class="tech-item"><img alt="Qualys" loading="lazy" src="Vedtam%20Partners/qualys.png" /></div>
            <!-- Track 1 Set 2 -->
            <div class="tech-item"><img alt="Microsoft" loading="lazy" src="Vedtam%20Partners/Microsoft.png" /></div>
            <div class="tech-item"><img alt="Lenovo" loading="lazy" src="Vedtam%20Partners/lenovo.png" /></div>
            <div class="tech-item"><img alt="HP" loading="lazy" src="Vedtam%20Partners/hp.png" /></div>
            <div class="tech-item"><img alt="Sophos" loading="lazy" src="Vedtam%20Partners/sophos.png" /></div>
            <div class="tech-item"><img alt="Dell" loading="lazy" src="Vedtam%20Partners/dell.png" /></div>
            <div class="tech-item"><img alt="Cisco" loading="lazy" src="Vedtam%20Partners/cisco.png" /></div>
            <div class="tech-item"><img alt="AWS" loading="lazy" src="Vedtam%20Partners/aws.png" /></div>
            <div class="tech-item"><img alt="Red Hat" loading="lazy" src="Vedtam%20Partners/red%20hat.png" /></div>
            <div class="tech-item"><img alt="Azure" loading="lazy" src="Vedtam%20Partners/azura.png" /></div>
            <div class="tech-item"><img alt="Qualys" loading="lazy" src="Vedtam%20Partners/qualys.png" /></div>
          </div>
          
          <div class="tech-marquee-track reverse">
            <!-- Track 2 Set 1 -->
            <div class="tech-item"><img alt="Check Point" loading="lazy" src="Vedtam%20Partners/checkpoint.png" /></div>
            <div class="tech-item"><img alt="Commvault" loading="lazy" src="Vedtam%20Partners/commvault.png" /></div>
            <div class="tech-item"><img alt="Extreme Networks" loading="lazy" src="Vedtam%20Partners/extreme.png" /></div>
            <div class="tech-item"><img alt="Forcepoint" loading="lazy" src="Vedtam%20Partners/forcepoint.png" /></div>
            <div class="tech-item"><img alt="Fortinet" loading="lazy" src="Vedtam%20Partners/fortinet.png" /></div>
            <div class="tech-item"><img alt="Huawei" loading="lazy" src="Vedtam%20Partners/huawei.png" /></div>
            <div class="tech-item"><img alt="Jamf" loading="lazy" src="Vedtam%20Partners/jamf.png" /></div>
            <div class="tech-item"><img alt="Juniper" loading="lazy" src="Vedtam%20Partners/juniper.png" /></div>
            <div class="tech-item"><img alt="SonicWall" loading="lazy" src="Vedtam%20Partners/sonicwall.png" /></div>
            <div class="tech-item"><img alt="Palo Alto" loading="lazy" src="Vedtam%20Partners/paloalto.png" /></div>
            <!-- Track 2 Set 2 -->
            <div class="tech-item"><img alt="Check Point" loading="lazy" src="Vedtam%20Partners/checkpoint.png" /></div>
            <div class="tech-item"><img alt="Commvault" loading="lazy" src="Vedtam%20Partners/commvault.png" /></div>
            <div class="tech-item"><img alt="Extreme Networks" loading="lazy" src="Vedtam%20Partners/extreme.png" /></div>
            <div class="tech-item"><img alt="Forcepoint" loading="lazy" src="Vedtam%20Partners/forcepoint.png" /></div>
            <div class="tech-item"><img alt="Fortinet" loading="lazy" src="Vedtam%20Partners/fortinet.png" /></div>
            <div class="tech-item"><img alt="Huawei" loading="lazy" src="Vedtam%20Partners/huawei.png" /></div>
            <div class="tech-item"><img alt="Jamf" loading="lazy" src="Vedtam%20Partners/jamf.png" /></div>
            <div class="tech-item"><img alt="Juniper" loading="lazy" src="Vedtam%20Partners/juniper.png" /></div>
            <div class="tech-item"><img alt="SonicWall" loading="lazy" src="Vedtam%20Partners/sonicwall.png" /></div>
            <div class="tech-item"><img alt="Palo Alto" loading="lazy" src="Vedtam%20Partners/paloalto.png" /></div>
          </div>
        </div>
      </div>
"""

our_clients_html = """
  <!-- Premium Our Clients Section -->
  <section class="premium-client-container">
    <div class="container">
      <div class="industries-header-v2 reveal">
        <div class="section-label" style="color: #10b981;">Trusted By Our Clients</div>
        <h2>Enterprise Partnerships <span>You Can Rely On</span></h2>
      </div>
      <div class="client-cloud-wrapper reveal">
        <div class="client-cloud-grid">
          <div class="client-cloud-item"><img alt="Client" loading="lazy" src="vedtam%20TESTIMONIAL/1.png" /></div>
          <div class="client-cloud-item"><img alt="Client" loading="lazy" src="vedtam%20TESTIMONIAL/2.png" /></div>
          <div class="client-cloud-item"><img alt="Client" loading="lazy" src="vedtam%20TESTIMONIAL/3.png" /></div>
          <div class="client-cloud-item"><img alt="Client" loading="lazy" src="vedtam%20TESTIMONIAL/4.png" /></div>
          <div class="client-cloud-item"><img alt="Client" loading="lazy" src="vedtam%20TESTIMONIAL/5.png" /></div>
          <div class="client-cloud-item"><img alt="Client" loading="lazy" src="vedtam%20TESTIMONIAL/6.png" /></div>
          <div class="client-cloud-item"><img alt="Client" loading="lazy" src="vedtam%20TESTIMONIAL/7.png" /></div>
          <div class="client-cloud-item"><img alt="Client" loading="lazy" src="vedtam%20TESTIMONIAL/8.png" /></div>
          <div class="client-cloud-item"><img alt="Client" loading="lazy" src="vedtam%20TESTIMONIAL/9.png" /></div>
          <div class="client-cloud-item"><img alt="Client" loading="lazy" src="vedtam%20TESTIMONIAL/10.png" /></div>
          <div class="client-cloud-item"><img alt="Client" loading="lazy" src="vedtam%20TESTIMONIAL/image.png" /></div>
          <div class="client-cloud-item"><img alt="Client" loading="lazy" src="vedtam%20TESTIMONIAL/nimbuslogo.jpeg" /></div>
          <div class="client-cloud-item"><img alt="Client" loading="lazy" src="vedtam%20TESTIMONIAL/12.png" /></div>
          <div class="client-cloud-item"><img alt="Client" loading="lazy" src="vedtam%20TESTIMONIAL/13.png" /></div>
          <div class="client-cloud-item"><img alt="Client" loading="lazy" src="vedtam%20TESTIMONIAL/14.png" /></div>
          <div class="client-cloud-item"><img alt="Client" loading="lazy" src="vedtam%20TESTIMONIAL/15.png" /></div>
        </div>
      </div>
    </div>
  </section>
"""

# Find Partner Strip
start_idx1 = content.find('<!-- Hero Partners Strip -->')
if start_idx1 == -1:
    print("Could not find Hero Partners Strip")
    sys.exit(1)

# Find the end of Our Clients strip which is right before CERT-In Subscribe Modal
start_idx2 = content.find('<!-- Our Clients Strip -->', start_idx1)
end_idx2 = content.find('</div>\n    </div>\n  </section>\n  <!-- CERT-In Subscribe Modal -->', start_idx2)
if end_idx2 == -1:
    end_idx2 = content.find('<!-- CERT-In Subscribe Modal -->', start_idx2)
    
if end_idx2 == -1:
    print("Could not find end of Our Clients Strip")
    sys.exit(1)

# Delete both strips
block_to_replace = content[start_idx1:end_idx2]
content = content.replace(block_to_replace, tech_partners_html + '\n  </div>\n    </div>\n  </section>\n  ')

# Insert CSS
head_end = content.find('</head>')
if head_end != -1:
    content = content[:head_end] + new_css + content[head_end:]

# Insert Our Clients above FAQ
faq_idx = content.find('<section class="faq-section">')
if faq_idx != -1:
    content = content[:faq_idx] + our_clients_html + "\n  " + content[faq_idx:]
else:
    print("FAQ section not found")

with open(filepath, "w", encoding="utf-8") as f:
    f.write(content)

print("HTML modified successfully.")
