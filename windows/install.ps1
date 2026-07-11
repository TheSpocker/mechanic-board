param(
    [string]$InstallDir = "$env:LOCALAPPDATA\MechanicBoard"
)

$ErrorActionPreference = 'Stop'

$repoRoot = Split-Path -Parent $PSScriptRoot
$sourceApp = Join-Path $repoRoot 'app'

if (-not (Test-Path $sourceApp)) {
    throw "Source app folder not found: $sourceApp"
}

New-Item -ItemType Directory -Force -Path $InstallDir | Out-Null
Copy-Item -Path (Join-Path $repoRoot '*') -Destination $InstallDir -Recurse -Force

$python = Get-Command python -ErrorAction SilentlyContinue
if (-not $python) {
    throw 'Python was not found on PATH. Please install Python 3.12+ and try again.'
}

$venvPath = Join-Path $InstallDir 'venv'
& $python.Source -m venv $venvPath
$venvPython = Join-Path $venvPath 'Scripts\python.exe'

& $venvPython -m pip install --upgrade pip
& $venvPython -m pip install -r (Join-Path $InstallDir 'app\requirements.txt')

$batPath = Join-Path $InstallDir 'start-mechanic-board.bat'
@"
@echo off
setlocal
cd /d "$InstallDir\app"
set DB_ENGINE=sqlite3
"$venvPython" manage.py migrate --noinput
start "Mechanic Board" /b "$venvPython" manage.py runserver 0.0.0.0:8000
"@ | Set-Content -Path $batPath -Encoding ascii

Write-Host "Installation complete."
Write-Host "Run: $batPath"
