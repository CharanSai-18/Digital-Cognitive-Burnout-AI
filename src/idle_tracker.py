from pynput import mouse, keyboard
import time
import csv
import os

IDLE_THRESHOLD = 60  # seconds
LOG_INTERVAL = 10    # seconds

last_activity_time = time.time()

def on_activity(*args):
    global last_activity_time
    last_activity_time = time.time()

# Start listeners
mouse.Listener(
    on_move=on_activity,
    on_click=on_activity,
    on_scroll=on_activity
).start()

keyboard.Listener(
    on_press=on_activity
).start()

# Ensure data directory exists
os.makedirs("data/raw", exist_ok=True)

log_file = "data/raw/activity_log.csv"

# Write header if file does not exist
if not os.path.exists(log_file):
    with open(log_file, "w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow(["timestamp", "status"])

print("Idle tracker started. Press Ctrl+C to stop.")

while True:
    current_time = time.time()
    status = "IDLE" if current_time - last_activity_time > IDLE_THRESHOLD else "ACTIVE"

    with open(log_file, "a", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([time.strftime("%Y-%m-%d %H:%M:%S"), status])

    time.sleep(LOG_INTERVAL)
