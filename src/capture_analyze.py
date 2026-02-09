import cv2
import mediapipe as mp
import pandas as pd
import time
import threading

METRICS_CSV = "data/real_time_student_metrics.csv"

def start_monitoring(duration_minutes=5, stop_callback=lambda: False, update_callback=None):
    """
    Real-time attention monitoring.
    - duration_minutes: run for N minutes
    - stop_callback: returns True to stop
    - update_callback: function to call with latest metrics (for Streamlit display)
    """

    cap = cv2.VideoCapture(0)
    mp_face_mesh = mp.solutions.face_mesh.FaceMesh(static_image_mode=False)

    cont_attention = 0
    cont_distraction = 0
    second_number = 1
    start_time = time.time()

    # Initialize CSV
    pd.DataFrame(columns=[
        "Second", "Face_Present", "Continuous_Attention", "Continuous_Distraction"
    ]).to_csv(METRICS_CSV, index=False)

    while (time.time() - start_time) < duration_minutes * 60:
        if stop_callback():
            break

        ret, frame = cap.read()
        if not ret:
            continue

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = mp_face_mesh.process(rgb_frame)
        face_present = "Yes" if results.multi_face_landmarks else "No"

        # Update attention/distraction
        if face_present == "Yes":
            cont_attention += 1
            cont_distraction = 0
        else:
            cont_distraction += 1
            cont_attention = 0

        # Prepare metrics
        row = {
            "Second": second_number,
            "Face_Present": face_present,
            "Continuous_Attention": cont_attention,
            "Continuous_Distraction": cont_distraction
        }

        # Append to CSV
        pd.DataFrame([row]).to_csv(METRICS_CSV, mode='a', header=False, index=False)

        # Callback to Streamlit for live update
        if update_callback:
            update_callback(row)

        second_number += 1

    cap.release()
