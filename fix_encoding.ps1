$dirPath = "c:\Users\Manu\Downloads\new-vedtam-main (3)\new-vedtam-main"

$correctChars = @(
    [char]0x2014, # em dash
    [char]0x2192, # right arrow
    [char]0x2713, # check
    [char]0x2022, # bullet
    [char]0x00A9, # copyright
    [char]0x276F, # next
    [char]0x276E, # prev
    [char]0x201C, # lquote
    [char]0x201D, # rquote
    [char]0x2019, # squote
    [char]0x00A0  # nbsp
)

$utf8 = [System.Text.Encoding]::UTF8
$win1252 = [System.Text.Encoding]::GetEncoding(1252)

$replacements = [ordered]@{}

foreach ($char in $correctChars) {
    $bytes = $utf8.GetBytes($char)
    $mojibake = $win1252.GetString($bytes)
    
    if ($mojibake -ne $char) {
        $replacements[$mojibake] = $char
    }
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
