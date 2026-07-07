$ProjectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$BackendRoot = Join-Path $ProjectRoot "backend"
$FrontendRoot = Join-Path $ProjectRoot "frontend"
$LogFolder = Join-Path $BackendRoot "storage\logs"
$PythonExe = Join-Path $BackendRoot ".venv\Scripts\python.exe"
$OldRootPythonExe = Join-Path $ProjectRoot ".venv\Scripts\python.exe"
$BackendPort = 8010
$FrontendPort = 8028

New-Item -ItemType Directory -Force -Path $LogFolder | Out-Null

if (!(Test-Path $PythonExe)) {
  if (Test-Path $OldRootPythonExe) {
    $PythonExe = $OldRootPythonExe
  } else {
    $PythonExe = "python"
  }
}

function Stop-ByteBotPort {
  param([int]$Port)

  $listeners = Get-NetTCPConnection -LocalPort $Port -State Listen -ErrorAction SilentlyContinue

  foreach ($listener in $listeners) {
    $process = Get-Process -Id $listener.OwningProcess -ErrorAction SilentlyContinue

    if ($process -and $process.ProcessName -like "python*") {
      Write-Host "Stopping old Byte-Bot python server on port $Port..."
      Stop-Process -Id $process.Id -Force
    }
  }
}

Stop-ByteBotPort -Port $BackendPort
Stop-ByteBotPort -Port $FrontendPort
Start-Sleep -Milliseconds 700

Write-Host "Starting Byte-Bot backend on http://127.0.0.1:$BackendPort ..."
Start-Process `
  -FilePath $PythonExe `
  -ArgumentList @("-m", "uvicorn", "backend.app.main:app", "--host", "127.0.0.1", "--port", "$BackendPort") `
  -WorkingDirectory $ProjectRoot `
  -WindowStyle Hidden `
  -RedirectStandardOutput (Join-Path $LogFolder "backend.log") `
  -RedirectStandardError (Join-Path $LogFolder "backend-error.log")

Start-Sleep -Seconds 3

Write-Host "Starting Byte-Bot frontend on http://127.0.0.1:$FrontendPort/chat.html ..."
Start-Process `
  -FilePath $PythonExe `
  -ArgumentList @("-m", "http.server", "$FrontendPort", "--bind", "127.0.0.1") `
  -WorkingDirectory $FrontendRoot `
  -WindowStyle Hidden `
  -RedirectStandardOutput (Join-Path $LogFolder "frontend.log") `
  -RedirectStandardError (Join-Path $LogFolder "frontend-error.log")

Start-Sleep -Seconds 1
Start-Process "http://127.0.0.1:$FrontendPort/chat.html"

Write-Host ""
Write-Host "Byte-Bot is starting."
Write-Host "Backend:  http://127.0.0.1:$BackendPort/health"
Write-Host "Frontend: http://127.0.0.1:$FrontendPort/chat.html"
Write-Host "Logs:     $LogFolder"
