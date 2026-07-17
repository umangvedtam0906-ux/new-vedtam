$files = Get-ChildItem -Path "c:\Users\Manu\Downloads\new-vedtam\new-vedtam" -Filter *.html -Recurse
foreach ($file in $files) {
    # Try reading as UTF-8
    $content = Get-Content -Path $file.FullName -Raw -Encoding UTF8
    $modified = $false

    # Location
    if ($content -match '<span[^>]*class="fc-icon"[^>]*>.*?</span>(?=\s*Location:)') {
        $content = $content -replace '<span[^>]*class="fc-icon"[^>]*>.*?</span>(?=\s*Location:)', '<i class="fas fa-map-marker-alt fc-icon"></i>'
        $modified = $true
    }
    
    # Email
    if ($content -match '<span[^>]*class="fc-icon"[^>]*>.*?</span>(?=\s*Email:)') {
        $content = $content -replace '<span[^>]*class="fc-icon"[^>]*>.*?</span>(?=\s*Email:)', '<i class="fas fa-envelope fc-icon"></i>'
        $modified = $true
    }

    # Phone
    if ($content -match '<span[^>]*class="fc-icon"[^>]*>.*?</span>(?=\s*Phone:)') {
        $content = $content -replace '<span[^>]*class="fc-icon"[^>]*>.*?</span>(?=\s*Phone:)', '<i class="fas fa-phone fc-icon"></i>'
        $modified = $true
    }

    # Add FontAwesome if missing
    if ($content -notmatch 'font-awesome' -and $content -notmatch 'all\.min\.css') {
        if ($content -match '</head>') {
            $content = $content -replace '</head>', "  <link rel=`"stylesheet`" href=`"https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css`" />`n</head>"
            $modified = $true
        }
    }

    if ($modified) {
        Set-Content -Path $file.FullName -Value $content -Encoding UTF8
    }
}
