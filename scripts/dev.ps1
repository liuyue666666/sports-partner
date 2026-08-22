# sports-partner 本地开发脚本 (PowerShell)

param(
    [ValidateSet('infra', 'backend', 'admin', 'test', 'all')]
    [string]$Target = 'all'
)

$Root = Split-Path -Parent $MyInvocation.MyCommand.Path
Set-Location $Root

function Start-Infra {
    Write-Host '>> Starting MySQL + Redis (docker compose)...' -ForegroundColor Cyan
    docker compose up -d
}

function Start-Backend {
    Write-Host '>> Starting FastAPI backend on :8000...' -ForegroundColor Cyan
    Set-Location "$Root\backend"
    if (-not (Test-Path '.venv')) { python -m venv .venv }
    .\.venv\Scripts\pip install -r requirements.txt -q
    .\.venv\Scripts\uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
}

function Start-Admin {
    Write-Host '>> Starting Vue admin on :5173...' -ForegroundColor Cyan
    Set-Location "$Root\admin"
    if (-not (Test-Path 'node_modules')) { npm install }
    npm run dev
}

function Run-Tests {
    Write-Host '>> Running backend tests...' -ForegroundColor Cyan
    Set-Location "$Root\backend"
    .\.venv\Scripts\pytest ..\tests\backend -v
}

switch ($Target) {
    'infra'   { Start-Infra }
    'backend' { Start-Backend }
    'admin'   { Start-Admin }
    'test'    { Run-Tests }
    'all'     {
        Start-Infra
        Write-Host ''
        Write-Host 'Infrastructure started. Open two terminals:' -ForegroundColor Yellow
        Write-Host '  1) .\scripts\dev.ps1 -Target backend'
        Write-Host '  2) .\scripts\dev.ps1 -Target admin'
        Write-Host '  Miniapp: open miniapp/ in WeChat DevTools'
    }
}
