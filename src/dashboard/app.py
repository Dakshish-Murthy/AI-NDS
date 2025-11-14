"""
app.py – Streamlit Dashboard for AI-NDS
--------------------------------------------------------
Phase 5: Integration & Visualization

Professional Real-Time Intrusion Detection Dashboard
--------------------------------------------------------
Now includes:
  🔴 Animated intrusion alert bar
  🔔 Beep notification
  ✅ Dismissible alerts
  🕓 Persistent alert history log
  ✨ Dark modern UI with live metrics
--------------------------------------------------------
"""

import streamlit as st
import pandas as pd
import time
import os
from datetime import datetime
import plotly.express as px
import streamlit.components.v1 as components

# =====================================================
# ⚙️ CONFIGURATION
# =====================================================
st.set_page_config(
    page_title="AI-NDS Dashboard",
    page_icon="🧠",
    layout="wide"
)

LOG_FILE = "data/realtime_log.csv"
REFRESH_INTERVAL = 5  # seconds

# =====================================================
# SESSION STATE for Alert Tracking
# =====================================================
if "alert_history" not in st.session_state:
    st.session_state.alert_history = []
if "alert_dismissed" not in st.session_state:
    st.session_state.alert_dismissed = False
if "last_intrusion_count" not in st.session_state:
    st.session_state.last_intrusion_count = 0

# =====================================================
# 🎨 STYLING + ANIMATIONS
# =====================================================
st.markdown(
    """
    <style>
    .main {
        background-color:#0e1117;
        color:white;
        font-family:'Inter',sans-serif;
    }
    h1,h2,h3,h4,h5,h6,p,div,span{color:#f5f6fa!important;}

    /* LIVE pulsing dot */
    .live-dot {
        height: 12px;width: 12px;
        background-color: #22d3ee;
        border-radius: 50%;
        display: inline-block;
        margin-right: 8px;
        box-shadow: 0 0 0 rgba(34,211,238,0.6);
        animation: pulse 1.5s infinite;
    }
    @keyframes pulse {
        0% { box-shadow: 0 0 0 0 rgba(34,211,238,0.7); }
        70% { box-shadow: 0 0 0 10px rgba(34,211,238,0); }
        100% { box-shadow: 0 0 0 0 rgba(34,211,238,0); }
    }

    /* Metric card */
    .metric-card {
        background:linear-gradient(135deg,rgba(46,60,89,0.45),rgba(22,30,50,0.6));
        padding:1em;border-radius:12px;
        box-shadow:0 0 20px rgba(0,0,0,0.3);
        border:1px solid rgba(80,120,200,0.3);
        transition:all .25s ease-in-out;
    }
    .metric-card:hover {
        transform:scale(1.03);
        box-shadow:0 0 25px rgba(34,211,238,0.25);
    }
    [data-testid="stMetricValue"] {
        font-size:26px;font-weight:600;color:#22d3ee;
    }

    hr{margin-top:.8em;margin-bottom:.8em;border-color:#2e7cff;}
    .big-font{font-size:22px!important;color:#2e7cff;text-align:right;}
    .success-box{
        border-left:5px solid #16a34a;
        background-color:rgba(22,163,74,.08);
        padding:.8em;border-radius:6px;
        margin-top:10px;font-weight:500;
    }

    /* Intrusion alert bar */
    .intrusion-alert{
        border-radius:8px;padding:12px 16px;
        background:linear-gradient(90deg,rgba(239,83,80,0.95),rgba(183,28,28,0.95));
        color:white;font-weight:700;
        display:flex;align-items:center;gap:12px;
        box-shadow:0 8px 24px rgba(239,83,80,0.15);
        animation:blink 1s infinite;
        justify-content:space-between;
    }
    @keyframes blink{
        0%{opacity:1;}50%{opacity:.85;}100%{opacity:1;}
    }
    .intrusion-icon{
        display:inline-flex;align-items:center;justify-content:center;
        width:28px;height:28px;border-radius:50%;
        background:rgba(255,255,255,0.16);font-size:16px;
    }
    .dismiss-btn{
        background-color:rgba(255,255,255,0.2);
        border:none;border-radius:6px;
        padding:4px 10px;color:white;cursor:pointer;
    }
    .dismiss-btn:hover{
        background-color:rgba(255,255,255,0.3);
    }
    </style>
    """,
    unsafe_allow_html=True
)

# =====================================================
# 🧩 LOAD DATA
# =====================================================
@st.cache_data(ttl=5)
def load_data():
    if os.path.exists(LOG_FILE) and os.path.getsize(LOG_FILE) > 0:
        df = pd.read_csv(LOG_FILE)
        df["Timestamp"] = pd.to_datetime(df["Timestamp"], errors="coerce")
        return df.dropna(subset=["Timestamp"])
    else:
        return pd.DataFrame(columns=["Timestamp", "Src IP", "Dst IP", "Protocol", "Packet Length", "Prediction"])

# =====================================================
# 🏷️ HEADER
# =====================================================
st.markdown(
    """
    <h1 style="display:flex;align-items:center;">
        <span class="live-dot"></span>
        AI-NDS: Real-Time Network Intrusion Detection System
    </h1>
    """,
    unsafe_allow_html=True
)
st.caption("AI-driven live traffic analysis and anomaly visualization dashboard")

