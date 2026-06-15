# 设置 webhook_receiver.py 开机自启动
$ErrorActionPreference = "Stop"

$taskName = "PriceActionWebhookReceiver"
$scriptPath = "g:\trading-helper\webhook_receiver.py"
$pythonPath = (Get-Command python).Source

# 创建任务计划
$action = New-ScheduledTaskAction -Execute $pythonPath -Argument $scriptPath -WorkingDirectory "g:\trading-helper"
$trigger = New-ScheduledTaskTrigger -AtStartup
$principal = New-ScheduledTaskPrincipal -UserId "$env:USERNAME" -LogonType Interactive -RunLevel Limited
$settings = New-ScheduledTaskSettingsSet -AllowStartIfOnBatteries -DontStopIfGoingOnBatteries -StartWhenAvailable

# 注册任务
Register-ScheduledTask -TaskName $taskName -Action $action -Trigger $trigger -Principal $principal -Settings $settings -Force

Write-Host "✅ 开机自启动已设置" -ForegroundColor Green
Write-Host "任务名称: $taskName"
Write-Host "脚本路径: $scriptPath"
Write-Host ""
Write-Host "管理方式:"
Write-Host "  - 查看: taskschd.msc（任务计划程序）"
Write-Host "  - 禁用: Disable-ScheduledTask -TaskName '$taskName'"
Write-Host "  - 删除: Unregister-ScheduledTask -TaskName '$taskName' -Confirm:`$false"
