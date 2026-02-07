import streamlit as st
import pandas as pd
import cv2
import mediapipe as mp
import time
import os

st.set_page_config(page_title="Real-Time Student Attention", layout="wide")
st.title("📊 Real-Time Student Attention Monitoring")

# ---------------- Session state ----------------
if "stop_monitor" not in st.session_state:
    st.session_state.stop_monitor = False

duration = st.number_input("Class duration (minutes)", min_value=1, max_value=60, value=5)
start_button = st.button("Start Monitoring")
stop_button = st.button("Stop Monitoring")

METRICS_CSV = "../data/real_time_student_metrics.csv"

# ---------------- Start Monitoring ----------------
if start_button:
    st.session_state.stop_monitor = False

    # Clear old CSV
    if os.path.exists(METRICS_CSV):
        os.remove(METRICS_CSV)

    st.success("Monitoring started!")

    # Placeholders for live update
    chart_placeholder = st.empty()
    table_placeholder = st.empty()
    alert_placeholder = st.empty()

    # Initialize webcam and mediapipe
    cap = cv2.VideoCapture(0)
    mp_face = mp.solutions.face_mesh
    face_mesh = mp_face.FaceMesh(static_image_mode=False)

    cont_attention = 0
    cont_distraction = 0
    second_number = 1
    start_time = time.time()

    while time.time() - start_time < duration * 60:
        if st.session_state.stop_monitor:
            st.warning("Monitoring stopped!")
            break

        ret, frame = cap.read()
        if not ret:
            continue

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)
        face_present = "Yes" if results.multi_face_landmarks else "No"

        # Update attention/distraction
        if face_present == "Yes":
            cont_attention += 1
            cont_distraction = 0
        else:
            cont_distraction += 1
            cont_attention = 0

        # Engagement/confusion
        if cont_attention >= 20:
            engagement = "High"
            confusion = "Low"
            alert_text = "🟢 High Attention"
        elif cont_distraction >= 10:
            engagement = "Low"
            confusion = "High"
            alert_text = "🔴 Low Attention"
        else:
            engagement = "Medium"
            confusion = "Medium"
            alert_text = "🟡 Medium Attention"

        # Save metrics to CSV
        row = {
            "Second": second_number,
            "Face_Present": face_present,
            "Continuous_Attention": cont_attention,
            "Continuous_Distraction": cont_distraction,
            "Engagement": engagement,
            "Confusion": confusion
        }
        if not os.path.exists(METRICS_CSV):
            pd.DataFrame([row]).to_csv(METRICS_CSV, index=False)
        else:
            pd.DataFrame([row]).to_csv(METRICS_CSV, mode='a', header=False, index=False)

        # Update dashboard
        df = pd.read_csv(METRICS_CSV)
        chart_placeholder.line_chart(df[["Continuous_Attention","Continuous_Distraction"]])
        table_placeholder.table(df.tail(5))
        alert_placeholder.markdown(f"### Alert: {alert_text}")

        second_number += 1
        time.sleep(1)

    cap.release()
    st.success("Monitoring finished!")
