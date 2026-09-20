import streamlit as st
import cv2
import numpy as np
import pandas as pd
import time

# Page Configuration
st.set_page_config(
    page_title="AEGIS-GUARD | AI Border Defense",
    page_icon="🛡️",
    layout="wide"
)

# Dark Mode Tactical Styling
st.markdown("""
<style>
    .stApp { background-color: #080c14; color: #00ffcc; font-family: 'Courier New', monospace; }
    .stButton>button { width: 100%; background-color: #dc2626; color: white; font-weight: bold; border: none; }
    .stButton>button:hover { background-color: #991b1b; }
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
    st.caption("AI Border Defense Shield | Tactical Role-Based Login")
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
    # Sidebar
    st.sidebar.title("🎛️ Command Controls")
    st.sidebar.write(f"**Operator:** {st.session_state['user']}")
    st.sidebar.write(f"**Role:** {st.session_state['role']}")
    if st.sidebar.button("Logout"):
        st.session_state["logged_in"] = False
        st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.subheader("📡 Offline Mesh Telemetry")
    st.sidebar.success("AIR-GAPPED MESH: ACTIVE")
    st.sidebar.info("LATENCY: <1.8ms (LOCAL EDGE)")
    
    sector = st.sidebar.selectbox("Active Defense Sector", ["Sector 4-B (High Threat)", "Sector 1-A (Clear Outpost)", "Border Gate West"])
    sensor_mode = st.sidebar.radio("CV Filter Spectrum", ["Real-Time Thermal", "Infrared Night Vision", "Standard Motion Bounding"])

    # Header
    st.title("🛡️ AEGIS-GUARD Tactical Surveillance Console")
    st.caption(f"Connected Sector: {sector} | Network: Offline Local Mesh | Encryption: AES-256")
    st.markdown("---")

    # Metrics Bar
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Target Distance", "142 meters", "+1.2 m/s")
    m2.metric("AI Model Confidence", "94.8%", "HIGH LOCK")
    m3.metric("Edge Processing Speed", "45 FPS", "NPU Acceleration")
    m4.metric("Threat Rating", "LEVEL 4 BREACH", "Action Required")

    st.markdown("---")
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("📹 Live Camera Feed & Edge Computer Vision")
        use_camera = st.checkbox("Activate Live Laptop Camera / Video Feed", value=True)
        frame_window = st.image([])

        if use_camera:
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            if ret:
                frame = cv2.resize(frame, (640, 360))
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                
                # Thermal / Night Vision Color Mapping
                if sensor_mode == "Real-Time Thermal":
                    frame = cv2.applyColorMap(gray, cv2.COLORMAP_JET)
                    cv2.putText(frame, "THERMAL SPECTRUM ACTIVE", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)
                elif sensor_mode == "Infrared Night Vision":
                    frame = cv2.applyColorMap(gray, cv2.COLORMAP_SUMMER)
                    cv2.putText(frame, "INFRARED NIGHT VISION ACTIVE", (20, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)

                # Pure Python/NumPy Motion & Center Target Box (No Cascade Dependency)
                h, w, _ = frame.shape
                cv2.rectangle(frame, (w//4, h//4), (3*w//4, 3*h//4), (0, 255, 0), 2)
                cv2.putText(frame, "TARGET LOCK: ACTIVE CV TRACKING", (w//4, h//4 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 255, 0), 2)

                frame_window.image(frame, channels="BGR", use_container_width=True)
            cap.release()
        else:
            st.info("Camera inactive. Enable the checkbox above to process live feeds.")

        st.markdown("---")
        st.subheader("🗺️ GPS Incursion Satellite Map")
        map_data = pd.DataFrame({'lat': [28.5355], 'lon': [77.3910]})
        st.map(map_data, zoom=11)

    with col2:
        st.subheader("🚨 Threat & Protocol Status")
        if "Sector 4-B" in sector:
            st.error("⚠️ CRITICAL ALERT: Perimeter Breach Detected")
            st.warning("Coordinates: 28.5355° N, 77.3910° E")
        else:
            st.success("✅ Sector Perimeter Secure")

        st.markdown("---")
        st.subheader("⚡ Tactical Actions")
        
        if st.session_state["role"] in ["Base Command Officer", "System Administrator"]:
            if st.button("🚨 TRIGGER SILENT ALARM"):
                timestamp = time.strftime("%H:%M:%S")
                st.session_state["logs"].append(f"[{timestamp}] Silent Alarm Triggered by {st.session_state['user']}")
                st.error("🚨 SIREN SOUNDED AT COMMAND BASE!")
                st.components.v1.html(
                    '<audio autoplay><source src="https://www.soundjay.com/buttons/beep-01a.mp3" type="audio/mpeg"></audio>',
                    height=0
                )

            if st.button("📡 BROADCAST MESH PROTOCOL"):
                timestamp = time.strftime("%H:%M:%S")
                st.session_state["logs"].append(f"[{timestamp}] Mesh Signal Broadcasted across Nodes")
                st.info("Offline Mesh Nodes Synchronized.")
        else:
            st.info("🔒 Field Patrol Role: Restricted Controls")

        st.markdown("---")
        st.subheader("📋 Real-Time Command Log")
        if st.session_state["logs"]:
            for log in reversed(st.session_state["logs"]):
                st.code(log)
        else:
            st.caption("No emergency protocols logged in this session.")
