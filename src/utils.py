def log_info(message):
    print(f"[INFO] {message}")

def create_folder(path):
    import os
    if not os.path.exists(path):
        os.makedirs(path)
