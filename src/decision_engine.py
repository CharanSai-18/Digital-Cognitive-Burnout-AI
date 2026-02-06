import pandas as pd
import os

input_file = "data/processed/daily_scores.csv"
output_file = "data/processed/daily_recommendations.csv"

df = pd.read_csv(input_file)

notifications = []
messages = []

for _, row in df.iterrows():

    focus = row["focus_score"]
    breaks = row["break_score"]
    load = row["cognitive_load_score"]
    risk = row["burnout_risk"]

    notify = False
    message = "No notification needed."

    # --- DECISION LOGIC ---
    if risk == "HIGH":
        notify = True
        message = "High burnout risk detected. Take a longer break and reduce screen time."

    elif risk == "MEDIUM":
        notify = True
        message = "Moderate cognitive load. Consider a short walk or rest."

    elif focus < 30:
        notify = True
        message = "Low focus today. Try working in short focused sessions."

    # --- SAFETY CHECK ---
    if focus == 0 and breaks == 0:
        notify = False
        message = "Insufficient data to generate insights."

    notifications.append("YES" if notify else "NO")
    messages.append(message)

df["notify_user"] = notifications
df["recommendation"] = messages

os.makedirs("data/processed", exist_ok=True)
df.to_csv(output_file, index=False)

print("Day 7 decision engine complete.")
print("Saved to:", output_file)
