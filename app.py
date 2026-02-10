import streamlit as st
import pandas as pd
import os
import matplotlib.pyplot as plt

# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------
st.set_page_config(page_title="AI Focus & Burnout", layout="wide")

# ------------------------------------------------
# SIMPLE MOBILE LOGIN (SIMULATION)
# ------------------------------------------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

def login_page():
    st.title("📱 Login")
    mobile = st.text_input("Enter Mobile Number")
    otp = st.text_input("Enter OTP")

    if st.button("Login"):
        if mobile and otp:
            st.session_state.logged_in = True
            st.success("Login Successful ✅")
            st.rerun()
        else:
            st.error("Enter details")

if not st.session_state.logged_in:
    login_page()
    st.stop()

# ------------------------------------------------
# LOAD DATA
# ------------------------------------------------
DATA_PATH = "data/processed/daily_scores.csv"

if not os.path.exists(DATA_PATH):
    st.error("Run scoring engine first.")
    st.stop()

df = pd.read_csv(DATA_PATH)
latest = df.iloc[-1]

# ------------------------------------------------
# HEADER
# ------------------------------------------------
st.title("🧠 AI Focus & Burnout Detection System")
st.caption("Passive monitoring • Daily insights • Burnout prevention")

# ------------------------------------------------
# SIDEBAR NAVIGATION
# ------------------------------------------------
st.sidebar.title("📌 Navigation")
page = st.sidebar.radio("Go to", [
    "🏠 Home",
    "📊 Analytics",
    "📈 Progress",
    "⭐ Pro",
    "⚙ Settings"
])

# ------------------------------------------------
# COLOR FUNCTION
# ------------------------------------------------
def risk_color(risk):
    if risk == "LOW":
        return "green"
    elif risk == "MEDIUM":
        return "orange"
    else:
        return "red"

# ------------------------------------------------
# HOME PAGE
# ------------------------------------------------
if page == "🏠 Home":
    st.header("📌 Today's Summary")

    c1, c2, c3 = st.columns(3)

    with c1:
        st.markdown(f"### Burnout Risk")
        st.markdown(f"<h1 style='color:{risk_color(latest['burnout_risk'])}'>{latest['burnout_risk']}</h1>", unsafe_allow_html=True)

    with c2:
        st.metric("Cognitive Load", round(latest["cognitive_load_score"], 1))

    with c3:
        st.metric("Focus Score", round(latest["focus_score"], 1))

    st.divider()

    # Activity
    st.header("📊 Activity Overview")

    a1, a2, a3 = st.columns(3)
    a1.metric("Active Minutes", latest["active_minutes"])
    a2.metric("Idle Minutes", latest["idle_minutes"])
    a3.metric("Unique Apps Used", latest["unique_apps_used"])

    st.divider()

    # Screen
    st.header("💻 Screen Usage")
    s1, s2 = st.columns(2)
    s1.metric("Screen ON", latest["ON"])
    s2.metric("Screen OFF", latest["OFF"])

    st.divider()

    # AI Recommendation
    st.header("💡 AI Recommendation")

    if latest["burnout_risk"] == "LOW":
        st.success("Great balance. Keep it up.")
    elif latest["burnout_risk"] == "MEDIUM":
        st.warning("Moderate burnout risk. Take short breaks.")
    else:
        st.error("High burnout risk. Rest immediately.")

# ------------------------------------------------
# ANALYTICS PAGE
# ------------------------------------------------
elif page == "📊 Analytics":
    st.header("📊 Workload Analytics")

    fig, ax = plt.subplots()
    ax.plot(df["cognitive_load_score"])
    ax.set_title("Cognitive Load Trend")
    st.pyplot(fig)

    fig, ax = plt.subplots()
    ax.plot(df["focus_score"])
    ax.set_title("Focus Trend")
    st.pyplot(fig)

# ------------------------------------------------
# PROGRESS PAGE
# ------------------------------------------------
elif page == "📈 Progress":
    st.header("📈 Your Improvement Over Time")

    avg_focus = df["focus_score"].mean()
    avg_load = df["cognitive_load_score"].mean()

    st.metric("Average Focus", round(avg_focus, 1))
    st.metric("Average Cognitive Load", round(avg_load, 1))

# ------------------------------------------------
# PRO FEATURES PAGE
# ------------------------------------------------
elif page == "⭐ Pro":
    st.header("⭐ Premium Features")

    st.info("📊 Advanced dashboards")
    st.info("⏳ Smart focus timer")
    st.info("🧠 Personalized AI coach")

    st.warning("Upgrade coming soon 🚀")

# ------------------------------------------------
# SETTINGS PAGE
# ------------------------------------------------
elif page == "⚙ Settings":
    st.header("⚙ Settings")

    if st.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

# ------------------------------------------------
# FOOTER
# ------------------------------------------------
st.divider()
st.success("🏆 AI Focus & Burnout System Running Successfully")
