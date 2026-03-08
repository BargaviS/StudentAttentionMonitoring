import pandas as pd
from datetime import datetime
import os

OUTPUT_CSV = "../data/real_time_student_metrics.csv"

def analyze_student(processed_csv):
    
    df = pd.read_csv(processed_csv)
    df_metrics = []

    continuous_attention = 0
    continuous_distraction = 0

    for _, row in df.iterrows():
        face = row["Face_Present"]

        if face == "Yes":
            continuous_attention += 1
            continuous_distraction = 0
        else:
            continuous_distraction += 1
            continuous_attention = 0

        if continuous_attention >= 20:
            engagement_level = "High"
            confusion_level = "Low"
        elif continuous_distraction >= 10:
            engagement_level = "Low"
            confusion_level = "High"
        else:
            engagement_level = "Medium"
            confusion_level = "Medium"

        df_metrics.append({
            "Student_ID": row["Student_ID"],
            "Minute": row["Minute"],
            "Face_Present": face,
            "Continuous_Attention": continuous_attention,
            "Continuous_Distraction": continuous_distraction,
            "Engagement_Level": engagement_level,
            "Confusion_Level": confusion_level,
            "Timestamp": datetime.now()
        })

    os.makedirs(os.path.dirname(OUTPUT_CSV), exist_ok=True)
    if not os.path.exists(OUTPUT_CSV):
        pd.DataFrame(df_metrics).to_csv(OUTPUT_CSV, index=False)
    else:
        pd.DataFrame(df_metrics).to_csv(OUTPUT_CSV, mode='a', header=False, index=False)

    print(f"[INFO] Metrics updated: {OUTPUT_CSV}")
    return OUTPUT_CSV

if __name__ == "__main__":
    sample_processed = "../data/processed/S1_processed_sample.csv"
    analyze_student(sample_processed)
