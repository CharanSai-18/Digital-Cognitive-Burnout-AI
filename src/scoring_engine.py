import pandas as pd
import os

input_file = "data/processed/daily_summary.csv"
output_file = "data/processed/daily_scores.csv"

df = pd.read_csv(input_file)

# ---- SAFE NORMALIZATION HELPERS ----
def clamp(value, min_val=0, max_val=100):
    return max(min_val, min(value, max_val))

# ---- SCORE CALCULATIONS ----
focus_scores = []
break_scores = []
cognitive_load_scores = []
burnout_levels = []

for _, row in df.iterrows():

    # Focus Score
    focus = (
        row.get("active_minutes", 0) * 10
        - row.get("app_switches", 0) * 2
    )
    focus = clamp(focus)

    # Break Score
    breaks = (
        row.get("idle_minutes", 0) * 8
        + row.get("screen_off_minutes", 0) * 10
    )
    breaks = clamp(breaks)

    # Cognitive Load Score
    cognitive_load = (
        row.get("app_switches", 0) * 5
        + (100 - breaks) * 0.3
    )
    cognitive_load = clamp(cognitive_load)

    # Burnout Risk
    if cognitive_load > 70 and focus < 40:
        burnout = "HIGH"
    elif cognitive_load > 40:
        burnout = "MEDIUM"
    else:
        burnout = "LOW"

    focus_scores.append(focus)
    break_scores.append(breaks)
    cognitive_load_scores.append(cognitive_load)
    burnout_levels.append(burnout)

# ---- ADD TO DATAFRAME ----
df["focus_score"] = focus_scores
df["break_score"] = break_scores
df["cognitive_load_score"] = cognitive_load_scores
df["burnout_risk"] = burnout_levels

# ---- SAVE OUTPUT ----
df.to_csv(output_file, index=False)

print("Day 6 scoring complete.")
print("Saved to:", output_file)
