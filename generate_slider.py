slides_data = [
    {'title': 'Cybersecurity Services', 'url': 'solutions/cybersecurity-services.html', 'icon': 'fas fa-shield-alt', 'grad': 1, 'label': 'Security Solutions', 'h1_1': 'Next-Gen', 'h1_2': 'Cybersecurity', 'desc': 'Protect your digital assets with AI-driven threat detection and response.'},
    {'title': 'Network Security Solutions', 'url': 'solutions/network-security-solutions.html', 'icon': 'fas fa-server', 'grad': 2, 'label': 'Security Solutions', 'h1_1': 'Enterprise', 'h1_2': 'Network Security', 'desc': 'Robust firewalls and intrusion prevention for your entire infrastructure.'},
    {'title': 'DevOps Solutions', 'url': 'solutions/devops-solutions.html', 'icon': 'fas fa-laptop-code', 'grad': 3, 'label': 'Infrastructure', 'h1_1': 'Agile', 'h1_2': 'DevOps Solutions', 'desc': 'Streamline your deployment pipelines with CI/CD automation.'},
    {'title': 'OT Security Services', 'url': 'solutions/ot-security-services.html', 'icon': 'fas fa-industry', 'grad': 1, 'label': 'Industrial Security', 'h1_1': 'Industrial', 'h1_2': 'OT Security', 'desc': 'Protect critical infrastructure and industrial control systems from cyber threats.'},
    {'title': 'Cloud Services', 'url': 'solutions/cloud-services.html', 'icon': 'fas fa-cloud', 'grad': 2, 'label': 'Cloud', 'h1_1': 'Scalable', 'h1_2': 'Cloud Services', 'desc': 'Design and deploy high-performance environments on AWS, Azure, and Google Cloud.'},
    {'title': 'IT Managed Services', 'url': 'solutions/it-managed-services.html', 'icon': 'fas fa-network-wired', 'grad': 3, 'label': 'Managed Services', 'h1_1': '24/7', 'h1_2': 'IT Management', 'desc': 'Optimize operations with round-the-clock infrastructure support.'},
    {'title': 'Software Solutions', 'url': 'solutions/software-services.html', 'icon': 'fas fa-code', 'grad': 1, 'label': 'Innovation', 'h1_1': 'Custom', 'h1_2': 'Software Solutions', 'desc': 'Application development powered by next-generation AI integrations.'},
    {'title': 'DPDP Act Compliance', 'url': 'consulting/dpdp-act-consulting-services.html', 'icon': 'fas fa-file-contract', 'grad': 2, 'label': 'Data Privacy', 'h1_1': 'India', 'h1_2': 'DPDP Act Ready', 'desc': 'Ensure your organization meets the latest Digital Personal Data Protection mandates.'},
    {'title': 'Virtual CISO Services', 'url': 'consulting/virtual-ciso-services.html', 'icon': 'fas fa-user-shield', 'grad': 3, 'label': 'Strategic Advisory', 'h1_1': 'Expert', 'h1_2': 'Virtual CISO', 'desc': 'Align your technology and security strategy with business goals.'},
    {'title': 'ISO Consultancy', 'url': 'consulting/iso-consulting-services.html', 'icon': 'fas fa-certificate', 'grad': 1, 'label': 'Certifications', 'h1_1': 'Global', 'h1_2': 'ISO Standards', 'desc': 'Achieve ISO 27001, 9001 and other key standards with our proven roadmap.'},
    {'title': 'QMS Consulting', 'url': 'consulting/qms-consulting-services.html', 'icon': 'fas fa-tasks', 'grad': 2, 'label': 'Quality', 'h1_1': 'Robust', 'h1_2': 'QMS Consulting', 'desc': 'Establish Quality Management Systems that drive continuous improvement.'},
    {'title': 'HIPAA Compliance', 'url': 'consulting/hipaa-consulting-services.html', 'icon': 'fas fa-notes-medical', 'grad': 3, 'label': 'Healthcare Privacy', 'h1_1': 'Full', 'h1_2': 'HIPAA Compliance', 'desc': 'Secure patient data and ensure healthcare regulatory compliance effortlessly.'},
    {'title': 'SOC 2 Consulting', 'url': 'consulting/soc2-consulting-services.html', 'icon': 'fas fa-lock', 'grad': 1, 'label': 'Certifications', 'h1_1': 'Trust via', 'h1_2': 'SOC 2 Consulting', 'desc': 'Build trust with clients by demonstrating robust security and availability controls.'},
    {'title': 'PCI DSS Compliance', 'url': 'consulting/pci-dss-consulting-services.html', 'icon': 'fas fa-credit-card', 'grad': 2, 'label': 'Payment Security', 'h1_1': 'Secure', 'h1_2': 'PCI DSS Compliance', 'desc': 'Protect cardholder data and achieve seamless payment security certification.'},
    {'title': 'GDPR Consulting', 'url': 'consulting/gdpr-consulting-services.html', 'icon': 'fas fa-globe-europe', 'grad': 3, 'label': 'Data Privacy', 'h1_1': 'European', 'h1_2': 'GDPR Consulting', 'desc': 'Navigate the complexities of the General Data Protection Regulation.'},
    {'title': 'Network Security Consulting', 'url': 'consulting/network-security-consulting-services.html', 'icon': 'fas fa-project-diagram', 'grad': 1, 'label': 'Strategic Advisory', 'h1_1': 'Proactive', 'h1_2': 'Network Consulting', 'desc': 'Expert guidance to architect and fortify your enterprise networks.'},
    {'title': 'Network Security Audit', 'url': 'consulting/network-security-audit-services.html', 'icon': 'fas fa-search', 'grad': 2, 'label': 'Assessment', 'h1_1': 'Rigorous', 'h1_2': 'Security Audits', 'desc': 'Comprehensive VAPT and risk assessments to uncover hidden vulnerabilities.'}
]

