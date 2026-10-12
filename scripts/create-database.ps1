# create-database.ps1 -- creates the ezlcal role + database and writes backend\.env
# Run ONCE from an elevated *Windows PowerShell 5.1* window (powershell.exe, not pwsh):
#   powershell.exe -ExecutionPolicy Bypass -File .\scripts\create-database.ps1
# Re-running is safe: it resets the ezlcal role password and rewrites .env to match.
param(
  [string]$PgBin   = 'C:\Program Files\PostgreSQL\15\bin',
  [string]$PgHost  = '127.0.0.1',            # never 'localhost' (resolves to ::1 and breaks auth)
  [int]   $PgPort  = 5432,
  [string]$DbName  = 'ezlcal',
  [string]$DbUser  = 'ezlcal',
  [int]   $ApiPort = 8090,
  [string]$PublicUrl = 'https://ezlcal.alamark.com'
)
$ErrorActionPreference = 'Stop'
$root = Split-Path -Parent $PSScriptRoot
$envFile = Join-Path $root 'backend\.env'
$psql = Join-Path $PgBin 'psql.exe'
if (-not (Test-Path $psql)) { throw "psql.exe not found at $psql. Pass -PgBin with the right folder." }

function New-Secret([int]$len) {
  $chars = 'ABCDEFGHJKLMNPQRSTUVWXYZabcdefghijkmnopqrstuvwxyz23456789'.ToCharArray()
  $bytes = New-Object byte[] $len
  [System.Security.Cryptography.RandomNumberGenerator]::Create().GetBytes($bytes)
  -join ($bytes | ForEach-Object { $chars[$_ % $chars.Length] })
}
function Invoke-Psql([string]$db, [string]$sql) {
  $out = & $psql -h $PgHost -p $PgPort -U postgres -d $db -v ON_ERROR_STOP=1 -tA -c $sql 2>&1
  if ($LASTEXITCODE -ne 0) { throw "psql failed: $out" }
  return $out
}

$superSecure = Read-Host 'Password for the postgres superuser' -AsSecureString
$env:PGPASSWORD = [Runtime.InteropServices.Marshal]::PtrToStringAuto([Runtime.InteropServices.Marshal]::SecureStringToBSTR($superSecure))
try {
  $appPw = New-Secret 32   # letters/digits only: safe inside a URL and inside PowerShell strings

  $exists = Invoke-Psql 'postgres' "SELECT 1 FROM pg_roles WHERE rolname='$DbUser'"
  if ($exists -match '1') {
    Invoke-Psql 'postgres' "ALTER ROLE $DbUser WITH LOGIN PASSWORD '$appPw'" | Out-Null
    Write-Host "Role $DbUser existed; password reset."
  } else {
    Invoke-Psql 'postgres' "CREATE ROLE $DbUser WITH LOGIN PASSWORD '$appPw'" | Out-Null
    Write-Host "Role $DbUser created."
  }

  $dbExists = Invoke-Psql 'postgres' "SELECT 1 FROM pg_database WHERE datname='$DbName'"
  if ($dbExists -match '1') {
    Write-Host "Database $DbName already exists; left as is."
  } else {
    Invoke-Psql 'postgres' "CREATE DATABASE $DbName OWNER $DbUser ENCODING 'UTF8'" | Out-Null
    Write-Host "Database $DbName created."
  }
  Invoke-Psql $DbName "GRANT ALL ON SCHEMA public TO $DbUser" | Out-Null

  $jwt = New-Secret 48
  $lines = @(
    "DATABASE_URL=postgresql://${DbUser}:${appPw}@${PgHost}:${PgPort}/${DbName}",
    "JWT_SECRET=$jwt",
    'TOKEN_DAYS=30',
    "PORT=$ApiPort",
    "PUBLIC_BASE_URL=$PublicUrl"
  )
  if (Test-Path $envFile) { Copy-Item $envFile "$envFile.bak" -Force; Write-Host 'Existing .env backed up to .env.bak' }
  [IO.File]::WriteAllLines($envFile, $lines)   # UTF-8 without BOM
  Write-Host "Wrote $envFile (API port $ApiPort)."
  Write-Host 'Done. Next: scripts\deploy.ps1 -Seed -CreateUsers'
}
finally {
  Remove-Item Env:\PGPASSWORD -ErrorAction SilentlyContinue
}
