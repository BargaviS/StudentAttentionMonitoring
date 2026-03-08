import cv2
import mediapipe as mp
import pandas as pd
<<<<<<< HEAD
import os
import time

METRICS_CSV = "data/real_time_student_metrics.csv"


def start_monitoring(duration_minutes=5, stop_callback=lambda: False):

=======
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

>>>>>>> 312f094 (Updated Streamlit app: real-time attention with sound alert and demo video)
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Cannot open webcam")
        return
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False)

    cont_attention = 0
    cont_distraction = 0
    second_number = 1
<<<<<<< HEAD

    start_time = time.time()

    print("Monitoring started...")

    while (time.time() - start_time) < duration_minutes * 60:

       
=======
    start_time = time.time()

    
    pd.DataFrame(columns=[
        "Second", "Face_Present", "Continuous_Attention", "Continuous_Distraction"
    ]).to_csv(METRICS_CSV, index=False)

    while (time.time() - start_time) < duration_minutes * 60:
>>>>>>> 312f094 (Updated Streamlit app: real-time attention with sound alert and demo video)
        if stop_callback():
            print("Monitoring stopped by user.")
            break

        ret, frame = cap.read()

        if not ret:
            continue

<<<<<<< HEAD
       
=======
>>>>>>> 312f094 (Updated Streamlit app: real-time attention with sound alert and demo video)
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

       
        results = face_mesh.process(rgb_frame)

        face_present = "Yes" if results.multi_face_landmarks else "No"

        if face_present == "Yes":
            cont_attention += 1
            cont_distraction = 0
        else:
            cont_distraction += 1
            cont_attention = 0

<<<<<<< HEAD
        
        if cont_attention >= 5:
            engagement = "High"
        elif cont_distraction >= 5:
            engagement = "Low"
        else:
            engagement = "Medium"

       
        if cont_distraction >= 5:
            confusion = "High"
        else:
            confusion = "Low"

=======
        
>>>>>>> 312f094 (Updated Streamlit app: real-time attention with sound alert and demo video)
        row = {
            "Second": second_number,
            "Face_Present": face_present,
            "Continuous_Attention": cont_attention,
            "Continuous_Distraction": cont_distraction,
            "Engagement": engagement,
            "Confusion": confusion,
            "Timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }

<<<<<<< HEAD
        
        os.makedirs("data", exist_ok=True)

        
        if not os.path.exists(METRICS_CSV):
            pd.DataFrame([row]).to_csv(METRICS_CSV, index=False)
        else:
            pd.DataFrame([row]).to_csv(
                METRICS_CSV,
                mode='a',
                header=False,
                index=False
            )

        print(f"Second {second_number} | Attention: {engagement} | Confusion: {confusion}")
=======
        
        pd.DataFrame([row]).to_csv(METRICS_CSV, mode='a', header=False, index=False)

        
        if update_callback:
            update_callback(row)
>>>>>>> 312f094 (Updated Streamlit app: real-time attention with sound alert and demo video)

        second_number += 1

       
        time.sleep(1)

    
    cap.release()
    cv2.destroyAllWindows()

    print("Monitoring finished.")
