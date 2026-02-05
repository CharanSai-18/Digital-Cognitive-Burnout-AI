import pandas as pd
import os

# Paths
activity_file = "data/raw/activity_log.csv"
screen_file = "data/raw/screen_log.csv"
app_file = "data/raw/app_usage_log.csv"
output_file = "data/processed/daily_summary.csv"

os.makedirs("data/processed", exist_ok=True)

# Load data
activity = pd.read_csv(activity_file)
screen = pd.read_csv(screen_file)
apps = pd.read_csv(app_file)

# Convert timestamps
activity["timestamp"] = pd.to_datetime(activity["timestamp"])
screen["timestamp"] = pd.to_datetime(screen["timestamp"])
apps["timestamp"] = pd.to_datetime(apps["timestamp"])

# Add date column
activity["date"] = activity["timestamp"].dt.date
screen["date"] = screen["timestamp"].dt.date
apps["date"] = apps["timestamp"].dt.date

# ---- ACTIVITY FEATURES ----
activity_summary = activity.groupby("date")["status"].value_counts().unstack(fill_value=0)
activity_summary["active_minutes"] = activity_summary.get("ACTIVE", 0) * (10 / 60)
activity_summary["idle_minutes"] = activity_summary.get("IDLE", 0) * (10 / 60)

# ---- SCREEN FEATURES ----
screen_summary = screen.groupby("date")["screen_status"].value_counts().unstack(fill_value=0)
screen_summary["screen_off_minutes"] = screen_summary.get("OFF", 0) * (10 / 60)

# ---- APP FEATURES ----
app_summary = apps.groupby("date")["app_name"].nunique().to_frame("unique_apps_used")
apps["app_switch"] = apps["app_name"] != apps["app_name"].shift()
switch_summary = apps.groupby("date")["app_switch"].sum().to_frame("app_switches")

# ---- MERGE ALL FEATURES ----
daily_summary = activity_summary.merge(
    screen_summary, on="date", how="outer"
).merge(
    app_summary, on="date", how="outer"
).merge(
    switch_summary, on="date", how="outer"
)

daily_summary = daily_summary.fillna(0)

# Save output
daily_summary.to_csv(output_file)

print("Day 5 aggregation complete.")
print("Saved to:", output_file)
