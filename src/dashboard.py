import pandas as pd
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from utils import log_info
import os

METRICS_CSV = "../data/real_time_student_metrics.csv"

# ------------------ Configurable options ------------------
SHOW_ATTENTION = True
SHOW_CONFUSION = True

def live_dashboard(refresh_sec=5):
    """
    Live dashboard reading CSV every refresh_sec seconds
    """
    if not os.path.exists(METRICS_CSV):
        log_info("Metrics CSV not found. Waiting for data...")
    
    fig, ax = plt.subplots()
    plt.ion()
    fig.suptitle("Real-Time Student Attention Dashboard")

    while True:
        if os.path.exists(METRICS_CSV):
            df = pd.read_csv(METRICS_CSV)

            ax.clear()
            students = df["Student_ID"].unique()
            for student in students:
                student_df = df[df["Student_ID"]==student]
                seconds = student_df["Second"]

                if SHOW_ATTENTION:
                    attention = student_df["Continuous_Attention"]
                    ax.plot(seconds, attention, label=f"{student} Attention", color='green')

                if SHOW_CONFUSION:
                    confusion = student_df["Continuous_Distraction"]
                    ax.plot(seconds, confusion, label=f"{student} Confusion", color='red')

                # Highlight alerts
                alert_indices = student_df[student_df["Continuous_Attention"]<seconds.max()*0.5].index
                for idx in alert_indices:
                    ax.axvline(x=student_df.loc[idx, "Second"], color='red', linestyle='--', alpha=0.3)

            ax.set_xlabel("Seconds")
            ax.set_ylabel("Metric Value")
            ax.legend(loc="upper right")
            ax.grid(True)
            plt.pause(refresh_sec)
        else:
            plt.pause(refresh_sec)

