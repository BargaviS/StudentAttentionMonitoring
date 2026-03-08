import threading
from utils import log_info
from real_time_pipeline import start_real_time_monitoring, start_dashboard_thread

def main():
    while True:
        try:
            duration_minutes = int(input("Enter class duration in minutes: "))
            if duration_minutes <= 0:
                raise ValueError
            break
        except ValueError:
            print("Please enter a valid positive integer for minutes.")

    log_info(f"Starting real-time monitoring for {duration_minutes} minutes...")

    dashboard_thread = threading.Thread(target=start_dashboard_thread)
    dashboard_thread.daemon = True
    dashboard_thread.start()

    start_real_time_monitoring(duration_minutes=duration_minutes)

    log_info("Class monitoring finished.")
    dashboard_thread.join()

if __name__ == "__main__":
    main()
