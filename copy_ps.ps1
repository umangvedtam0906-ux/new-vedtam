$src = "C:\Users\Manu\.gemini\antigravity-ide\brain\229faa3e-a6cd-4d34-b755-fcb62ce17388"
$dest = "C:\Users\Manu\Downloads\new-vedtam-main (7)\new-vedtam\images\solutions"

if (-Not (Test-Path $dest)) {
    New-Item -ItemType Directory -Force -Path $dest
}

Get-ChildItem -Path $src -Filter "*_banner_*.png" | ForEach-Object {
    $newName = $_.Name -replace '_1\d{12}\.png', '.png'
    $destPath = Join-Path $dest $newName
    Copy-Item -Path $_.FullName -Destination $destPath -Force
    Write-Output "Copied $_.Name to $destPath"
}
