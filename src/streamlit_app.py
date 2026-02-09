import streamlit as st
import pandas as pd
import cv2
import mediapipe as mp
import time
import os
import altair as alt

st.set_page_config(page_title="Real-Time Student Attention", layout="wide")
st.title("📊 Real-Time Student Attention Monitoring System")

# ---------------- Session state ----------------
if "monitoring" not in st.session_state:
    st.session_state.monitoring = False
if "stop_monitor" not in st.session_state:
    st.session_state.stop_monitor = False
if "metrics" not in st.session_state:
    st.session_state.metrics = []

# CSV path
METRICS_CSV = "data/real_time_student_metrics.csv"
os.makedirs("data", exist_ok=True)

# ---------------- Start / Stop Buttons ----------------
duration = st.number_input("Class duration (minutes)", min_value=1, max_value=60, value=5)
col1, col2 = st.columns(2)
start_button = col1.button("Start Monitoring")
stop_button = col2.button("Stop Monitoring")

# ---------------- Monitoring Function ----------------
def run_monitoring(duration_minutes):
    cap = cv2.VideoCapture(0)
    mp_face = mp.solutions.face_mesh
    face_mesh = mp_face.FaceMesh(static_image_mode=False)

    cont_attention = 0
    cont_distraction = 0
    second_number = 1
    start_time = time.time()

    # Placeholders
    chart_placeholder = st.empty()
    table_placeholder = st.empty()
    alert_placeholder = st.empty()
    video_placeholder = st.empty()

    # To avoid repeating sound every second
    low_alert_played = False

    while time.time() - start_time < duration_minutes * 60:
        if st.session_state.stop_monitor:
            st.warning("Monitoring stopped!")
            break

        ret, frame = cap.read()
        if not ret:
            continue

        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        results = face_mesh.process(rgb_frame)
        face_present = "Yes" if results.multi_face_landmarks else "No"

        # Update attention/distraction counters
        if face_present == "Yes":
            cont_attention += 1
            cont_distraction = 0
            low_alert_played = False  # Reset low alert flag
        else:
            cont_distraction += 1
            cont_attention = 0

        # Determine engagement & alert
        if cont_attention >= 20:
            engagement = "High"
            confusion = "Low"
            alert_color = "green"
            alert_text = "🟢 High Attention"
        elif cont_distraction >= 10:
            engagement = "Low"
            confusion = "High"
            alert_color = "red"
            alert_text = "🔴 Low Attention"
        else:
            engagement = "Medium"
            confusion = "Medium"
            alert_color = "orange"
            alert_text = "🟡 Medium Attention"

        # Save metrics
        st.session_state.metrics.append({
            "Second": second_number,
            "Face_Present": face_present,
            "Continuous_Attention": cont_attention,
            "Continuous_Distraction": cont_distraction,
            "Engagement": engagement,
            "Confusion": confusion
        })

        # ---------------- Dashboard ----------------
        df = pd.DataFrame(st.session_state.metrics)

        # Altair colored line chart
        if len(df) > 1:
            df_melt = df.melt(id_vars="Second", value_vars=["Continuous_Attention", "Continuous_Distraction"])
            color_scale = alt.Scale(domain=["Continuous_Attention", "Continuous_Distraction"], range=["green", "red"])
            chart = alt.Chart(df_melt).mark_line(point=True).encode(
                x="Second",
                y="value",
                color=alt.Color("variable", scale=color_scale, legend=alt.Legend(title="Metric"))
            ).properties(height=300)
            chart_placeholder.altair_chart(chart, use_container_width=True)

        # Last 5 seconds table
        table_placeholder.table(df.tail(5))

        # Alert text
        alert_placeholder.markdown(
            f"<h2 style='color:{alert_color}'>{alert_text}</h2>",
            unsafe_allow_html=True
        )

        # ---------------- Sound alert for Low Attention ----------------
        if alert_text == "🔴 Low Attention" and not low_alert_played:
            audio_file = "alert_sound.mp3"  # Make sure this file exists
            if os.path.exists(audio_file):
                audio_bytes = open(audio_file, "rb").read()
                st.audio(audio_bytes, format="audio/mp3")
            low_alert_played = True

        # Live video
        video_placeholder.image(rgb_frame, channels="RGB", width=400)

        second_number += 1
        time.sleep(1)

    cap.release()
    pd.DataFrame(st.session_state.metrics).to_csv(METRICS_CSV, index=False)
    st.success("Monitoring finished!")

# ---------------- Handle Buttons ----------------
if start_button:
    st.session_state.monitoring = True
    st.session_state.stop_monitor = False
    st.session_state.metrics = []
    run_monitoring(duration)

if stop_button:
    st.session_state.stop_monitor = True

# ---------------- Download CSV ----------------
if os.path.exists(METRICS_CSV):
    st.download_button(
        label="📥 Download Metrics CSV",
        data=open(METRICS_CSV, "rb").read(),
        file_name="real_time_student_metrics.csv"
    )
