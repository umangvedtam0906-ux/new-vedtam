$files = Get-ChildItem -Path "c:\Users\Manu\Desktop\vedtam website" -Filter "*.html"

foreach ($file in $files) {
    if ($file.Name -eq "network-security-consulting-services.html") {
        continue
    }
    
    $content = [IO.File]::ReadAllText($file.FullName)
    
    if ($content -notmatch "network-security-consulting-services\.html") {
        # Desktop & Mobile Nav
        $content = $content -replace '(?m)^(\s*)(<a href="network-security-audit-services\.html"(?: class="active")?>Network Security Audit</a>)', '$1<a href="network-security-consulting-services.html">Network Security Consulting</a>`r`n$1$2'
        
        # Footer
        $content = $content -replace '(?m)^(\s*)(<li><a href="network-security-audit-services\.html"(?: class="active")?>Network Security Audit</a></li>)', '$1<li><a href="network-security-consulting-services.html">Network Security Consulting</a></li>`r`n$1$2'
        
        $utf8NoBom = New-Object System.Text.UTF8Encoding $false
        [IO.File]::WriteAllText($file.FullName, $content, $utf8NoBom)
        Write-Host "Updated $($file.Name)"
    }
}
