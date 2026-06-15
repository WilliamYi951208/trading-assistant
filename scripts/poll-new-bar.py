"""
poll-new-bar.py — 轮询 VPS 检测新 K 线，有新数据则 exit 2 唤醒 Claude Code
用于 Claude Code asyncRewake hook (SessionStart)
"""
import sys
import time
import json
import os
import subprocess
from urllib.request import urlopen, Request
from urllib.error import URLError

VPS_URL = "http://YOUR_VPS_IP/latest-brief"
STATE_FILE = os.path.join(os.environ.get("TEMP", "/tmp"), "claude-last-bar-index.txt")
LOCK_FILE = os.path.join(os.environ.get("TEMP", "/tmp"), "claude-poll-new-bar.lock")


def acquire_lock():
    """确保只有一个实例在跑。如果已有实例，直接退出。"""
    my_pid = str(os.getpid())
    if os.path.exists(LOCK_FILE):
        try:
            old_pid = open(LOCK_FILE).read().strip()
            if old_pid and old_pid.isdigit():
                # Windows 可靠检查：用 tasklist 查进程
                result = subprocess.run(
                    ["tasklist", "/FI", f"PID eq {old_pid}", "/NH"],
                    capture_output=True, text=True, timeout=3
                )
                if old_pid in result.stdout:
                    sys.exit(0)  # 旧进程还活着，静默退出
        except Exception:
            pass
    with open(LOCK_FILE, "w") as f:
        f.write(my_pid)


def release_lock():
    try:
        os.remove(LOCK_FILE)
    except OSError:
        pass

def get_latest():
    try:
        req = Request(VPS_URL)
        with urlopen(req, timeout=5) as resp:
            return resp.read().decode("utf-8")
    except (URLError, OSError):
        return None

def extract_bar_index(text):
    if not text:
        return None
    for line in text.splitlines():
        if "bar_index" in line:
            parts = line.split("：") if "：" in line else line.split(":")
            if len(parts) >= 2:
                idx = parts[-1].strip()
                if idx.isdigit():
                    return idx
    return None

def load_last_index():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return f.read().strip()
    return ""

def save_index(idx):
    with open(STATE_FILE, "w") as f:
        f.write(idx)

def main():
    acquire_lock()  # 确保只有一个实例
    last_index = load_last_index()

    try:
        while True:  # 无限循环，持续监听
            text = get_latest()
            current_index = extract_bar_index(text)

            if current_index and last_index and current_index != last_index:
                save_index(current_index)
                msg = f"\n{'='*50}\n新 K 线通知\n{'='*50}\n{text}\n"
                sys.stderr.write(msg)
                sys.stderr.flush()
                release_lock()
                sys.exit(2)  # 唤醒 Claude，脚本结束

            if current_index and not last_index:
                last_index = current_index
                save_index(current_index)

            time.sleep(3)
    except KeyboardInterrupt:
        release_lock()
        sys.exit(0)

if __name__ == "__main__":
    main()
