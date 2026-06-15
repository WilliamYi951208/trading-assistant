# 创建启动快捷方式
$ErrorActionPreference = "Stop"

$startupFolder = [Environment]::GetFolderPath("Startup")
$shortcutPath = Join-Path $startupFolder "PriceActionWebhook.lnk"
$scriptPath = "g:\trading-helper\start-webhook-receiver.ps1"

# 创建 WScript.Shell 对象
$WScriptShell = New-Object -ComObject WScript.Shell
$shortcut = $WScriptShell.CreateShortcut($shortcutPath)
$shortcut.TargetPath = "powershell.exe"
$shortcut.Arguments = "-WindowStyle Hidden -ExecutionPolicy Bypass -File `"$scriptPath`""
$shortcut.WorkingDirectory = "g:\trading-helper"
$shortcut.Description = "Price Action Webhook Receiver"
$shortcut.Save()

Write-Host "✅ 启动快捷方式已创建" -ForegroundColor Green
Write-Host "位置: $shortcutPath"
Write-Host ""
Write-Host "下次开机会自动启动 webhook_receiver.py"
Write-Host "如需禁用，删除该快捷方式即可"
