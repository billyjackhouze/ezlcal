# deploy.ps1 -- pull latest code, update Python deps, migrate, publish static files, restart the service.
# Windows PowerShell 5.1:  powershell.exe -ExecutionPolicy Bypass -File .\scripts\deploy.ps1 [-Seed] [-CreateUsers] [-NoPull]
#   -Seed         load backend\seed\seed.json (first deploy; safe to repeat, never overwrites edited events)
#   -CreateUsers  create a login for each staff member and print temporary passwords once
param(
  [switch]$Seed,
  [switch]$CreateUsers,
  [switch]$NoPull,
  [string]$ServiceName = 'ezlcal',
  [string]$Python = 'py'          # 'py' launcher; pass a full python.exe path if the launcher isn't installed
)
$ErrorActionPreference = 'Stop'
$root    = Split-Path -Parent $PSScriptRoot
$backend = Join-Path $root 'backend'
$venvPy  = Join-Path $backend '.venv\Scripts\python.exe'
$dist    = Join-Path $backend 'dist'
$envFile = Join-Path $backend '.env'

function Check([string]$step) { if ($LASTEXITCODE -ne 0) { throw "$step failed (exit $LASTEXITCODE)" } }

if (-not (Test-Path $envFile)) { throw "backend\.env is missing. Run scripts\create-database.ps1 first." }
$port = ((Get-Content $envFile | Where-Object { $_ -match '^PORT=' }) -replace '^PORT=', '').Trim()
if (-not $port) { throw 'PORT is not set in backend\.env' }

Set-Location $root
if (-not $NoPull) {
  $dirty = git status --porcelain --untracked-files=no
  if ($dirty) { throw "Local changes would block git pull:`n$dirty`nUndo them (git checkout -- <file>) and re-run." }
  $before = git rev-parse HEAD
  git pull --ff-only; Check 'git pull'
  $after = git rev-parse HEAD
  if ($before -eq $after) { Write-Host 'Already up to date.' } else { Write-Host "Updated $($before.Substring(0,7)) -> $($after.Substring(0,7))" }
}

if (-not (Test-Path $venvPy)) {
  Write-Host 'Creating Python virtual environment...'
  if ($Python -eq 'py') { & py -3 -m venv (Join-Path $backend '.venv') } else { & $Python -m venv (Join-Path $backend '.venv') }
  Check 'venv create'
}
& $venvPy -m pip install --upgrade pip --quiet; Check 'pip upgrade'
& $venvPy -m pip install -r (Join-Path $backend 'requirements.txt') --quiet; Check 'pip install'

Push-Location $backend
try {
  & $venvPy -m app.manage migrate; Check 'migrate'
  if ($Seed)        { & $venvPy -m app.manage seed;         Check 'seed' }
  if ($CreateUsers) { & $venvPy -m app.manage create-users; Check 'create-users' }
} finally { Pop-Location }

# publish static files to backend\dist (IIS physical path)
if (-not (Test-Path $dist)) { New-Item -ItemType Directory $dist | Out-Null }
robocopy (Join-Path $root 'web') $dist /MIR /XF web.config.template /NFL /NDL /NJH /NJS /NP | Out-Null
if ($LASTEXITCODE -ge 8) { throw "robocopy failed (exit $LASTEXITCODE)" }
$global:LASTEXITCODE = 0
(Get-Content (Join-Path $root 'web\web.config.template') -Raw).Replace('__PORT__', $port) |
  Set-Content (Join-Path $dist 'web.config') -Encoding UTF8
Write-Host "Static files published to $dist (API proxied to 127.0.0.1:$port)."

$svc = Get-Service -Name $ServiceName -ErrorAction SilentlyContinue
if ($svc) {
  Restart-Service $ServiceName
  Start-Sleep -Seconds 3
  try {
    $h = Invoke-RestMethod "http://127.0.0.1:$port/api/health" -TimeoutSec 10
    Write-Host "API healthy: $($h | ConvertTo-Json -Compress)"
  } catch { Write-Warning "Service restarted but /api/health did not answer: $($_.Exception.Message). Check logs\ezlcal-*.log" }
} else {
  Write-Host "Service '$ServiceName' not installed yet. Next: scripts\install-service.ps1"
}
