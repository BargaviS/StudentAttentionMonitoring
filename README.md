<<<<<<< HEAD
Real-Time Student Attention Monitoring System

A real-time AI-based system to monitor student attention, engagement, and confusion during lectures, with an interactive dashboard for teachers.

1️⃣ Problem

Teachers often cannot know if students are attentive or confused during lectures.
This leads to:

Disengagement

Poor learning outcomes

Ineffective teaching strategies

There is no simple, real-time method to measure student attention in classrooms, making timely intervention impossible.

2️⃣ Solution

This project provides a real-time monitoring system that:

Detects student faces, head orientation, and posture using webcam feeds.

Tracks attention, engagement, and confusion per second.

Displays a live interactive dashboard with charts and color-coded alerts.

Stores only minimal numeric metrics in a CSV file for later analysis.

3️⃣ Key Features

✅ Real-time attention prediction per second

✅ Interactive Streamlit dashboard for live visualization

✅ Color-coded alert system:

🟢 High Attention

🟡 Medium Attention

🔴 Low Attention

✅ Minimal storage: only numeric CSV, no raw videos

✅ Stop monitoring anytime via dashboard

✅ Demo-ready, easy for anyone to run

4️⃣ Folder Structure
StudentAttentionMonitoring/
│
├── data/                     # Metrics CSV only
│   └── real_time_student_metrics.csv
├── src/                      # Source code
│   ├── streamlit_app.py      # Interactive dashboard
│   ├── capture_analyze.py    # Webcam + attention logic
│   └── utils.py              # Helper functions
├── notebooks/                # Optional experiments / demo
│   └── demo.ipynb
├── requirements.txt          # Dependencies
├── .gitignore                # Ignore unnecessary files
└── README.md                 # Project documentation

5️⃣ Installation

Clone the repository:

git clone https://github.com/<username>/StudentAttentionMonitoring.git
cd StudentAttentionMonitoring
6️⃣ Usage

Run the Streamlit dashboard:

streamlit run src/streamlit_app.py


Enter class duration (minutes)

Click Start Monitoring → live dashboard appears

Metrics update every second, showing attention & confusion levels

Click Stop Monitoring anytime

Metrics are automatically saved in data/real_time_student_metrics.csv

7️⃣ Demo / Visualization

Live line chart: Continuous attention vs. distraction

Latest metrics table: Last 5 seconds summary

Alert card: Color-coded attention alert for teachers
8️⃣ Future Improvements

Multi-student monitoring on a single dashboard

Advanced head/eye gaze tracking

Analytics export for teachers (PDF / Excel)

Real-time audio/lecture content integration for deeper insights
=======
# StudentAttentionMonitoring
This project provides a real-time solution for monitoring student attention during lectures using webcam feeds.  It tracks attention, engagement, and confusion per second, displays live metrics on an interactive dashboard,  and stores minimal numeric data for analysis. Ideal for teachers to get actionable insights and improve learning outcomes.
>>>>>>> 3c311a0ce76cebe09408cde6e4830458db7087e3
