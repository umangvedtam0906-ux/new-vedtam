$htmlFiles = @(
    "C:\Users\Manu\Downloads\new-vedtam-main (7)\new-vedtam\solutions.html",
    "C:\Users\Manu\Downloads\new-vedtam-main (7)\new-vedtam\consulting.html",
    "C:\Users\Manu\Downloads\new-vedtam-main (7)\new-vedtam\solutions-and-consulting.html"
)

# For Solutions, map to the images we found in services_images/
$replacements = @{
    "https://images.unsplash.com/photo-1550751827-4bd374c3f58b?w=800&q=80" = "services_images/service_cyber_security_1774586735180.png"
    "https://images.unsplash.com/photo-1558494949-ef010cbdcc31?w=800&q=80" = "services_images/service_network_security_1774586750963.png"
    "https://images.unsplash.com/photo-1618401471353-b98afee0b2eb?w=800&q=80" = "services_images/service_devops_1774586766465.png"
    "https://images.unsplash.com/photo-1581091226825-a6a2a5aee158?w=800&q=80" = "services_images/service_ot_security_1774586821288.png"
    "https://images.unsplash.com/photo-1451187580459-43490279c0fa?w=800&q=80" = "services_images/service_cloud_1774586800180.png"
    "https://images.unsplash.com/photo-1504384308090-c894fdcc538d?w=800&q=80" = "services_images/service_it_managed_1774586782051.png"
    "https://images.unsplash.com/photo-1555066931-4365d14bab8c?w=800&q=80" = "services_images/software_solutions_hero.png"
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
