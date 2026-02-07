import cv2
import mediapipe as mp
import os
import pandas as pd
from datetime import datetime

# Paths
RAW_VIDEO_PATH = "../data/raw_videos"
PROCESSED_PATH = "../data/processed"
os.makedirs(PROCESSED_PATH, exist_ok=True)

# Mediapipe modules
mp_face = mp.solutions.face_mesh
mp_pose = mp.solutions.pose

def process_video(video_file, student_id="S1"):
    """
    Process video to extract frame-level features:
    - Face presence
    - Head orientation (placeholder)
    - Eye gaze (placeholder)
    - Posture (placeholder)
    Aggregates per-minute metrics and saves CSV in data/processed
    """
    cap = cv2.VideoCapture(video_file)
    fps = int(cap.get(cv2.CAP_PROP_FPS))

    face_mesh = mp_face.FaceMesh(static_image_mode=False)
    pose = mp_pose.Pose(static_image_mode=False)

    features = []
    frame_count = 0

    while True:
        ret, frame = cap.read()
        if not ret:
            break

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Face detection
        face_results = face_mesh.process(rgb_frame)
        face_present = "Yes" if face_results.multi_face_landmarks else "No"

        # Placeholder for head orientation, eye gaze, posture
        head_orientation = "Forward"
        eye_direction = "Screen"
        posture_state = "Upright"

        # Store frame-level feature
        features.append({
            "Student_ID": student_id,
            "Frame": frame_count,
            "Face_Present": face_present,
            "Head_Orientation": head_orientation,
            "Eye_Direction": eye_direction,
            "Posture_State": posture_state
        })

        frame_count += 1

    cap.release()
    print(f"[INFO] Video processed: {video_file}")

    # Aggregate per minute
    frames_per_minute = fps * 60
    aggregated = []
    for i in range(0, len(features), frames_per_minute):
        minute_frames = features[i:i+frames_per_minute]
        minute_number = i // frames_per_minute + 1

        face_count = sum(1 for f in minute_frames if f["Face_Present"] == "Yes")
        face_presence = "Yes" if face_count > len(minute_frames)/2 else "No"

        aggregated.append({
            "Student_ID": student_id,
            "Minute": minute_number,
            "Face_Present": face_presence,
            "Head_Orientation": "Forward",
            "Eye_Direction": "Screen",
            "Posture_State": "Upright"
        })

    # Save processed CSV
    timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
    output_file = os.path.join(PROCESSED_PATH, f"{student_id}_processed_{timestamp}.csv")
    pd.DataFrame(aggregated).to_csv(output_file, index=False)
    print(f"[INFO] Processed features saved: {output_file}")

    return output_file

if __name__ == "__main__":
    # Example usage
    sample_video = "../data/raw_videos/sample_video.mp4"  # replace with your video
    process_video(sample_video, student_id="S1")
