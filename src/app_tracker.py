import win32gui
import win32process
import psutil
import time
import csv
import os

LOG_INTERVAL = 5  # seconds

def get_active_app():
    try:
        hwnd = win32gui.GetForegroundWindow()
        _, pid = win32process.GetWindowThreadProcessId(hwnd)
        process = psutil.Process(pid)
        return process.name()
    except:
        return "Unknown"

os.makedirs("data/raw", exist_ok=True)
log_file = "data/raw/app_usage_log.csv"

if not os.path.exists(log_file):
    with open(log_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "app_name"])

print("App usage tracker started. Press Ctrl+C to stop.")

while True:
    app = get_active_app()

    with open(log_file, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), app])

    time.sleep(LOG_INTERVAL)