html = '      <div class="phs-slides" id="phsSlides">\n'

for i, slide in enumerate(slides_data):
    active_class = ' active' if i == 0 else ''
    next1 = slides_data[(i + 1) % len(slides_data)]
    next2 = slides_data[(i + 2) % len(slides_data)]
    
    html += f'''        <!-- Slide {i+1}: {slide['title']} -->
        <div class="phs-slide{active_class}">
          <div class="phs-content">
            <div class="phs-label">{slide['label']}</div>
            <h1 class="phs-title">{slide['h1_1']} <br><span>{slide['h1_2']}</span></h1>
            <p class="phs-desc">{slide['desc']}</p>
            <div class="phs-actions">
              <a href="{slide['url']}" class="phs-btn phs-btn-primary">Learn More</a>
            </div>
          </div>
          <div class="phs-visuals">
            <a href="{slide['url']}" class="phs-card main" style="text-decoration:none">
              <div class="phs-card-icon grad-{slide['grad']}"><i class="{slide['icon']}"></i></div>
              <h3 class="phs-card-title">{slide['title']}</h3>
              <p class="phs-card-text">{slide['desc']}</p>
            </a>
            <div class="phs-card secondary">
              <div class="phs-card-icon grad-{next1['grad']}"><i class="{next1['icon']}"></i></div>
              <h3 class="phs-card-title">{next1['title']}</h3>
            </div>
            <div class="phs-card tertiary">
              <div class="phs-card-icon grad-{next2['grad']}"><i class="{next2['icon']}"></i></div>
              <h3 class="phs-card-title">{next2['title']}</h3>
            </div>
          </div>
        </div>
'''

html += '      </div>\n      \n      <div class="phs-nav">\n        <div class="phs-arrows">\n          <div class="phs-arrow" id="phsPrev"><i class="fas fa-chevron-left"></i></div>\n          <div class="phs-arrow" id="phsNext"><i class="fas fa-chevron-right"></i></div>\n        </div>\n        <div class="phs-dots" id="phsDots">\n'
for i in range(len(slides_data)):
    active = ' active' if i == 0 else ''
    html += f'          <div class="phs-dot{active}" data-index="{i}"></div>\n'

html += '        </div>\n      </div>'

with open('new_slider.html', 'w', encoding='utf-8') as f:
    f.write(html)
