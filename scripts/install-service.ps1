# install-service.ps1 -- registers the API as a Windows service via NSSM (re-runnable: updates in place).
# Elevated Windows PowerShell 5.1:  powershell.exe -ExecutionPolicy Bypass -File .\scripts\install-service.ps1
param(
  [string]$Nssm = 'C:\nssm\nssm-2.24\win64\nssm.exe',
  [string]$ServiceName = 'ezlcal'
)
$ErrorActionPreference = 'Stop'
$root    = Split-Path -Parent $PSScriptRoot
$backend = Join-Path $root 'backend'
$venvPy  = Join-Path $backend '.venv\Scripts\python.exe'
$logs    = Join-Path $root 'logs'
if (-not (Test-Path $Nssm))   { throw "nssm.exe not found at $Nssm. Pass -Nssm with its path." }
if (-not (Test-Path $venvPy)) { throw 'Python venv missing. Run scripts\deploy.ps1 first.' }
$port = ((Get-Content (Join-Path $backend '.env') | Where-Object { $_ -match '^PORT=' }) -replace '^PORT=', '').Trim()

$inUse = netstat -an | Select-String "127.0.0.1:$port\s+.*LISTENING"
$existing = Get-Service -Name $ServiceName -ErrorAction SilentlyContinue
if ($inUse -and -not $existing) { throw "Port $port is already in use by something else. Pick another PORT in backend\.env and re-run deploy.ps1." }
if (-not (Test-Path $logs)) { New-Item -ItemType Directory $logs | Out-Null }

function N { & $Nssm @args | Out-Null; if ($LASTEXITCODE -ne 0) { throw "nssm $($args -join ' ') failed" } }

if ($existing) { Write-Host "Updating existing service $ServiceName"; & $Nssm stop $ServiceName | Out-Null }
else { N install $ServiceName $venvPy }

N set $ServiceName Application $venvPy
N set $ServiceName AppParameters "-m uvicorn app.main:app --host 127.0.0.1 --port $port --workers 2 --proxy-headers"
N set $ServiceName AppDirectory $backend
N set $ServiceName DisplayName 'EZLine Calendar API (ezlcal)'
N set $ServiceName Start SERVICE_AUTO_START
N set $ServiceName AppStdout (Join-Path $logs 'ezlcal-out.log')
N set $ServiceName AppStderr (Join-Path $logs 'ezlcal-err.log')
N set $ServiceName AppRotateFiles 1
N set $ServiceName AppRotateBytes 5242880

& $Nssm start $ServiceName | Out-Null
Start-Sleep -Seconds 4
try {
  $h = Invoke-RestMethod "http://127.0.0.1:$port/api/health" -TimeoutSec 10
  Write-Host "Service running. Health: $($h | ConvertTo-Json -Compress)"
} catch {
  Write-Warning "Service installed but /api/health did not answer. Look at $logs\ezlcal-err.log"
}
