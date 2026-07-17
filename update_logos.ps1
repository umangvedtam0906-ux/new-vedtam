$dirPath = "c:\Users\Manu\Downloads\new-vedtam-main (3)\new-vedtam-main"

$pattern = '(?si)(<a[^>]*class="[^"]*nav-logo[^"]*"[^>]*>)\s*<img[^>]*class="logo-en"[^>]*src="([^"]*?)website-logo/VEDTAM%20TECH%20SOLUTIONS%20en\.png"[^>]*>\s*<img[^>]*class="logo-hi"[^>]*src="([^"]*?)website-logo/VEDTAM%20TECH%20SOLUTIONS%20hn\.png"[^>]*>\s*</a>'

$count = 0

Get-ChildItem -Path $dirPath -Filter "*.html" -Recurse | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    
    if ($content -match $pattern) {
        $newContent = [regex]::Replace($content, $pattern, {
            param($m)
            $a_tag = $m.Groups[1].Value
            $prefix = $m.Groups[2].Value
            
            return @"
$a_tag
        <img alt="Vedtam Tech Solutions logo" decoding="async"
          src="${prefix}website-logo/VEDTAM%20TECH%20SOLUTIONS%20en.png" 
          data-logo-switcher 
          data-logos="${prefix}website-logo/VEDTAM%20TECH%20SOLUTIONS%20en.png, ${prefix}website-logo/VEDTAM%20TECH%20SOLUTIONS%20hn.png" />
      </a>
"@
        })
        Set-Content -Path $_.FullName -Value $newContent -Encoding UTF8
        $count++
    }
}

Write-Host "Replaced old logo tags in $count files."
