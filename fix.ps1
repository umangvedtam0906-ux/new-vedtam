$files = Get-ChildItem -Path . -Filter *.html -Recurse

$locPattern = '<span\s+class="fc-icon">✓</span>'
$locReplace = '<i class="fas fa-map-marker-alt fc-icon"></i>'

$emailPattern = '<span\s+class="fc-icon">âœ‰</span>'
$emailReplace = '<i class="fas fa-envelope fc-icon"></i>'

$phonePattern = '<span\s+class="fc-icon">â˜Ž</span>'
$phoneReplace = '<i class="fas fa-phone fc-icon"></i>'

$faLink = '  <link rel="stylesheet" href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.15.4/css/all.min.css" />'

foreach ($file in $files) {
    # Read as UTF-8
    $content = Get-Content -Path $file.FullName -Raw -Encoding UTF8

    $modified = $false

    if ($content -notmatch "font-awesome" -and $content -notmatch "all\.min\.css") {
        if ($content -match "</head>") {
            $content = $content -replace "</head>", "$faLink`n</head>"
            $modified = $true
        }
    }

    if ($content -match $locPattern) {
        $content = $content -replace $locPattern, $locReplace
        $modified = $true
    }
    if ($content -match $emailPattern) {
        $content = $content -replace $emailPattern, $emailReplace
        $modified = $true
    }
    if ($content -match $phonePattern) {
        $content = $content -replace $phonePattern, $phoneReplace
        $modified = $true
    }

    if ($modified) {
        [IO.File]::WriteAllText($file.FullName, $content, [System.Text.Encoding]::UTF8)
        Write-Host "Fixed: $($file.FullName)"
    }
}
