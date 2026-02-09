import cv2
import mediapipe as mp
import pandas as pd
import os
import time

METRICS_CSV = "data/real_time_student_metrics.csv"


def start_monitoring(duration_minutes=5, stop_callback=lambda: False):

    # Initialize webcam
    cap = cv2.VideoCapture(0)

    if not cap.isOpened():
        print("Error: Cannot open webcam")
        return

    # Initialize Mediapipe FaceMesh ONCE (important for performance)
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(static_image_mode=False)

    cont_attention = 0
    cont_distraction = 0
    second_number = 1

    start_time = time.time()

    print("Monitoring started...")

    while (time.time() - start_time) < duration_minutes * 60:

        # Stop button support
        if stop_callback():
            print("Monitoring stopped by user.")
            break

        ret, frame = cap.read()

        if not ret:
            continue

        # Convert frame
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        # Detect face
        results = face_mesh.process(rgb_frame)

        face_present = "Yes" if results.multi_face_landmarks else "No"

        # Update attention logic
        if face_present == "Yes":
            cont_attention += 1
            cont_distraction = 0
        else:
            cont_distraction += 1
            cont_attention = 0

        # Engagement level
        if cont_attention >= 5:
            engagement = "High"
        elif cont_distraction >= 5:
            engagement = "Low"
        else:
            engagement = "Medium"

        # Confusion level
        if cont_distraction >= 5:
            confusion = "High"
        else:
            confusion = "Low"

        # Save metrics
        row = {
            "Second": second_number,
            "Face_Present": face_present,
            "Continuous_Attention": cont_attention,
            "Continuous_Distraction": cont_distraction,
            "Engagement": engagement,
            "Confusion": confusion,
            "Timestamp": time.strftime("%Y-%m-%d %H:%M:%S")
        }

        # Create folder if not exists
        os.makedirs("data", exist_ok=True)

        # Save CSV safely
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

        second_number += 1

        # Wait 1 second → REAL TIME
        time.sleep(1)

    # Cleanup
    cap.release()
    cv2.destroyAllWindows()

    print("Monitoring finished.")
