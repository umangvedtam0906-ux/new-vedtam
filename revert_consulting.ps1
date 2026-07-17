$htmlFiles = @(
    "C:\Users\Manu\Downloads\new-vedtam-main (7)\new-vedtam\consulting.html",
    "C:\Users\Manu\Downloads\new-vedtam-main (7)\new-vedtam\solutions-and-consulting.html"
)

$svgDoc = '<div class="premium-icon-wrapper"><svg fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z" /></svg></div>'
$svgBolt = '<div class="premium-icon-wrapper"><svg fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M13 10V3L4 14h7v7l9-11h-7z" /></svg></div>'
$svgSearch = '<div class="premium-icon-wrapper"><svg fill="none" stroke="currentColor" viewBox="0 0 24 24" stroke-width="1.5"><path stroke-linecap="round" stroke-linejoin="round" d="M21 21l-5.197-5.197m0 0A7.5 7.5 0 105.196 5.196a7.5 7.5 0 0010.607 10.607z" /></svg></div>'

$replacements = @{
    '<img src="https://images.unsplash.com/photo-1589829085413-56de8ae18c73\?w=800&q=80" class="card-image-banner" alt="[^"]*">' = $svgDoc
    '<img src="https://images.unsplash.com/photo-1573164713988-8665fc963095\?w=800&q=80" class="card-image-banner" alt="[^"]*">' = $svgDoc
    '<img src="https://images.unsplash.com/photo-1450101499163-c8848c66ca85\?w=800&q=80" class="card-image-banner" alt="[^"]*">' = $svgDoc
    '<img src="https://images.unsplash.com/photo-1512758117926-0b1981a4d9aa\?w=800&q=80" class="card-image-banner" alt="[^"]*">' = $svgDoc
    '<img src="https://images.unsplash.com/photo-1576091160399-112ba8d25d1d\?w=800&q=80" class="card-image-banner" alt="[^"]*">' = $svgDoc
    '<img src="https://images.unsplash.com/photo-1563986768494-4dee2763ff0f\?w=800&q=80" class="card-image-banner" alt="[^"]*">' = $svgDoc
    '<img src="https://images.unsplash.com/photo-1563013544-824ae1b704d3\?w=800&q=80" class="card-image-banner" alt="[^"]*">' = $svgDoc
    '<img src="https://images.unsplash.com/photo-1507925922888-eb81b01da42e\?w=800&q=80" class="card-image-banner" alt="[^"]*">' = $svgDoc
    '<img src="https://images.unsplash.com/photo-1544197150-b99a580bb7a8\?w=800&q=80" class="card-image-banner" alt="[^"]*">' = $svgBolt
    '<img src="https://images.unsplash.com/photo-1554224155-6726b3ff858f\?w=800&q=80" class="card-image-banner" alt="[^"]*">' = $svgSearch
}

foreach ($file in $htmlFiles) {
    if (Test-Path $file) {
        $content = Get-Content $file -Raw
        foreach ($pattern in $replacements.Keys) {
            $val = $replacements[$pattern]
            $content = $content -replace $pattern, $val
        }
        Set-Content -Path $file -Value $content -Encoding UTF8
        Write-Output "Reverted consulting images to SVGs in $file"
    }
}
