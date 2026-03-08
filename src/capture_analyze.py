import cv2
import mediapipe as mp
import pandas as pd
<<<<<<< HEAD
<<<<<<< HEAD
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

=======
>>>>>>> 0e0e79ddec796e691e7bb0d75cb22213e0e4dce1
import os
import time

METRICS_CSV = "data/real_time_student_metrics.csv"


def start_monitoring(duration_minutes=5, stop_callback=lambda: False):

<<<<<<< HEAD
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
=======
    # Initialize webcam
>>>>>>> ac466067f3199ca78cf9de9e668330a65000594f
>>>>>>> 0e0e79ddec796e691e7bb0d75cb22213e0e4dce1
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
<<<<<<< HEAD
=======
    start_time = time.time()

    # Initialize CSV
    pd.DataFrame(columns=[
        "Second", "Face_Present", "Continuous_Attention", "Continuous_Distraction"
    ]).to_csv(METRICS_CSV, index=False)

    while (time.time() - start_time) < duration_minutes * 60:
=======
>>>>>>> 0e0e79ddec796e691e7bb0d75cb22213e0e4dce1

    start_time = time.time()

    print("Monitoring started...")

    while (time.time() - start_time) < duration_minutes * 60:

<<<<<<< HEAD
       
=======
    start_time = time.time()

    
    pd.DataFrame(columns=[
        "Second", "Face_Present", "Continuous_Attention", "Continuous_Distraction"
    ]).to_csv(METRICS_CSV, index=False)

    while (time.time() - start_time) < duration_minutes * 60:
>>>>>>> 312f094 (Updated Streamlit app: real-time attention with sound alert and demo video)
=======
        # Stop button support
>>>>>>> ac466067f3199ca78cf9de9e668330a65000594f
>>>>>>> 0e0e79ddec796e691e7bb0d75cb22213e0e4dce1
        if stop_callback():
            print("Monitoring stopped by user.")
            break

        ret, frame = cap.read()

        if not ret:
            continue

<<<<<<< HEAD
<<<<<<< HEAD
       
=======
>>>>>>> 312f094 (Updated Streamlit app: real-time attention with sound alert and demo video)
=======
=======
        # Convert frame
>>>>>>> ac466067f3199ca78cf9de9e668330a65000594f
>>>>>>> 0e0e79ddec796e691e7bb0d75cb22213e0e4dce1
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
<<<<<<< HEAD
        
=======
        # Prepare metrics
=======
        # Engagement level
>>>>>>> 0e0e79ddec796e691e7bb0d75cb22213e0e4dce1
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

<<<<<<< HEAD
=======
        
>>>>>>> 312f094 (Updated Streamlit app: real-time attention with sound alert and demo video)
=======
        # Save metrics
>>>>>>> ac466067f3199ca78cf9de9e668330a65000594f
>>>>>>> 0e0e79ddec796e691e7bb0d75cb22213e0e4dce1
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
<<<<<<< HEAD
        
=======
        # Append to CSV
        pd.DataFrame([row]).to_csv(METRICS_CSV, mode='a', header=False, index=False)

        # Callback to Streamlit for live update
        if update_callback:
            update_callback(row)
=======
        # Create folder if not exists
>>>>>>> 0e0e79ddec796e691e7bb0d75cb22213e0e4dce1
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
<<<<<<< HEAD
=======
        
        pd.DataFrame([row]).to_csv(METRICS_CSV, mode='a', header=False, index=False)

        
        if update_callback:
            update_callback(row)
>>>>>>> 312f094 (Updated Streamlit app: real-time attention with sound alert and demo video)
=======
>>>>>>> ac466067f3199ca78cf9de9e668330a65000594f
>>>>>>> 0e0e79ddec796e691e7bb0d75cb22213e0e4dce1

        second_number += 1

       
        time.sleep(1)

    
    cap.release()
    cv2.destroyAllWindows()

    print("Monitoring finished.")
