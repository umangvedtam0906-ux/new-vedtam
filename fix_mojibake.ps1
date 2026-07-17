$dirPath = "c:\Users\Manu\Downloads\new-vedtam-main (3)\new-vedtam-main"

$replacements = @{
    "â€”" = "—"
    "â†’" = "→"
    "âœ“" = "✓"
    "â€¢" = "•"
    "Â©" = "©"
    "â ¯" = "❯"
    "â ®" = "❮"
    "â€œ" = "“"
    "â€ " = "”"
    "â€™" = "’"
    "Â " = " "
}

$count = 0

Get-ChildItem -Path $dirPath -Filter "*.html" -Recurse | ForEach-Object {
    $content = Get-Content $_.FullName -Raw -Encoding UTF8
    $original = $content
    
    foreach ($key in $replacements.Keys) {
        $content = $content.Replace($key, $replacements[$key])
    }
    
    if ($content -cne $original) {
        Set-Content -Path $_.FullName -Value $content -Encoding UTF8
        $count++
    }
}

Write-Host "Fixed mojibake in $count HTML files."
