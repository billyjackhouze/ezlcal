# iis-site.ps1 -- creates the ezlcal IIS site with an HTTP host-header binding only.
# It never edits FileMaker Server's own site, bindings or certificate.
# HTTPS is a separate step once we've seen the certificate setup in fms26-discovery.txt.
# Elevated Windows PowerShell 5.1 (powershell.exe -- the IIS: drive does not work under pwsh 7):
#   powershell.exe -ExecutionPolicy Bypass -File .\scripts\iis-site.ps1
param(
  [string]$HostName = 'ezlcal.alamark.com',
  [string]$SiteName = 'ezlcal'
)
$ErrorActionPreference = 'Stop'
if ($PSVersionTable.PSVersion.Major -ne 5) { throw 'Run this in Windows PowerShell 5.1 (powershell.exe), not pwsh.' }
Import-Module WebAdministration
$root = Split-Path -Parent $PSScriptRoot
$dist = Join-Path $root 'backend\dist'
if (-not (Test-Path (Join-Path $dist 'index.html'))) { throw 'backend\dist is empty. Run scripts\deploy.ps1 first.' }

# 1. Refuse to collide with anything already bound to this hostname
$clash = Get-WebBinding | Where-Object { $_.bindingInformation -like "*:$HostName" -and $_.ItemXPath -notlike "*name='$SiteName'*" }
if ($clash) { $clash | Format-Table protocol, bindingInformation, ItemXPath; throw "$HostName is already bound on another site (above). Stopping." }

# 2. URL Rewrite + ARR proxy must be available for the /api rule
$rewrite = Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\IIS Extensions\URL Rewrite' -ErrorAction SilentlyContinue
if (-not $rewrite) { throw 'IIS URL Rewrite module is not installed. Install it, then re-run.' }
$proxy = Get-WebConfigurationProperty -PSPath 'MACHINE/WEBROOT/APPHOST' -Filter 'system.webServer/proxy' -Name enabled -ErrorAction SilentlyContinue
if (-not $proxy -or -not $proxy.Value) {
  Write-Warning 'ARR proxy is not enabled at the server level, so /api/* will 502. Tell Claude what fms26-discovery.txt showed before enabling it; it is a server-wide setting.'
}

# 3. App pool (no managed code) + site
if (-not (Test-Path "IIS:\AppPools\$SiteName")) {
  New-WebAppPool -Name $SiteName | Out-Null
  Set-ItemProperty "IIS:\AppPools\$SiteName" -Name managedRuntimeVersion -Value ''
  Write-Host "App pool $SiteName created."
}
if (-not (Get-Website -Name $SiteName -ErrorAction SilentlyContinue)) {
  New-Website -Name $SiteName -PhysicalPath $dist -ApplicationPool $SiteName -HostHeader $HostName -Port 80 | Out-Null
  Write-Host "Site $SiteName created: http://$HostName -> $dist"
} else {
  Set-ItemProperty "IIS:\Sites\$SiteName" -Name physicalPath -Value $dist
  Write-Host "Site $SiteName already existed; physical path confirmed."
}

# 4. App pool identity can read the files
& icacls $dist /grant "IIS AppPool\${SiteName}:(OI)(CI)RX" /T /Q | Out-Null
if ($LASTEXITCODE -ne 0) { throw 'icacls failed granting read access' }

# 5. Loopback test with a spoofed Host header (no DNS needed yet)
foreach ($path in '/', '/manifest.webmanifest', '/api/health') {
  try {
    $r = Invoke-WebRequest -Uri "http://127.0.0.1$path" -Headers @{ Host = $HostName } -UseBasicParsing -TimeoutSec 10
    Write-Host ("{0,-24} {1}" -f $path, $r.StatusCode)
  } catch { Write-Warning ("{0,-24} FAILED: {1}" -f $path, $_.Exception.Message) }
}
Write-Host 'HTTP site is in place. HTTPS binding comes next, once the certificate source is confirmed.'
