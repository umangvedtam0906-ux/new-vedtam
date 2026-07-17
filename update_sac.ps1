$file = "C:\Users\Manu\Downloads\new-vedtam-main (7)\new-vedtam\solutions-and-consulting.html"
$content = Get-Content $file -Raw

$cssToInject = @"
  <style id="premium-cards-css">
    /* Premium Glassmorphism & Neon Cards */
    .premium-feature-card {
      position: relative;
      display: flex;
      flex-direction: column;
      text-decoration: none;
      padding: 2.5rem 2rem;
      background: rgba(12, 21, 36, 0.4) !important;
      backdrop-filter: blur(16px);
      -webkit-backdrop-filter: blur(16px);
      border: 1px solid rgba(8, 68, 129, 0.4) !important;
      border-radius: 24px !important;
      transition: transform 0.4s cubic-bezier(0.175, 0.885, 0.32, 1.275), box-shadow 0.4s ease, border-color 0.4s ease !important;
      overflow: hidden;
      z-index: 1;
    }

    .premium-feature-card::before {
      content: '';
      position: absolute;
      top: -50%;
      left: -50%;
      width: 200%;
      height: 200%;
      background: conic-gradient(transparent, rgba(0, 195, 255, 0.4), transparent 30%);
      animation: sweepBorder 4s linear infinite;
      opacity: 0;
      transition: opacity 0.4s ease;
      z-index: -2;
    }

    .premium-feature-card::after {
      content: '';
      position: absolute;
      inset: 1px;
      background: rgba(12, 21, 36, 0.95);
      border-radius: 23px;
      z-index: -1;
    }

    .premium-feature-card:hover::before {
      opacity: 1;
    }

    .premium-feature-card:hover {
      transform: translateY(-8px) scale(1.02);
      box-shadow: 0 20px 40px rgba(0, 163, 217, 0.15), 0 0 20px rgba(0, 195, 255, 0.1) inset !important;
      border-color: rgba(0, 195, 255, 0.5) !important;
    }

    @keyframes sweepBorder {
      0% { transform: rotate(0deg); }
      100% { transform: rotate(360deg); }
    }

    .card-image-banner {
      width: calc(100% + 4rem);
      margin: -2.5rem -2rem 1.5rem -2rem;
      height: 180px;
      object-fit: cover;
      border-bottom: 1px solid rgba(8, 68, 129, 0.4);
      transition: transform 0.5s cubic-bezier(0.175, 0.885, 0.32, 1.275), filter 0.5s ease;
      filter: brightness(0.85);
      border-radius: 24px 24px 0 0;
    }
    
    .premium-feature-card:hover .card-image-banner {
      transform: scale(1.05);
      filter: brightness(1.1) contrast(1.1);
    }

    .premium-feature-card h3 {
      color: #fff !important;
      margin-bottom: 0.8rem !important;
      font-size: 1.3rem !important;
      font-weight: 700;
      letter-spacing: 0.5px;
      transition: color 0.3s ease;
      position: relative;
      z-index: 2;
    }

    .premium-feature-card:hover h3 {
      color: #00c3ff !important;
    }

    .premium-feature-card p {
      color: #94a3b8 !important;
      font-size: 0.95rem !important;
      line-height: 1.6 !important;
      margin: 0 !important;
      transition: color 0.3s ease;
      position: relative;
      z-index: 2;
    }
    
    .premium-feature-card:hover p {
      color: #e2e8f0 !important;
    }
  </style>
"@

if ($content -notmatch 'id="premium-cards-css"') {
    $content = $content -replace '</head>', "$cssToInject`n</head>"
}

$replacements = @{
    "solutions/cybersecurity-services.html" = "cybersecurity_banner.png"
    "solutions/network-security-solutions.html" = "network_security_banner.png"
    "solutions/devops-solutions.html" = "devops_banner.png"
    "solutions/ot-security-services.html" = "ot_security_banner.png"
    "solutions/cloud-services.html" = "cloud_services_banner.png"
    "solutions/it-managed-services.html" = "it_managed_banner.png"
    "solutions/software-services.html" = "software_banner.png"
    
    "consulting/dpdp-act-consulting-services.html" = "dpdp_act_banner.png"
    "consulting/virtual-ciso-services.html" = "vciso_banner.png"
    "consulting/iso-consulting-services.html" = "iso_banner.png"
    "consulting/qms-consulting-services.html" = "qms_banner.png"
    "consulting/hipaa-consulting-services.html" = "hipaa_banner.png"
    "consulting/soc2-consulting-services.html" = "soc2_banner.png"
    "consulting/pci-dss-consulting-services.html" = "pci_banner.png"
    "consulting/gdpr-consulting-services.html" = "gdpr_banner.png"
    "consulting/network-security-consulting-services.html" = "netsec_consult_banner.png"
    "consulting/network-security-audit-services.html" = "netsec_audit_banner.png"
}

foreach ($key in $replacements.Keys) {
    $imgFile = $replacements[$key]
    $escapedKey = [regex]::Escape($key)
    $pattern = '(?s)(<a href="' + $escapedKey + '"[^>]*>)\s*<div class=[''"]premium-icon-wrapper[''"]>.*?</div>'
    $imgTag = '<img src="images/solutions/' + $imgFile + '" class="card-image-banner" alt="Service Banner">'
    $content = [regex]::Replace($content, $pattern, "`$1`n                $imgTag")
}

Set-Content -Path $file -Value $content -Encoding UTF8
Write-Output "Updated solutions-and-consulting.html successfully"
