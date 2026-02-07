import threading
from utils import log_info
from real_time_pipeline import start_real_time_monitoring, start_dashboard_thread

def main():
    # ------------------ Step 1: Ask for class duration ------------------
    while True:
        try:
            duration_minutes = int(input("Enter class duration in minutes: "))
            if duration_minutes <= 0:
                raise ValueError
            break
        except ValueError:
            print("Please enter a valid positive integer for minutes.")

    log_info(f"Starting real-time monitoring for {duration_minutes} minutes...")

    # ------------------ Step 2: Start Dashboard in a Separate Thread ------------------
    dashboard_thread = threading.Thread(target=start_dashboard_thread)
    dashboard_thread.daemon = True
    dashboard_thread.start()

    # ------------------ Step 3: Start Real-Time Monitoring ------------------
    # This function handles multi-student capture, per-frame processing,
    # alerting, and CSV logging
    start_real_time_monitoring(duration_minutes=duration_minutes)

    # ------------------ Step 4: Finish ------------------
    log_info("Class monitoring finished.")
    dashboard_thread.join()

if __name__ == "__main__":
    main()
