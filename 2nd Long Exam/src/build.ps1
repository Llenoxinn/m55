# Builds every reviewer in src/ and copies the PDFs next to "Lecture Notes 01.pdf".
#
# Requirements: a TeX distribution with latexmk (MiKTeX or TeX Live) on PATH.
# Usage (from anywhere):   powershell -ExecutionPolicy Bypass -File ".\src\build.ps1"
# Optional:                 -Only lecture-notes-02     (build a single document)
#                           -Figures                   (regenerate matplotlib figures first)
param(
    [string]$Only = "",
    [switch]$Figures
)

$ErrorActionPreference = "Stop"
$src  = $PSScriptRoot
$dest = Split-Path $src -Parent

# folder name -> output PDF name
$docs = [ordered]@{
    "lecture-notes-02" = "Lecture Notes 02.pdf"
    "lecture-notes-03" = "Lecture Notes 03.pdf"
    "mock-exams"       = "Mock Exams.pdf"
}

foreach ($name in $docs.Keys) {
    if ($Only -and $Only -ne $name) { continue }
    $dir = Join-Path $src $name
    if (-not (Test-Path (Join-Path $dir "$name.tex"))) { continue }

    if ($Figures -and (Test-Path (Join-Path $dir "figures\make_figures.py"))) {
        Write-Host "==> figures for $name"
        python (Join-Path $dir "figures\make_figures.py")
        if ($LASTEXITCODE -ne 0) { throw "figure generation failed for $name" }
    }

    Write-Host "==> compiling $name"
    Push-Location $dir
    try {
        latexmk -pdf -interaction=nonstopmode -halt-on-error -outdir=build "$name.tex"
        if ($LASTEXITCODE -ne 0) { throw "latexmk failed for $name (see $dir\build\$name.log)" }
    } finally {
        Pop-Location
    }
    Copy-Item (Join-Path $dir "build\$name.pdf") (Join-Path $dest $docs[$name]) -Force
    Write-Host "    -> $($docs[$name])"
}
