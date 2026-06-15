Set-Location $PSScriptRoot
Start-Process python -ArgumentList ".\webhook_receiver.py" -WindowStyle Hidden -PassThru | ForEach-Object {
    $_.Id | Out-File "$PSScriptRoot\webhook-receiver.pid" -Force
}
Write-Host "webhook_receiver.py started (PID saved to webhook-receiver.pid)"
