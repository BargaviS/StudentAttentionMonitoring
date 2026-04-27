import sys
import os
import streamlit as st
import cv2
import pandas as pd
import time
import altair as alt

# ---------------- FIX PATH ISSUE ----------------
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), "..")))

from core.face_tracker import FaceTracker
from core.attention_engine import AttentionEngine


# ---------------- UI SETUP ----------------
st.set_page_config(page_title="Student Attention Monitor", layout="wide")

st.title("🎯 Student Attention Monitoring System")
st.markdown("Real-time AI-based classroom monitoring")

# ---------------- INIT ----------------
tracker = FaceTracker()
engine = AttentionEngine(window_size=50)

if "run" not in st.session_state:
    st.session_state.run = False

col1, col2 = st.columns(2)

with col1:
    if st.button("▶ Start Monitoring"):
        st.session_state.run = True

with col2:
    if st.button("⛔ Stop Monitoring"):
        st.session_state.run = False


video_placeholder = st.empty()
graph_placeholder = st.empty()
stats_placeholder = st.empty()

cap = cv2.VideoCapture(0)
data = []


# ---------------- MAIN LOOP ----------------
while st.session_state.run:

    ret, frame = cap.read()
    if not ret:
        st.error("Camera not found")
        break

    # AI prediction
    score = tracker.get_attention_score(frame)

    # update engine
    engine.update(score)

    avg = engine.get_average()
    active, inactive = engine.get_active_inactive()

    data.append({"time": len(data), "attention": score})
    df = pd.DataFrame(data)

    # VIDEO
    frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    video_placeholder.image(frame, channels="RGB")

    # STATS
    stats_placeholder.metric("Average Attention", f"{avg:.2f}%")
    stats_placeholder.write(f"🟢 Active: {active}   🔴 Inactive: {inactive}")

    # GRAPH
    chart = alt.Chart(df).mark_line().encode(
        x="time",
        y="attention"
    ).properties(height=300)

    graph_placeholder.altair_chart(chart, use_container_width=True)

    time.sleep(0.03)

cap.release()