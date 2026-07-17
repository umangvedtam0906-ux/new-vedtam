$dirPath = "c:\Users\Manu\Downloads\new-vedtam-main (3)\new-vedtam-main"

$styleBlock = @"
  <style id="mega-menu-desktop-zoom-fix">
    /* Mega Menu Zoom Overflow Fix for all screen sizes */
    .mega-menu {
      max-height: calc(100vh - 80px) !important;
      overflow-y: auto !important;
    }
    .mega-menu::-webkit-scrollbar {
      width: 6px;
    }
    .mega-menu::-webkit-scrollbar-thumb {
      background-color: rgba(6, 182, 212, 0.5);
      border-radius: 10px;
    }
  </style>
</head>
"@

$count = 0

Get-ChildItem -Path $dirPath -Filter "*.html" -Recurse | ForEach-Object {
    $content = Get-Content $_.FullName -Raw
    
    # Check if we already applied the fix
    if ($content -notmatch "mega-menu-desktop-zoom-fix") {
        # case-insensitive replace of </head>
        $newContent = $content -ireplace "</head>", $styleBlock
        Set-Content -Path $_.FullName -Value $newContent -Encoding UTF8
        $count++
    }
}

Write-Host "Applied zoom fix to $count HTML files."
