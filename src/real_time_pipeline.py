import cv2
import mediapipe as mp
import pandas as pd
import threading
import time
from datetime import datetime
from utils import log_info, create_folder
import os

RAW_VIDEO_PATH = "../data/raw_videos"       
PROCESSED_PATH = "../data/processed"       
METRICS_CSV = "../data/real_time_student_metrics.csv"

create_folder(RAW_VIDEO_PATH)
create_folder(PROCESSED_PATH)

mp_face = mp.solutions.face_mesh

ATTENTION_ALERT_THRESHOLD = 0.5     
CONFUSION_ALERT_DURATION = 2       

STUDENT_IDS = ["S1", "S2"]  
CAMERA_IDS = [0, 1]        

def update_metrics(student_id, features, second_number, last_metrics):
    """
    Compute attention, engagement, confusion in real-time per second
    last_metrics: dict to store continuous attention/distraction to avoid CSV read every second
    """
    face_count = sum(1 for f in features if f["Face_Present"] == "Yes")
    face_presence = "Yes" if face_count > len(features)/2 else "No"

    continuous_attention = last_metrics[student_id]["Continuous_Attention"]
    continuous_distraction = last_metrics[student_id]["Continuous_Distraction"]

    if face_presence == "Yes":
        continuous_attention += 1
        continuous_distraction = 0
    else:
        continuous_distraction += 1
        continuous_attention = 0

    last_metrics[student_id]["Continuous_Attention"] = continuous_attention
    last_metrics[student_id]["Continuous_Distraction"] = continuous_distraction

    if continuous_attention >= 20:
        engagement_level = "High"
        confusion_level = "Low"
    elif continuous_distraction >= 10:
        engagement_level = "Low"
        confusion_level = "High"
    else:
        engagement_level = "Medium"
        confusion_level = "Medium"

    if continuous_attention/second_number < ATTENTION_ALERT_THRESHOLD:
        log_info(f"[ALERT] Student {student_id} attention low at second {second_number}")

    row = {
        "Student_ID": student_id,
        "Second": second_number,
        "Face_Present": face_presence,
        "Continuous_Attention": continuous_attention,
        "Continuous_Distraction": continuous_distraction,
        "Engagement_Level": engagement_level,
        "Confusion_Level": confusion_level,
        "Timestamp": datetime.now()
    }

    if not os.path.exists(METRICS_CSV):
        pd.DataFrame([row]).to_csv(METRICS_CSV, index=False)
    else:
        pd.DataFrame([row]).to_csv(METRICS_CSV, mode='a', header=False, index=False)

def start_real_time_monitoring(duration_minutes=5, stop_event=None):
    """
    Multi-student, live frame processing pipeline with safe stop
    """
    if stop_event is None:
        stop_event = threading.Event()

    cap_dict = {}
    face_mesh_dict = {}

    for student_id, cam_id in zip(STUDENT_IDS, CAMERA_IDS):
        cap_dict[student_id] = cv2.VideoCapture(cam_id)
        face_mesh_dict[student_id] = mp_face.FaceMesh(static_image_mode=False)

    start_time = time.time()
    second_number = 1
    features_per_student = {s: [] for s in STUDENT_IDS}
    last_metrics = {s: {"Continuous_Attention":0, "Continuous_Distraction":0} for s in STUDENT_IDS}

    log_info(f"Monitoring started for {duration_minutes} minutes")

    while not stop_event.is_set() and (time.time() - start_time) < duration_minutes * 60:
        for student_id, cap in cap_dict.items():
            ret, frame = cap.read()
            if not ret:
                continue
            rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

            results = face_mesh_dict[student_id].process(rgb_frame)
            face_present = "Yes" if results.multi_face_landmarks else "No"

            head_orientation = "Forward"
            eye_direction = "Screen"
            posture_state = "Upright"

            features_per_student[student_id].append({
                "Face_Present": face_present,
                "Head_Orientation": head_orientation,
                "Eye_Direction": eye_direction,
                "Posture_State": posture_state
            })

            cv2.imshow(f"{student_id} Live Feed", frame)

        if second_number % 1 == 0:
            for student_id in STUDENT_IDS:
                update_metrics(student_id, features_per_student[student_id], second_number, last_metrics)
                features_per_student[student_id] = []  # reset for next second
            second_number += 1

        if cv2.waitKey(1) & 0xFF == ord('q'):
            log_info("Manual stop pressed.")
            stop_event.set()
            break
    for cap in cap_dict.values():
        cap.release()
    cv2.destroyAllWindows()
    log_info("Monitoring completed.")

def start_dashboard_thread(refresh_sec=5):
    from dashboard import live_dashboard
    live_dashboard(refresh_sec=refresh_sec)
