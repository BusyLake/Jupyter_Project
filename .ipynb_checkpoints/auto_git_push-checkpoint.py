import time
import subprocess
from watchdog.observers import Observer
from watchdog.events import FileSystemEventHandler

class NotebookEventHandler(FileSystemEventHandler):
    def on_modified(self, event):
        if event.src_path.endswith(".ipynb"):
            print(f"🔁 {event.src_path} が保存されました。Gitに自動Pushします...")
            try:
                subprocess.run(["git", "add", "."], check=True)
                subprocess.run(["git", "commit", "-m", "Auto commit from Jupyter save"], check=True)
                subprocess.run(["git", "push"], check=True)
                print("✅ Push 完了！")
            except subprocess.CalledProcessError as e:
                print("⚠️ Git操作に失敗しました：", e)

# 監視するフォルダのパスを指定
watch_path = "C:/Users/Busy_Lake/jupyter_project"

event_handler = NotebookEventHandler()
observer = Observer()
observer.schedule(event_handler, watch_path, recursive=True)
observer.start()

print("👀 .ipynbファイルの変更を監視中... Ctrl+Cで終了します。")
try:
    while True:
        time.sleep(1)
except KeyboardInterrupt:
    observer.stop()
observer.join()
