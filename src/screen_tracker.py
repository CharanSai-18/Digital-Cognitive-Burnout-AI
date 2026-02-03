import win32gui
import time
import csv
import os

LOG_INTERVAL = 10  # seconds

def is_screen_on():
    return win32gui.GetForegroundWindow() != 0

# Create data folder if not exists
os.makedirs("data/raw", exist_ok=True)
log_file = "data/raw/screen_log.csv"

# Create CSV file with header if not exists
if not os.path.exists(log_file):
    with open(log_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "screen_status"])

print("Screen tracker started. Press Ctrl+C to stop.")

while True:
    status = "ON" if is_screen_on() else "OFF"

    with open(log_file, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), status])

    time.sleep(LOG_INTERVAL)
