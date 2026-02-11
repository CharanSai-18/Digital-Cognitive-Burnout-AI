import pandas as pd
from datetime import datetime
from pathlib import Path

# =====================================================
# PATHS
# =====================================================
RAW_PATH = Path("data/raw/activity_log.csv")
PROCESSED_PATH = Path("data/processed/daily_scores.csv")


# =====================================================
# HELPERS
# =====================================================
def ensure_files():
    """Create folders/files if not exist"""
    PROCESSED_PATH.parent.mkdir(parents=True, exist_ok=True)

    if not PROCESSED_PATH.exists():
        columns = [
            "mobile",
            "date",
            "ACTIVE",
            "active_minutes",
            "idle_minutes",
            "OFF",
            "ON",
            "screen_off_minutes",
            "unique_apps_used",
            "app_switches",
            "focus_score",
            "break_score",
            "cognitive_load_score",
            "burnout_risk",
        ]
        pd.DataFrame(columns=columns).to_csv(PROCESSED_PATH, index=False)


# =====================================================
# SCORING ENGINE
# =====================================================
def calculate_scores(df):
    """Very simple scoring logic (can upgrade later)"""

    active_minutes = df["active_minutes"].sum()
    idle_minutes = df["idle_minutes"].sum()
    on_count = df["ON"].sum()
    off_count = df["OFF"].sum()
    unique_apps = df["app"].nunique()
    switches = df["app"].ne(df["app"].shift()).sum()

    # Focus = more active + less switching
    focus_score = max(0, 100 - (switches * 2 + idle_minutes))

    # Break score = more idle + more off
    break_score = idle_minutes + off_count

    # Cognitive load = inverse of breaks
    cognitive_load = max(0, 100 - break_score)

    # Burnout risk
    if cognitive_load < 30:
        risk = "LOW"
    elif cognitive_load < 70:
        risk = "MEDIUM"
    else:
        risk = "HIGH"

    return {
        "ACTIVE": df["ACTIVE"].sum(),
        "active_minutes": active_minutes,
        "idle_minutes": idle_minutes,
        "OFF": off_count,
        "ON": on_count,
        "screen_off_minutes": df["screen_off_minutes"].sum(),
        "unique_apps_used": unique_apps,
        "app_switches": switches,
        "focus_score": focus_score,
        "break_score": break_score,
        "cognitive_load_score": cognitive_load,
        "burnout_risk": risk,
    }


# =====================================================
# MAIN FUNCTION
# =====================================================
def run_daily_aggregation(mobile):
    ensure_files()

    if not RAW_PATH.exists():
        print("No raw data found")
        return

    raw_df = pd.read_csv(RAW_PATH)

    if raw_df.empty:
        print("Raw file empty")
        return

    today = datetime.now().strftime("%Y-%m-%d")

    # calculate
    scores = calculate_scores(raw_df)

    new_row = {"mobile": mobile, "date": today, **scores}

    processed_df = pd.read_csv(PROCESSED_PATH)

    # Remove existing record of today for this mobile
    processed_df = processed_df[
        ~(
            (processed_df["mobile"].astype(str) == str(mobile))
            & (processed_df["date"] == today)
        )
    ]

    # Add new
    processed_df = pd.concat([processed_df, pd.DataFrame([new_row])])

    processed_df.to_csv(PROCESSED_PATH, index=False)

    print("Daily aggregation complete ✅")


# =====================================================
# RUN MANUALLY
# =====================================================
if __name__ == "__main__":
    mobile = input("Enter mobile number: ")
    run_daily_aggregation(mobile)
