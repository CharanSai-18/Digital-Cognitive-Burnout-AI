import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="AI Focus & Burnout Dashboard",
    layout="wide",
)

# ---------------- CSS ----------------
st.markdown("""
<style>
.card {
    padding: 18px;
    border-radius: 14px;
    background: #0b1220;
    color: white;
    text-align: center;
}
.card-title {
    font-size: 14px;
    color: #9ca3af;
}
.card-value {
    font-size: 26px;
    font-weight: 600;
}

.low { background: #064e3b; }
.medium { background: #78350f; }
.high { background: #7f1d1d; }

.section {
    margin-top: 30px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- LOAD DATA ----------------
df = pd.read_csv("data/processed/daily_scores.csv")
df["date"] = pd.to_datetime(df["date"])
latest = df.iloc[-1]

# ---------------- RISK COLOR ----------------
risk = latest["burnout_risk"]
risk_class = "low" if risk=="LOW" else "medium" if risk=="MEDIUM" else "high"

# ---------------- HEADER ----------------
st.markdown("""
### 🧠 AI Focus & Burnout Detection System  
*Passive monitoring · Cognitive insights · Burnout prevention*
""")

# ---------------- SUMMARY ----------------
st.markdown("<div class='section'></div>", unsafe_allow_html=True)
st.subheader("📌 Today’s Summary")

c1, c2, c3 = st.columns(3)

with c1:
    st.markdown(f"""
    <div class="card {risk_class}">
        <div class="card-title">Burnout Risk</div>
        <div class="card-value">{risk}</div>
    </div>
    """, unsafe_allow_html=True)

with c2:
    st.markdown(f"""
    <div class="card">
        <div class="card-title">Cognitive Load</div>
        <div class="card-value">{round(latest['cognitive_load_score'],1)}</div>
    </div>
    """, unsafe_allow_html=True)

with c3:
    st.markdown(f"""
    <div class="card">
        <div class="card-title">Focus Score</div>
        <div class="card-value">{round(latest['focus_score'],1)}</div>
    </div>
    """, unsafe_allow_html=True)

# ---------------- ACTIVITY ----------------
st.markdown("<div class='section'></div>", unsafe_allow_html=True)
st.subheader("📊 Activity Overview")

a1, a2, a3 = st.columns(3)

for col, title, key in [
    (a1, "Active Minutes", "active_minutes"),
    (a2, "Idle Minutes", "idle_minutes"),
    (a3, "Unique Apps Used", "unique_apps_used"),
]:
    with col:
        st.markdown(f"""
        <div class="card">
            <div class="card-title">{title}</div>
            <div class="card-value">{latest[key]}</div>
        </div>
        """, unsafe_allow_html=True)

# ---------------- SCREEN ----------------
st.markdown("<div class='section'></div>", unsafe_allow_html=True)
st.subheader("🖥 Screen Usage")

s1, s2 = st.columns(2)

with s1:
    st.markdown(f"""
    <div class="card">
        <div class="card-title">Screen ON (mins)</div>
        <div class="card-value">{latest['ON']}</div>
    </div>
    """, unsafe_allow_html=True)

with s2:
    st.markdown(f"""
    <div class="card">
        <div class="card-title">Screen OFF (mins)</div>
        <div class="card-value">{latest['screen_off_minutes']}</div>
    </div>
    """, unsafe_allow_html=True)

# ---------------- GRAPH ----------------
st.markdown("<div class='section'></div>", unsafe_allow_html=True)
st.subheader("📈 Focus vs Cognitive Load (7 Days)")

fig, ax = plt.subplots(figsize=(7,3))
ax.plot(df["date"], df["focus_score"], marker="o", label="Focus")
ax.plot(df["date"], df["cognitive_load_score"], marker="o", label="Cognitive Load")
ax.set_ylabel("Score")
ax.legend()
ax.grid(alpha=0.3)

st.pyplot(fig)

# ---------------- AI MESSAGE ----------------
st.markdown("<div class='section'></div>", unsafe_allow_html=True)
st.subheader("💡 AI Recommendation")

if risk == "LOW":
    st.success("Healthy focus pattern. Keep it up.")
elif risk == "MEDIUM":
    st.warning("Moderate strain detected. Consider short breaks.")
else:
    st.error("High burnout risk detected. Immediate rest advised.")

# ---------------- DATA ----------------
with st.expander("📅 Last 7 Days Data"):
    st.dataframe(df.tail(7), use_container_width=True)
