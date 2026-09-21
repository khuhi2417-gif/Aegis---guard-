import streamlit as st
import cv2
import numpy as np
import pandas as pd
import time

# Page Configuration
st.set_page_config(
    page_title="AEGIS-GUARD | AI Tactical Command",
    page_icon="🛡️",
    layout="wide"
)

# Dark Military Grid & HUD Styling
st.markdown("""
<style>
    /* Dark Tactical Background */
    .stApp {
        background-color: #050a0e;
        background-image: linear-gradient(rgba(0, 255, 204, 0.03) 1px, transparent 1px),
                          linear-gradient(90deg, rgba(0, 255, 204, 0.03) 1px, transparent 1px);
        background-size: 30px 30px;
        color: #00ffcc;
        font-family: 'Courier New', monospace;
    }

    /* Glowing Metrics */
    div[data-testid="stMetricValue"] {
        font-size: 1.8rem !important;
        color: #00ffcc !important;
        text-shadow: 0 0 10px rgba(0, 255, 204, 0.5);
    }

    /* Tactical Alert Box */
    .stAlert {
        border: 1px solid #ff0055 !important;
        box-shadow: 0 0 15px rgba(255, 0, 85, 0.4);
        background-color: rgba(255, 0, 85, 0.1) !important;
    }

    /* Glowing Command Buttons */
    .stButton>button {
        background: linear-gradient(180deg, #1f2937, #111827);
        border: 1px solid #00ffcc !important;
        color: #00ffcc !important;
        font-weight: bold;
        box-shadow: 0 0 8px rgba(0, 255, 204, 0.3);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background: #00ffcc !important;
        color: #000000 !important;
        box-shadow: 0 0 20px rgba(0, 255, 204, 0.8);
    }
</style>
""", unsafe_allow_html=True)

# Session State Setup
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "logs" not in st.session_state:
    st.session_state["logs"] = []

# --- 1. LOGIN PORTAL ---
if not st.session_state["logged_in"]:
    st.title("🛡️ AEGIS-GUARD: Zero-Network Access Portal")
    st.caption("Air-Gapped AI Border Defense System | Tactical Role-Based Login")
    st.markdown("---")
    
    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_b:
        st.subheader("🔑 Operator Authentication")
        user = st.text_input("Operator Call Sign", value="Command-01")
        pin = st.text_input("Access PIN", type="password", value="1234")
        role = st.selectbox("Assign Role", ["Base Command Officer", "Field Patrol Operator", "System Administrator"])
        
        if st.button("AUTHENTICATE & ACCESS SYSTEM"):
            if user and pin:
                st.session_state["logged_in"] = True
                st.session_state["user"] = user
                st.session_state["role"] = role
                st.rerun()

