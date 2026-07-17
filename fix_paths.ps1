$htmlFiles = @(
    "C:\Users\Manu\Downloads\new-vedtam-main (7)\new-vedtam\solutions.html",
    "C:\Users\Manu\Downloads\new-vedtam-main (7)\new-vedtam\consulting.html",
    "C:\Users\Manu\Downloads\new-vedtam-main (7)\new-vedtam\solutions-and-consulting.html"
)

$pattern = 'src="file:///C:/Users/Manu/.gemini/antigravity-ide/brain/[a-zA-Z0-9\-]+/([a-zA-Z0-9_]+)_\d{13}\.png"'

foreach ($file in $htmlFiles) {
    if (Test-Path $file) {
        $content = Get-Content $file -Raw
        $newContent = [regex]::Replace($content, $pattern, {
            param($match)
            $cleanName = $match.Groups[1].Value
            return 'src="images/solutions/' + $cleanName + '.png"'
        })
        Set-Content -Path $file -Value $newContent -Encoding UTF8
        Write-Output "Updated $file"
    }
}