placeholder = st.empty()

# =====================================================
# 🔄 DASHBOARD LOOP
# =====================================================
while True:
    with placeholder.container():
        df = load_data()

        if df.empty:
            st.warning("⚠️ No live data detected. Please run the real-time monitor first.")
            time.sleep(REFRESH_INTERVAL)
            continue

        preds = df["Prediction"].astype(str)
        total_packets = len(df)
        normal_packets = preds.str.contains("Normal", na=False).sum()
        intrusion_packets = preds.str.contains("Intrusion|Attack|Anomaly|1", na=False).sum()
        last_updated = df["Timestamp"].max()

        col1, col2, col3, col4 = st.columns(4)
        for col, label, val in zip(
            [col1, col2, col3, col4],
            ["📦 Total Packets", "✅ Normal", "🚨 Intrusions", "🕒 Last Update"],
            [total_packets, normal_packets, intrusion_packets, last_updated.strftime('%H:%M:%S') if pd.notnull(last_updated) else "-"]
        ):
            with col:
                st.markdown("<div class='metric-card'>", unsafe_allow_html=True)
                st.metric(label, f"{val}")
                st.markdown("</div>", unsafe_allow_html=True)

        st.markdown("---")

        # -------------------------------------------------
        # 🔴 ALERT BAR + SOUND + DISMISS
        # -------------------------------------------------
        if intrusion_packets > 0 and not st.session_state.alert_dismissed:
            if intrusion_packets != st.session_state.last_intrusion_count:
                st.session_state.alert_history.append(
                    {"time": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
                     "count": intrusion_packets}
                )
                st.session_state.last_intrusion_count = intrusion_packets

            alert_html = f"""
            <div class="intrusion-alert">
                <div style="display:flex;align-items:center;gap:10px;">
                    <div class="intrusion-icon">⚠️</div>
                    <div>Intrusion Detected — <strong>{intrusion_packets}</strong> suspicious flow(s)</div>
                </div>
                <button class="dismiss-btn" onclick="window.parent.postMessage('dismiss','*')">Dismiss</button>
            </div>
            <script>
            (function(){{
                try {{
                    if(!window.__ai_alert_played){{
                        var AudioContext=window.AudioContext||window.webkitAudioContext;
                        var ctx=new AudioContext();
                        function beep(f,d,v){{
                            var o=ctx.createOscillator();
                            var g=ctx.createGain();
                            o.type="sine";o.frequency.value=f;g.gain.value=v||0.06;
                            o.connect(g);g.connect(ctx.destination);
                            o.start();setTimeout(()=>o.stop(),d);
                        }}
                        beep(880,200,0.07);setTimeout(()=>beep(660,200,0.07),300);
                        window.__ai_alert_played=true;
                    }}
                }}catch(e){{console.log(e);}}
            }})();
            </script>
            """
            components.html(alert_html, height=70)

            # Listen for dismiss signal (JavaScript → Streamlit)
            msg = st.experimental_get_query_params().get("dismiss")
            if msg:
                st.session_state.alert_dismissed = True
        elif st.session_state.alert_dismissed:
            st.success("✅ Alert dismissed — monitoring continues silently.")

        # -------------------------------------------------
        # 📈 VISUALS
        # -------------------------------------------------
        left, right = st.columns([1.2, 2])
        with left:
            st.subheader("📊 Traffic Distribution")
            pie_fig = px.pie(
                names=["Normal", "Intrusion"],
                values=[normal_packets, intrusion_packets],
                color=["Normal", "Intrusion"],
                color_discrete_map={"Normal": "#16a34a", "Intrusion": "#dc2626"},
                hole=0.45,
            )
            st.plotly_chart(pie_fig, use_container_width=True)
        with right:
            st.subheader("📈 Traffic Trend Over Time")
            df["minute"] = df["Timestamp"].dt.strftime("%H:%M")
            trend_df = df.groupby(["minute", "Prediction"]).size().reset_index(name="Count")
            trend_fig = px.line(
                trend_df,
                x="minute", y="Count", color="Prediction",
                color_discrete_map={"✅ Normal": "#16a34a", "⚠️ Intrusion": "#dc2626"},
                markers=True, template="plotly_dark"
            )
            st.plotly_chart(trend_fig, use_container_width=True)

        st.markdown("---")

        # -------------------------------------------------
        # 🧾 RECENT NETWORK LOGS
        # -------------------------------------------------
        st.subheader("📜 Recent Network Activity")
        st.dataframe(
            df.sort_values(by="Timestamp", ascending=False).head(25),
            use_container_width=True, hide_index=True
        )

        if intrusion_packets == 0:
            st.markdown("<div class='success-box'>✅ No intrusions detected in recent traffic.</div>", unsafe_allow_html=True)

        # -------------------------------------------------
        # 🕓 ALERT HISTORY LOG
        # -------------------------------------------------
        if st.session_state.alert_history:
            st.markdown("### 🧾 Intrusion Alert History")
            hist_df = pd.DataFrame(st.session_state.alert_history)
            st.table(hist_df)

        st.markdown(f"<p class='big-font'>🔄 Auto-refreshing every {REFRESH_INTERVAL} seconds...</p>", unsafe_allow_html=True)
        time.sleep(REFRESH_INTERVAL)
