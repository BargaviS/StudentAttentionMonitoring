def start_monitoring(duration_minutes=5, stop_callback=lambda: False):
    cap = cv2.VideoCapture(0)
    mp_face_mesh = mp.solutions.face_mesh.FaceMesh(static_image_mode=False)

    cont_attention = 0
    cont_distraction = 0
    second_number = 1
    start_time = cv2.getTickCount()

    while (cv2.getTickCount() - start_time)/cv2.getTickFrequency() < duration_minutes*60:
        # Check stop flag
        if stop_callback():
            break

        ret, frame = cap.read()
        if not ret:
            continue

        # Simple face detection
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

        # Save metrics to CSV (simplified)
        row = {
            "Second": second_number,
            "Face_Present": face_present,
            "Continuous_Attention": cont_attention,
            "Continuous_Distraction": cont_distraction
        }
        import pandas as pd
        METRICS_CSV = "../data/real_time_student_metrics.csv"
        if not pd.io.common.file_exists(METRICS_CSV):
            pd.DataFrame([row]).to_csv(METRICS_CSV, index=False)
        else:
            pd.DataFrame([row]).to_csv(METRICS_CSV, mode='a', header=False, index=False)

        second_number += 1

    cap.release()
