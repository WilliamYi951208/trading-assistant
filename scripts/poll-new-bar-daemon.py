"""
poll-new-bar-daemon.py — 持续轮询 VPS 检测新 K 线
检测到新 K 时写入 trigger 文件，配合 FileChanged hook 唤醒 Claude
"""
import sys
import time
import os
from urllib.request import urlopen, Request
from urllib.error import URLError

VPS_URL = "http://YOUR_VPS_IP/latest-brief"
STATE_FILE = os.path.join(os.environ.get("TEMP", "/tmp"), "claude-last-bar-index.txt")
TRIGGER_FILE = os.path.join(os.environ.get("TEMP", "/tmp"), "claude-new-bar-trigger.txt")

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
    last_index = load_last_index()

    while True:
        text = get_latest()
        current_index = extract_bar_index(text)

        if current_index and last_index and current_index != last_index:
            save_index(current_index)
            with open(TRIGGER_FILE, "w", encoding="utf-8") as f:
                f.write(text)

        if current_index and not last_index:
            last_index = current_index
            save_index(current_index)

        if current_index:
            last_index = current_index

        time.sleep(3)

if __name__ == "__main__":
    main()
