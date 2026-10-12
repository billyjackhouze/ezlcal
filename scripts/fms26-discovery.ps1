# fms26-discovery.ps1  --  READ-ONLY. Changes nothing on the server.
# Run in an elevated *Windows PowerShell 5.1* window (powershell.exe, not pwsh):
#   powershell.exe -ExecutionPolicy Bypass -File .\fms26-discovery.ps1
# Writes the report to your Desktop as fms26-discovery.txt -- upload that file to the chat.

$out = Join-Path ([Environment]::GetFolderPath('Desktop')) 'fms26-discovery.txt'
function Section($t) { "`r`n===== $t =====" | Out-File $out -Append -Encoding utf8 }
function Run($t, [scriptblock]$b) {
  Section $t
  try { (& $b 2>&1 | Out-String -Width 220) | Out-File $out -Append -Encoding utf8 }
  catch { "ERROR: $($_.Exception.Message)" | Out-File $out -Append -Encoding utf8 }
}

"fms26 discovery  $(Get-Date -Format s)" | Out-File $out -Encoding utf8

Run 'PowerShell / OS'        { $PSVersionTable.PSVersion; (Get-CimInstance Win32_OperatingSystem).Caption }
Run 'Disk space'             { Get-PSDrive -PSProvider FileSystem | Select-Object Name, @{n='FreeGB';e={[math]::Round($_.Free/1GB,1)}}, @{n='UsedGB';e={[math]::Round($_.Used/1GB,1)}} }
Run 'Python'                 { where.exe python; python --version; py -0p }
Run 'Node'                   { where.exe node; node -v }
Run 'Git'                    { where.exe git; git --version; git config --system credential.helper }
Run 'PostgreSQL services'    { Get-Service | Where-Object { $_.Name -like 'postgres*' } | Select-Object Name, Status, StartType }
Run 'PostgreSQL installs'    { Get-ChildItem 'C:\Program Files\PostgreSQL' -ErrorAction SilentlyContinue | Select-Object Name }
Run 'NSSM'                   { where.exe nssm; Get-ChildItem C:\nssm* -Recurse -Filter nssm.exe -ErrorAction SilentlyContinue | Select-Object FullName }
Run 'Services running python/uvicorn/node' {
  Get-CimInstance Win32_Service | Where-Object { $_.PathName -match 'python|uvicorn|node|nssm' } |
    Select-Object Name, State, StartMode, PathName
}
Run 'Loopback listeners (ports in use)' { netstat -an | findstr LISTENING | findstr "127.0.0.1" }
Run 'All 80/443 listeners'   { netstat -an | findstr LISTENING | findstr ":80 :443" }

Import-Module WebAdministration -ErrorAction SilentlyContinue
Run 'IIS sites'              { Get-Website | Select-Object Name, ID, State, PhysicalPath }
Run 'IIS bindings'           { Get-WebBinding | Select-Object protocol, bindingInformation, sslFlags, ItemXPath }
Run 'IIS app pools'          { Get-ChildItem IIS:\AppPools | Select-Object Name, State, ManagedRuntimeVersion }
Run 'ARR / URL Rewrite'      {
  Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\IIS Extensions\URL Rewrite' -ErrorAction SilentlyContinue | Select-Object Version
  Get-ItemProperty 'HKLM:\SOFTWARE\Microsoft\IIS Extensions\Application Request Routing' -ErrorAction SilentlyContinue | Select-Object Version
  Get-WebConfigurationProperty -PSPath 'MACHINE/WEBROOT/APPHOST' -Filter 'system.webServer/proxy' -Name enabled -ErrorAction SilentlyContinue
}
Run 'SSL cert bindings'      { netsh http show sslcert }
Run 'Certificates (My + WebHosting)' {
  Get-ChildItem Cert:\LocalMachine\My, Cert:\LocalMachine\WebHosting -ErrorAction SilentlyContinue |
    Select-Object PSParentPath, Subject, NotAfter, Thumbprint
}
Run 'Existing app folders'   { Get-ChildItem C:\Apps, C:\inetpub -Directory -ErrorAction SilentlyContinue | Select-Object FullName }
Run 'Anything named ezl*'    { Get-ChildItem C:\ -Directory -Recurse -Depth 2 -Filter 'ezl*' -ErrorAction SilentlyContinue | Select-Object FullName }
Run 'FileMaker Server'       { Get-Service | Where-Object { $_.DisplayName -like '*FileMaker*' } | Select-Object Name, Status }

"`r`nDone. Report: $out" | Out-File $out -Append -Encoding utf8
Write-Host "Report written to $out"
