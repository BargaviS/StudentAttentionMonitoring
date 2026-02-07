import os
from datetime import datetime

def log_info(msg):
    print(f"[{datetime.now().strftime('%H:%M:%S')}] {msg}")

def create_folder(path):
    if not os.path.exists(path):
        os.makedirs(path)
        log_info(f"Folder created: {path}")
    else:
        log_info(f"Folder already exists: {path}")
