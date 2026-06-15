@echo off
chcp 65001 >nul
echo ===================================
echo   GC Scalp 交易环境一键启动
echo ===================================
echo.

:: 取消代理（ngrok 不兼容 Clash 代理）
set HTTP_PROXY=
set HTTPS_PROXY=
set http_proxy=
set https_proxy=

:: 启动 webhook 接收器
echo [1/2] 启动 webhook_receiver.py (port 8787)...
start "Webhook Receiver" cmd /k "cd /d G:\trading-helper && python webhook_receiver.py"
timeout /t 2 /nobreak >nul

:: 启动 ngrok
echo [2/2] 启动 ngrok (tunneling to 8787)...
start "ngrok" cmd /k "set HTTP_PROXY= && set HTTPS_PROXY= && ngrok http 8787"
timeout /t 3 /nobreak >nul

echo.
echo ===================================
echo   全部启动完成！
echo ===================================
echo.
echo   - webhook_receiver: http://127.0.0.1:8787
echo   - ngrok: 查看 ngrok 窗口获取公网 URL
echo   - 健康检查: http://127.0.0.1:8787/health
echo.
echo   注意：如果 ngrok URL 变了，需要去 TradingView 更新 Alert 的 Webhook URL
echo   当前固定域名: YOUR_NGROK_DOMAIN.ngrok-free.dev
echo.
pause