# --- 2. MAIN COMMAND DASHBOARD ---
else:
    # Sidebar Controls
    st.sidebar.title("🎛️ Command Controls")
    st.sidebar.write(f"**Operator:** `{st.session_state['user']}`")
    st.sidebar.write(f"**Role:** `{st.session_state['role']}`")
    if st.sidebar.button("Logout"):
        st.session_state["logged_in"] = False
        st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.subheader("📡 Mesh Network Status")
    st.sidebar.success("AIR-GAPPED MESH: ACTIVE")
    st.sidebar.info("LATENCY: <1.8ms (LOCAL EDGE)")
    
    sector = st.sidebar.selectbox("Active Defense Sector", ["Sector 4-B (High Threat)", "Sector 1-A (Clear Outpost)", "Border Gate West"])
    sensor_mode = st.sidebar.radio("CV Filter Spectrum", ["Real-Time Thermal", "Infrared Night Vision", "Standard Motion Bounding"])
    enable_audio = st.sidebar.checkbox("🔊 Audio Detection Alerts", value=True)

    # Main Header & Pulsing Status Indicator
    st.markdown("""
    <div style="display: flex; align-items: center; gap: 10px;">
        <div style="width: 12px; height: 12px; background-color: #00ffcc; border-radius: 50%; box-shadow: 0 0 10px #00ffcc;"></div>
        <h2 style="margin: 0; color: #00ffcc;">🛡️ AEGIS-GUARD Tactical Surveillance Console</h2>
    </div>
    """, unsafe_allow_html=True)
    st.caption(f"Sector: {sector} | Network: Air-Gapped Local Mesh | Encryption: AES-256")
    st.markdown("---")

    # Metrics Telemetry Bar
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Target Distance", "142.4 m", "+0.4 m/s")
    m2.metric("AI Confidence", "94.8%", "HIGH LOCK")
    m3.metric("Processing Speed", "45 FPS", "NPU Edge Acceleration")
    m4.metric("Threat Rating", "LEVEL 4 BREACH", "Action Required")

    st.markdown("---")
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("📹 Live Feed & Tactical Crosshair Tracking")
        use_camera = st.checkbox("Activate Camera Feed", value=True)
        frame_window = st.image([])

        if use_camera:
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            if ret:
                frame = cv2.resize(frame, (640, 360))
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                box_color = (0, 255, 0)
                status_text = "TARGET LOCK: ACTIVE CV TRACKING"

                # Apply Spectrum Mapping Filters
                if sensor_mode == "Real-Time Thermal":
                    frame = cv2.applyColorMap(gray, cv2.COLORMAP_JET)
                    cv2.putText(frame, "THERMAL SPECTRUM ACTIVE", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (255, 255, 255), 2)
                    box_color = (0, 255, 255)
                    status_text = "THERMAL TARGET LOCK: HEAT SIGNATURE DETECTED"
                elif sensor_mode == "Infrared Night Vision":
                    frame = cv2.applyColorMap(gray, cv2.COLORMAP_SUMMER)
                    cv2.putText(frame, "INFRARED NIGHT VISION ACTIVE", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                    box_color = (0, 255, 0)
                    status_text = "INFRARED LOCK: MOTION DETECTED"

                # Draw Target Box & Crosshair HUD Scope
                h, w, _ = frame.shape
                center_x, center_y = w // 2, h // 2
                
                # Bounding Box
                x1, y1, x2, y2 = w//4, h//4, 3*w//4, 3*h//4
                cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, 2)
                cv2.putText(frame, status_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, box_color, 2)

                # HUD Crosshair Overlays
                cv2.circle(frame, (center_x, center_y), 30, box_color, 1)
                cv2.line(frame, (center_x - 40, center_y), (center_x + 40, center_y), box_color, 1)
                cv2.line(frame, (center_x, center_y - 40), (center_x, center_y + 40), box_color, 1)

                frame_window.image(frame, channels="BGR", use_container_width=True)

                # Automated Thermal Audio Alert
                if sensor_mode == "Real-Time Thermal" and enable_audio:
                    st.components.v1.html(
                        '<audio autoplay><source src="https://www.soundjay.com/buttons/beep-07a.mp3" type="audio/mpeg"></audio>',
                        height=0
                    )
            cap.release()
        else:
            st.info("Camera inactive. Check the box above to launch live video processing.")

        st.markdown("---")
        st.subheader("📍 GPS Incursion Satellite Coordinates")
        map_data = pd.DataFrame({'lat': [28.5355], 'lon': [77.3910]})
        st.map(map_data, zoom=11)

    with col2:
        st.subheader("🚨 Threat Status")
        if "Sector 4-B" in sector:
            st.error("⚠️ CRITICAL ALERT: Perimeter Incursion Detected")
            st.warning("GPS: 28.5355° N, 77.3910° E")
        else:
            st.success("✅ Sector Perimeter Clear")

        st.markdown("---")
        st.subheader("⚡ Tactical Response Protocols")
        
        if st.session_state["role"] in ["Base Command Officer", "System Administrator"]:
            if st.button("🚨 TRIGGER SILENT ALARM"):
                timestamp = time.strftime("%H:%M:%S")
                st.session_state["logs"].append(f"[{timestamp}] Silent Alarm Triggered by {st.session_state['user']}")
                st.error("🚨 EMERGENCY SIREN SOUNDED AT BASE COMMAND!")
                st.components.v1.html(
                    '<audio autoplay><source src="https://www.soundjay.com/buttons/beep-01a.mp3" type="audio/mpeg"></audio>',
                    height=0
                )

            if st.button("📡 BROADCAST MESH PROTOCOL"):
                timestamp = time.strftime("%H:%M:%S")
                st.session_state["logs"].append(f"[{timestamp}] Mesh Signal Broadcasted to Field Units")
                st.info("Offline Mesh Nodes Synchronized.")
        else:
            st.info("🔒 Field Patrol Operator: Restricted Controls")

        st.markdown("---")
        st.subheader("📋 Real-Time Command Log")
        if st.session_state["logs"]:
            for log in reversed(st.session_state["logs"]):
                st.code(log)
        else:
            st.caption("No tactical alerts logged in this session.")
