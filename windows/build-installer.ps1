$ErrorActionPreference = 'Stop'
$repoRoot = Split-Path -Parent $PSScriptRoot
$nsis = Get-Command makensis.exe -ErrorAction SilentlyContinue
if (-not $nsis) {
    throw 'NSIS (makensis.exe) was not found. Install NSIS and try again.'
}

Push-Location $PSScriptRoot
try {
    & $nsis.Source installer.nsi
} finally {
    Pop-Location
}

Write-Host 'Installer build completed.'
