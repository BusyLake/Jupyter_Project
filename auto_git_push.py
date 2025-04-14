import os
import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler
from datetime import datetime

# ログファイルのパス
log_file = f"logs/git_log_{datetime.now().strftime('%Y-%m-%d')}.log"

def write_log(message):
    timestamp = datetime.now().strftime("[%Y-%m-%d %H:%M:%S]")
    with open(log_file, "a", encoding="utf-8") as f:
        f.write(f"{timestamp} {message}\n")
    print(f"{timestamp} {message}")

class GitAutoPusher(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(".ipynb") and ".ipynb_checkpoints" not in event.src_path:
            write_log(f"📁 変更検知: {event.src_path}")
            try:
                subprocess.run(["git", "add", "."], check=True)
                subprocess.run(["git", "commit", "-m", "Auto commit from watchdog"], check=True)
                subprocess.run(["git", "push"], check=True)
                write_log("✅ 自動コミット＆プッシュ完了")
            except subprocess.CalledProcessError as e:
                write_log(f"❌ エラー: {e}")

if __name__ == "__main__":
    path = "."
    event_handler = GitAutoPusher()
    observer = Observer()
    observer.schedule(event_handler, path, recursive=True)
    observer.start()
    try:
        write_log("👀 .ipynbファイルの変更を監視中... Ctrl+Cで終了します。")
        while True:
            time.sleep(1)
    except KeyboardInterrupt:
        observer.stop()
        write_log("🛑 監視停止")
    observer.join()