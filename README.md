
# 👁️ Real-Time Student Attention Monitoring System

An AI-powered real-time system that analyzes student attention, engagement, and confusion using webcam input and computer vision. The system provides live insights through an interactive dashboard to help educators improve teaching effectiveness.

---

## 🚀 Overview

Traditional classrooms lack real-time feedback on student engagement. This project solves that problem by using computer vision to monitor attention continuously and present actionable insights via a live dashboard.

The system processes webcam frames in real time, predicts attention levels, and displays metrics instantly — without storing raw video.

---

## ✨ Key Features

- Real-time attention monitoring using webcam
- Live interactive dashboard built with Streamlit
- Per-second attention, engagement, and confusion prediction
- Color-coded alerts for easy understanding
- Minimal storage (CSV metrics only, no video saved)
- Start and stop monitoring anytime
- Lightweight and efficient real-time processing

---

## 🧠 How It Works

1. Captures live webcam frames
2. Detects face using computer vision
3. Analyzes attention indicators
4. Computes attention and engagement metrics
5. Displays live dashboard with real-time updates
6. Stores numeric metrics for analysis

---

## 📊 Dashboard Features

- Live attention score visualization
- Continuous attention tracking
- Confusion level monitoring
- Real-time alerts
- Metrics table with timestamps

---

## 📁 Project Structure

```
StudentAttentionMonitoring/
│
├── data/
│   └── real_time_student_metrics.csv
│
├── src/
│   ├── streamlit_app.py
│   ├── capture_analyze.py
│   ├── analyzer.py
│   ├── dashboard.py
│   ├── utils.py
│
├── requirements.txt
├── .gitignore
└── README.md
```

---

## ⚙️ Installation

### 1. Clone repository

```bash
git clone https://github.com/BargaviS/StudentAttentionMonitoring.git
cd StudentAttentionMonitoring
```

### 2. Create virtual environment

```bash
python -m venv venv
```

Activate environment:

Windows:
```bash
venv\Scripts\activate
```

Mac/Linux:
```bash
source venv/bin/activate
```

---

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

---

## ▶️ Run the Application

```bash
streamlit run src/streamlit_app.py
```

Then open browser:

```
http://localhost:8501
```

Click **Start Monitoring** to begin real-time analysis.

---

## 📈 Example Output

The system displays:

- Attention Level: High / Medium / Low
- Continuous Attention Duration
- Confusion Level
- Real-time attention graph
- Live metrics table

---

## 🎯 Applications

- Smart classrooms
- Online learning platforms
- Student engagement analysis
- Education research
- Training and learning environments

---

## 🔮 Future Improvements

- Multi-student monitoring
- Deep learning attention models
- Cloud deployment
- Teacher analytics reports
- Mobile support

---

## 🛠️ Technologies Used

- Python
- OpenCV
- Streamlit
- Pandas
- Computer Vision

---

## 👩‍💻 Author

Bargavi S  
Aspiring AI Engineer  

GitHub: https://github.com/BargaviS  
LinkedIn: https://linkedin.com/in/bargavis  

---

## ⭐ Acknowledgment

If you found this project useful, please consider giving it a star.

---

## 📄 License

This project is licensed under the MIT License.
