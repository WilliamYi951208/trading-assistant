$ErrorActionPreference = "Stop"

# 安装目标路径
$targets = @(
    "$env:USERPROFILE\.codex\skills\价格行为助手",
    "$env:USERPROFILE\.agents\skills\price-action-assistant"
)

$sourceDir = $PSScriptRoot

Write-Host "=== Price Action Trading Assistant 安装脚本 ===" -ForegroundColor Cyan
Write-Host "源目录: $sourceDir"

foreach ($target in $targets) {
    Write-Host "`n安装到: $target" -ForegroundColor Yellow

    if (-not (Test-Path $target)) {
        New-Item -ItemType Directory -Path $target -Force | Out-Null
        Write-Host "  创建目录: $target"
    }

    # 复制 SKILL.md
    Copy-Item "$sourceDir\SKILL.md" "$target\SKILL.md" -Force
    Write-Host "  已复制: SKILL.md"

    # 复制核心文件
    $coreFiles = @(
        "config.json",
        "webhook_receiver.py",
        "fetch_data.py",
        "portable-trading-context.md",
        "account-status.md"
    )

    foreach ($file in $coreFiles) {
        if (Test-Path "$sourceDir\$file") {
            Copy-Item "$sourceDir\$file" "$target\$file" -Force
            Write-Host "  已复制: $file"
        }
    }
}

# 确保输出目录存在
$outputDir = "G:\PriceAction\交易日志"
if (-not (Test-Path $outputDir)) {
    New-Item -ItemType Directory -Path $outputDir -Force | Out-Null
    Write-Host "`n创建输出目录: $outputDir"
}

$barsDir = "$outputDir\bars"
if (-not (Test-Path $barsDir)) {
    New-Item -ItemType Directory -Path $barsDir -Force | Out-Null
}

# 复制 AGENT_BOOTSTRAP.md 到输出目录
if (Test-Path "$outputDir\AGENT_BOOTSTRAP.md") {
    Write-Host "`nAGENT_BOOTSTRAP.md 已存在于输出目录"
}

Write-Host "`n=== 安装完成 ===" -ForegroundColor Green
Write-Host "Skill 已安装到:"
foreach ($target in $targets) {
    Write-Host "  - $target"
}
Write-Host "输出目录: $outputDir"
Write-Host "`n使用方式:"
Write-Host "  1. 在 Agent 中说 '开始做单' 启动自动分析"
Write-Host "  2. 说 '停' 停止分析"
Write-Host "  3. 分析结果在: $outputDir\latest-codex-brief.md"
