param(
    [switch]$SkipInstall
)

$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot

if (-not $SkipInstall) {
    Push-Location $Root
    if (-not (Test-Path ".venv")) {
        python -m venv .venv
    }
    .\.venv\Scripts\python.exe -m pip install -r backend\requirements-dev.txt
    Pop-Location

    Push-Location "$Root\frontend"
    npm install
    Pop-Location
}

Write-Host "Start backend:" -ForegroundColor Cyan
Write-Host "  .\.venv\Scripts\Activate.ps1; cd backend; python manage.py runserver 8000"
Write-Host "Start frontend:" -ForegroundColor Cyan
Write-Host "  cd frontend; npm run dev"
