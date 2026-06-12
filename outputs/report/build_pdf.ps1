# Build research_report_v2.pdf from the markdown via pandoc + xelatex.
#
# Sections in the source are manually numbered ("## 1. Introduction"), so we do
# NOT pass --number-sections. The in-body H1 + author block (everything above the
# first horizontal rule) is stripped into a temp file so it isn't duplicated under
# the metadata title block; the canonical research_report_v2.md is left untouched.
#
# Usage:  powershell -File outputs/report/build_pdf.ps1
$ErrorActionPreference = "Stop"
$here = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $here

$pandoc = Join-Path $env:LOCALAPPDATA "Pandoc\pandoc.exe"
if (-not (Test-Path $pandoc)) {
    $cmd = Get-Command pandoc -ErrorAction SilentlyContinue
    if ($cmd) { $pandoc = $cmd.Source } else { throw "pandoc not found" }
}

$src = "research_report_v2.md"
$out = "research_report_v2.pdf"

# Strip everything up to and including the first '---' rule (title/author block).
# Read as UTF-8 explicitly: the default Get-Content codepage is the system ANSI
# (CP932 here), which mangles em-dashes, middots, Greek, and math symbols.
$lines = Get-Content $src -Encoding UTF8
$hrIdx = (0..($lines.Count - 1) | Where-Object { $lines[$_] -match '^---\s*$' } | Select-Object -First 1)
$body  = ($lines[($hrIdx + 1)..($lines.Count - 1)]) -join "`n"
$tmpMd = Join-Path $env:TEMP ("report_body_" + [System.Guid]::NewGuid().ToString("N") + ".md")
Set-Content -Path $tmpMd -Value $body -Encoding utf8

try {
    & $pandoc $tmpMd `
        --from=markdown+autolink_bare_uris `
        --metadata-file metadata.yaml `
        --include-in-header header.tex `
        --resource-path "$here" `
        --pdf-engine=xelatex `
        --toc --toc-depth=2 `
        -o $out
    Write-Output "wrote $out"
}
finally {
    Remove-Item $tmpMd -ErrorAction SilentlyContinue
}
