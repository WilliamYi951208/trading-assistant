"""
poll-atas-bar.py — 监听 ATAS 本地文件变更，检测新 K 线，exit 2 唤醒 Claude Code
独立于 webhook 链路，监听 G:/PriceAction/交易日志/atas/latest-atas-brief.md
"""
import sys
import time
import os
import subprocess

BRIEF_FILE = r"G:\PriceAction\交易日志\atas\latest-atas-brief.md"
STATE_FILE = os.path.join(os.environ.get("TEMP", "/tmp"), "claude-atas-bar-index.txt")
LOCK_FILE = os.path.join(os.environ.get("TEMP", "/tmp"), "claude-poll-atas.lock")


def acquire_lock():
    my_pid = str(os.getpid())
    if os.path.exists(LOCK_FILE):
        try:
            old_pid = open(LOCK_FILE).read().strip()
            if old_pid and old_pid.isdigit():
                result = subprocess.run(
                    ["tasklist", "/FI", f"PID eq {old_pid}", "/NH"],
                    capture_output=True, text=True, timeout=3
                )
                if old_pid in result.stdout:
                    sys.exit(0)
        except Exception:
            pass
    with open(LOCK_FILE, "w") as f:
        f.write(my_pid)


def release_lock():
    try:
        os.remove(LOCK_FILE)
    except OSError:
        pass


def extract_bar_index(filepath):
    if not os.path.exists(filepath):
        return None
    try:
        with open(filepath, "r", encoding="utf-8") as f:
            for line in f:
                if "bar_index" in line:
                    parts = line.split("：") if "：" in line else line.split(":")
                    if len(parts) >= 2:
                        idx = parts[-1].strip()
                        if idx.isdigit():
                            return idx
    except Exception:
        pass
    return None


def load_last_index():
    if os.path.exists(STATE_FILE):
        with open(STATE_FILE, "r") as f:
            return f.read().strip()
    return ""


def save_index(idx):
    with open(STATE_FILE, "w") as f:
        f.write(idx)


def read_brief():
    if not os.path.exists(BRIEF_FILE):
        return None
    try:
        with open(BRIEF_FILE, "r", encoding="utf-8") as f:
            return f.read()
    except Exception:
        return None


def main():
    acquire_lock()
    last_index = load_last_index()

    try:
        while True:
            current_index = extract_bar_index(BRIEF_FILE)

            if current_index and last_index and current_index != last_index:
                save_index(current_index)
                text = read_brief() or ""
                msg = f"\n{'='*50}\n📊 ATAS 新 K 线通知\n{'='*50}\n{text}\n{'='*50}\n"
                sys.stderr.write(msg)
                sys.stderr.flush()
                release_lock()
                sys.exit(2)

            if current_index and not last_index:
                last_index = current_index
                save_index(current_index)

            time.sleep(3)
    except KeyboardInterrupt:
        release_lock()
        sys.exit(0)


if __name__ == "__main__":
    main()
