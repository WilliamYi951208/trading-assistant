#!/bin/bash
# poll-new-bar.sh — 轮询 VPS 检测新 K 线，有新数据则 exit 2 唤醒 Claude
# 用于 Claude Code asyncRewake hook

VPS_URL="http://YOUR_VPS_IP/latest-brief"
STATE_FILE="/tmp/claude-last-bar-index"

# 读取上次的 bar_index
LAST_INDEX=""
if [ -f "$STATE_FILE" ]; then
    LAST_INDEX=$(cat "$STATE_FILE")
fi

# 每 3 秒轮询一次，最多等 295 秒（略小于 5 分钟）
for i in $(seq 1 98); do
    RESPONSE=$(curl -s --connect-timeout 3 "$VPS_URL" 2>/dev/null)
    if [ $? -ne 0 ] || [ -z "$RESPONSE" ]; then
        sleep 3
        continue
    fi

    # 提取 bar_index
    CURRENT_INDEX=$(echo "$RESPONSE" | grep "bar_index" | grep -o '[0-9]*')

    if [ -z "$CURRENT_INDEX" ]; then
        sleep 3
        continue
    fi

    # 如果是新 K（bar_index 变了）
    if [ -n "$LAST_INDEX" ] && [ "$CURRENT_INDEX" != "$LAST_INDEX" ]; then
        # 保存新的 bar_index
        echo "$CURRENT_INDEX" > "$STATE_FILE"
        # 输出数据到 stderr（会被 Claude 看到）
        echo "$RESPONSE" >&2
        # exit 2 唤醒 Claude
        exit 2
    fi

    # 第一次运行，记录当前 index
    if [ -z "$LAST_INDEX" ]; then
        LAST_INDEX="$CURRENT_INDEX"
        echo "$CURRENT_INDEX" > "$STATE_FILE"
    fi

    sleep 3
done

# 超时没有新 K，正常退出不唤醒
exit 0
