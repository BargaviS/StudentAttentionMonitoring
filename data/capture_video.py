import cv2
import os
from datetime import datetime

# Folder to save raw videos
RAW_VIDEO_PATH = "../data/raw_videos"
os.makedirs(RAW_VIDEO_PATH, exist_ok=True)

def capture_video(duration_minutes=5, fps=20, resolution=(640,480)):
    """
    Captures live webcam video for given duration in minutes
    and saves it as an .mp4 file with a timestamped filename.
    """
    cap = cv2.VideoCapture(0)  # 0 = default webcam
    width, height = resolution
    cap.set(3, width)
    cap.set(4, height)

    # Output file with timestamp
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"{RAW_VIDEO_PATH}/class_{timestamp}.mp4"
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(filename, fourcc, fps, resolution)

    print(f"[INFO] Recording started for {duration_minutes} minutes...")
    total_frames = duration_minutes * 60 * fps
    frame_count = 0

    while frame_count < total_frames:
        ret, frame = cap.read()
        if not ret:
            print("[ERROR] Failed to capture frame.")
            break

        out.write(frame)
        frame_count += 1

        # Optional: display live feed
        cv2.imshow('Recording', frame)
        if cv2.waitKey(1) & 0xFF == ord('q'):
            print("[INFO] Recording stopped manually.")
            break

    cap.release()
    out.release()
    cv2.destroyAllWindows()
    print(f"[INFO] Recording saved: {filename}")
    return filename

if __name__ == "__main__":
    # Example: record 5 minutes
    capture_video(duration_minutes=5)
