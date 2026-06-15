#!/bin/bash
# deploy-vps.sh — 一键部署 TradingView webhook receiver 到阿里云 VPS
# 用法: bash deploy-vps.sh

set -e

echo "=== TradingView Webhook Receiver VPS 部署 ==="

# 创建目录
echo "[1/5] 创建目录..."
mkdir -p /opt/trading-helper/data/bars
mkdir -p /opt/trading-helper/webhook-data

# 复制配置（重命名为 config.json）
echo "[2/5] 写入配置..."
cp /opt/trading-helper/config.vps.json /opt/trading-helper/config.json

# 安装 systemd service
echo "[3/5] 安装 systemd service..."
cp /opt/trading-helper/webhook-receiver.service /etc/systemd/system/
systemctl daemon-reload
systemctl enable webhook-receiver
systemctl restart webhook-receiver

# 开放防火墙端口
echo "[4/5] 开放 8787 端口..."
if command -v firewall-cmd &> /dev/null; then
    firewall-cmd --permanent --add-port=8787/tcp
    firewall-cmd --reload
elif command -v ufw &> /dev/null; then
    ufw allow 8787/tcp
else
    echo "  [跳过] 未检测到 firewall-cmd 或 ufw，请手动在阿里云安全组开放 8787 端口"
fi

# 验证
echo "[5/5] 验证服务状态..."
sleep 2
if curl -s http://127.0.0.1:8787/health | grep -q '"ok": true'; then
    echo ""
    echo "=== 部署成功 ==="
    echo "服务已启动: http://0.0.0.0:8787"
    echo ""
    echo "可用端点:"
    echo "  GET  /health       — 健康检查"
    echo "  GET  /latest-brief — 最新 K 线分析"
    echo "  GET  /bars         — 最近 20 根 K 线"
    echo "  GET  /status       — 会话状态"
    echo "  POST /start        — 激活会话"
    echo "  POST /stop         — 停止会话"
    echo "  POST /webhook      — 接收 TradingView 数据"
    echo ""
    echo "下一步:"
    echo "  1. 阿里云安全组开放 8787 端口（入方向）"
    echo "  2. TradingView Alert URL 改为: http://<公网IP>:8787/webhook"
    echo "  3. Alert JSON body 中加入: \"secret\": \"YOUR_WEBHOOK_SECRET_HERE\""
else
    echo ""
    echo "=== 部署可能失败 ==="
    echo "请检查: systemctl status webhook-receiver"
fi
