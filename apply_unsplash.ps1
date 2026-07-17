$htmlFiles = @(
    "C:\Users\Manu\Downloads\new-vedtam-main (7)\new-vedtam\solutions.html",
    "C:\Users\Manu\Downloads\new-vedtam-main (7)\new-vedtam\consulting.html",
    "C:\Users\Manu\Downloads\new-vedtam-main (7)\new-vedtam\solutions-and-consulting.html"
)

$replacements = @{
    "images/solutions/cybersecurity_banner.png" = "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=800&q=80"
    "images/solutions/network_security_banner.png" = "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=800&q=80"
    "images/solutions/devops_banner.png" = "https://images.unsplash.com/photo-1618401471353-b98afee0b2eb?w=800&q=80"
    "images/solutions/ot_security_banner.png" = "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=800&q=80"
    "images/solutions/cloud_services_banner.png" = "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=800&q=80"
    "images/solutions/it_managed_banner.png" = "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=800&q=80"
    "images/solutions/software_banner.png" = "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&q=80"
    
    "images/solutions/dpdp_act_banner.png" = "https://images.unsplash.com/photo-1589829085413-56de8ae18c73?w=800&q=80"
    "images/solutions/vciso_banner.png" = "https://images.unsplash.com/photo-1573164713988-8665fc963095?w=800&q=80"
    "images/solutions/iso_banner.png" = "https://images.unsplash.com/photo-1450101499163-c8848c66ca85?w=800&q=80"
    "images/solutions/qms_banner.png" = "https://images.unsplash.com/photo-1512758117926-0b1981a4d9aa?w=800&q=80"
    "images/solutions/hipaa_banner.png" = "https://images.unsplash.com/photo-1576091160399-112ba8d25d1d?w=800&q=80"
    "images/solutions/soc2_banner.png" = "https://images.unsplash.com/photo-1563986768494-4dee2763ff0f?w=800&q=80"
    "images/solutions/pci_banner.png" = "https://images.unsplash.com/photo-1563013544-824ae1b704d3?w=800&q=80"
    "images/solutions/gdpr_banner.png" = "https://images.unsplash.com/photo-1507925922888-eb81b01da42e?w=800&q=80"
    "images/solutions/netsec_consult_banner.png" = "https://images.unsplash.com/photo-1544197150-b99a580bb7a8?w=800&q=80"
    "images/solutions/netsec_audit_banner.png" = "https://images.unsplash.com/photo-1554224155-6726b3ff858f?w=800&q=80"
}

foreach ($file in $htmlFiles) {
    if (Test-Path $file) {
        $content = Get-Content $file -Raw
        foreach ($key in $replacements.Keys) {
            $val = $replacements[$key]
            $content = $content -replace [regex]::Escape($key), $val
        }
        Set-Content -Path $file -Value $content -Encoding UTF8
        Write-Output "Updated $file"
    }
}
