$ErrorActionPreference = "Stop"
$Root = Split-Path -Parent $PSScriptRoot
Push-Location "$Root\backend"
$env:DJANGO_SETTINGS_MODULE = "nawacorpus.test_settings"
..\.venv\Scripts\python.exe manage.py test corpus.tests
Pop-Location
