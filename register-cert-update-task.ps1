$ErrorActionPreference = "Stop"

$taskName = "VedtamCertDataUpdate"
$projectRoot = Split-Path -Parent $MyInvocation.MyCommand.Path
$runnerPath = Join-Path $projectRoot "run-cert-update-hidden.vbs"

if (-not (Test-Path $runnerPath)) {
  throw "Runner file not found: $runnerPath"
}

$action = New-ScheduledTaskAction -Execute "wscript.exe" -Argument "`"$runnerPath`"" -WorkingDirectory $projectRoot
$trigger = New-ScheduledTaskTrigger -Once -At "12:00AM" `
  -RepetitionInterval (New-TimeSpan -Minutes 15) `
  -RepetitionDuration (New-TimeSpan -Days 3650)
$settings = New-ScheduledTaskSettingsSet `
  -AllowStartIfOnBatteries `
  -DontStopIfGoingOnBatteries `
  -StartWhenAvailable

Register-ScheduledTask `
  -TaskName $taskName `
  -Action $action `
  -Trigger $trigger `
  -Settings $settings `
  -Description "Refreshes Vedtam CERT-In chart data 10 times a day (every 2.4 hours)." `
  -Force | Out-Null

Write-Host "Scheduled task '$taskName' registered successfully."
