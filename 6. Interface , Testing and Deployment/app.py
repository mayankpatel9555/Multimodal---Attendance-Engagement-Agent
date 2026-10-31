import streamlit as st
import pandas as pd
import numpy as np
import plotly.express as px
from datetime import datetime

# --- PAGE LAYOUT & CONFIGURATION ---
st.set_page_config(
    page_title="EduSense AI - Multimodal Attendance & Engagement Agent",
    page_icon="🎓",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- SIDEBAR CONTROLS ---
st.sidebar.title("EduSense AI")
st.sidebar.caption("Classroom Intelligence System")

nav_option = st.sidebar.radio(
    "Navigation", 
    ["Live Classroom Monitor", "Teacher Central & Profile", "Session Analytics & Export"]
)

st.sidebar.divider()
st.sidebar.subheader("Detection Controls")
conf_threshold = st.sidebar.slider("Face Detection Confidence", 0.0, 1.0, 0.80, 0.05)
enable_audio = st.sidebar.checkbox("Enable Acoustic Telemetry", value=True)

# --- CACHED TELEMETRY GENERATOR ---
@st.cache_data
def load_session_telemetry():
    timestamps = pd.date_range(start="2026-10-31 08:47:56", periods=20, freq='5s')
    # Attention curve replicating slight dips and recoveries
    attention = [85, 84, 85, 78, 82, 50, 80, 78, 25, 80, 85, 90, 30, 80, 88, 86, 85, 85, 92, 90]
    emotions = ["engaged", "engaged", "neutral", "engaged", "distracted", 
                "engaged", "engaged", "engaged", "distracted", "neutral", 
                "engaged", "engaged", "neutral", "distracted", "engaged", 
                "engaged", "engaged", "engaged", "engaged", "engaged"]
    
    return pd.DataFrame({
        "Timestamp": timestamps.strftime('%H:%M:%S'),
        "avg_attention": attention,
        "Emotion": emotions,
        "Audio_dB": np.random.uniform(-46.0, -42.0, size=20).round(1)
    })

telemetry_data = load_session_telemetry()

# ==========================================
# VIEW 1: LIVE CLASSROOM MONITOR
# ==========================================
if nav_option == "Live Classroom Monitor":
    st.title("🎯 Live Attendance & Engagement Monitor")
    
    # Status Banner
    st.success("🟢 SUCCESS: Engagement is optimal. Keep going!")

    # Top Metric KPI Row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        st.metric(label="Students Present", value="2", delta="Session Active")
    with col2:
        st.metric(label="Average Attention", value="87.5%", delta="+12% 30-day trend")
    with col3:
        st.metric(label="Noise Level", value="-44.0 dB", delta="normal discussion")
    with col4:
        st.metric(label="Active IDs", value="ID: 1, ID: 3", delta="All Engaged")

    st.divider()

    # Feed Layout and AI Insights
    left_feed, right_side = st.columns([2, 1])

    with left_feed:
        st.subheader("Webcam Input Stream")
        # Streamlit native webcam widget for live validation
        camera_frame = st.camera_input("Live Camera Feed")
        if camera_frame is not None:
            st.info("Input frame successfully captured and fed into vision pipeline.")

    with right_side:
        st.subheader("💡 AI Suggestion Box")
        st.error("**High Priority** (02m ago)\n\nChallenge students with a harder problem.\n\n*Impact: Deep Learning*")
        
        st.subheader("🏆 Live Leaderboard")
        leaderboard_df = pd.DataFrame({
            "Student": ["Student 1", "Student 3"],
            "Score": ["36 pts", "2 pts"]
        })
        st.dataframe(leaderboard_df, use_container_width=True, hide_index=True)

# ==========================================
# VIEW 2: TEACHER CENTRAL & PROFILE
# ==========================================
elif nav_option == "Teacher Central & Profile":
    st.title("👨‍🏫 Teacher Profile")
    st.caption("Effectiveness Dashboard & Insights")

    col_t1, col_t2, col_t3 = st.columns(3)
    with col_t1:
        st.metric(label="Teaching Effectiveness", value="87.5 / 100", delta="+12% 30-day trend")
    with col_t2:
        st.subheader("🌟 Strengths")
        st.write("• High engagement sessions (85%+)")
        st.write("• Emotion diversity management")
    with col_t3:
        st.subheader("📖 Recommendations")
        st.write("• Try interactive polls (boost +18%)")
        st.write("• Short video breaks (+25% re-engagement)")

    st.divider()
    st.subheader("Class History Comparison")
    hist_c1, hist_c2 = st.columns(2)
    with hist_c1:
        st.metric(label="CS101 (Yesterday)", value="78% Avg")
    with hist_c2:
        st.metric(label="Math Workshop", value="92% Avg")

# ==========================================
# VIEW 3: SESSION ANALYTICS & EXPORT
# ==========================================
elif nav_option == "Session Analytics & Export":
    st.title("📈 Session Analytics")
    st.caption("Deep dive into classroom engagement")

    # Action / Download Buttons
    btn_col1, btn_col2 = st.columns([1, 6])
    with btn_col1:
        csv_file = telemetry_data.to_csv(index=False).encode("utf-8")
        st.download_button(
            label="📥 CSV Data",
            data=csv_file,
            file_name="session_analytics_report.csv",
            mime="text/csv"
        )

    chart_left, chart_right = st.columns(2)

    with chart_left:
        st.subheader("Attention Trend")
        fig_line = px.line(
            telemetry_data, 
            x="Timestamp", 
            y="avg_attention", 
            markers=True, 
            title="Class Attention Trend Over Time"
        )
        fig_line.update_layout(yaxis_range=[0, 100], template="plotly_dark")
        st.plotly_chart(fig_line, use_container_width=True)

    with chart_right:
        st.subheader("Emotion Distribution Over Time")
        fig_bar = px.histogram(
            telemetry_data, 
            x="Timestamp", 
            color="Emotion", 
            title="Affective States (Engaged vs Distracted)"
        )
        fig_bar.update_layout(template="plotly_dark")
        st.plotly_chart(fig_bar, use_container_width=True)