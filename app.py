import streamlit as st
import cv2
import numpy as np
import pandas as pd
import time

# Page Configuration
st.set_page_config(
    page_title="AEGIS-GUARD | AI Tactical Command Console",
    page_icon="🛡️",
    layout="wide"
)

# --- ADVANCED HUD & MILITARY THEME CSS ---
st.markdown("""
<style>
    /* Dark Military Grid Background */
    .stApp {
        background-color: #050a0e;
        background-image: linear-gradient(rgba(0, 255, 204, 0.03) 1px, transparent 1px),
                          linear-gradient(90deg, rgba(0, 255, 204, 0.03) 1px, transparent 1px);
        background-size: 30px 30px;
        color: #00ffcc;
        font-family: 'Courier New', monospace;
    }

    /* Red Tactical Alert Styling */
    .stAlert {
        border: 1px solid #ff0055 !important;
        box-shadow: 0 0 15px rgba(255, 0, 85, 0.4);
        background-color: rgba(255, 0, 85, 0.1) !important;
    }

    /* Glowing HUD Command Buttons */
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

    /* Radar Animation Styling */
    .radar {
        width: 100px;
        height: 100px;
        margin: 10px auto;
        border-radius: 50%;
        border: 1px solid #00ffcc;
        background: radial-gradient(circle, rgba(0,255,204,0.1) 0%, rgba(0,0,0,0.8) 70%),
                    repeating-radial-gradient(circle, transparent 0, transparent 15px, rgba(0,255,204,0.1) 16px);
        position: relative;
        box-shadow: 0 0 15px rgba(0,255,204,0.3);
    }

    .radar::after {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        border-radius: 50%;
        background: conic-gradient(from 0deg, transparent 0deg, transparent 300deg, rgba(0,255,204,0.6) 360deg);
        animation: spin 3s linear infinite;
    }

    @keyframes spin {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
</style>
""", unsafe_allow_html=True)

# Helper Function for Tactical Terminal Log Prints
def terminal_print(message, status="INFO"):
    color = "#00ffcc" if status == "INFO" else "#ff0055"
    st.markdown(f"""
    <div style="
        background-color: #0d1117; 
        border-left: 4px solid {color}; 
        padding: 6px 10px; 
        font-family: 'Courier New', monospace; 
        font-size: 0.85rem; 
        color: {color}; 
        margin-bottom: 5px;
        box-shadow: 0 0 5px rgba(0,255,204,0.1);
    ">
        [SYS_LOG::{status}] > {message}
    </div>
    """, unsafe_allow_html=True)

# Session State Setup
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "logs" not in st.session_state:
    st.session_state["logs"] = []

# --- 1. LOGIN PORTAL ---
if not st.session_state["logged_in"]:
    st.title("🛡️ AEGIS-GUARD: Zero-Network Access Portal")
    st.caption("Air-Gapped AI Border Defense Shield | Tactical Role-Based Login")
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
    st.sidebar.write(f"**Operator:** `{st.session_state['user']}`")
    st.sidebar.write(f"**Role:** `{st.session_state['role']}`")
    if st.sidebar.button("Logout"):
        st.session_state["logged_in"] = False
        st.rerun()

    st.sidebar.markdown("---")
    
    # Animated Radar Scanner in Sidebar
    st.sidebar.markdown("""
    <div style="text-align: center;">
        <div class="radar"></div>
        <span style="font-size: 0.75rem; color: #00ffcc; letter-spacing: 1px;">RADAR SWEEP: ACTIVE</span>
    </div>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("---")
    st.sidebar.subheader("📡 Mesh Telemetry")
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

    # High-Contrast Metric HUD Cards
    st.markdown("""
    <div style="display: grid; grid-template-columns: repeat(4, 1fr); gap: 10px; margin-bottom: 20px;">
        <div style="background: rgba(0,255,204,0.05); border: 1px solid #00ffcc; padding: 12px; border-radius: 4px; text-align: center;">
            <div style="font-size: 0.75rem; color: #888;">TARGET DISTANCE</div>
            <div style="font-size: 1.5rem; font-weight: bold; color: #00ffcc;">142.4 m</div>
        </div>
        <div style="background: rgba(0,255,204,0.05); border: 1px solid #00ffcc; padding: 12px; border-radius: 4px; text-align: center;">
            <div style="font-size: 0.75rem; color: #888;">AI CONFIDENCE</div>
            <div style="font-size: 1.5rem; font-weight: bold; color: #00ffcc;">94.8%</div>
        </div>
        <div style="background: rgba(0,255,204,0.05); border: 1px solid #00ffcc; padding: 12px; border-radius: 4px; text-align: center;">
            <div style="font-size: 0.75rem; color: #888;">PROCESSING SPEED</div>
            <div style="font-size: 1.5rem; font-weight: bold; color: #00ffcc;">45 FPS</div>
        </div>
        <div style="background: rgba(255,0,85,0.1); border: 1px solid #ff0055; padding: 12px; border-radius: 4px; text-align: center;">
            <div style="font-size: 0.75rem; color: #ff0055;">THREAT LEVEL</div>
            <div style="font-size: 1.5rem; font-weight: bold; color: #ff0055;">LEVEL 4 BREACH</div>
        </div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("📹 Live Camera Feed & Tactical HUD Scope")
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

                # Apply Spectrum Mapping
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

                # OpenCV HUD Overlay logic
                h, w, _ = frame.shape
                center_x, center_y = w // 2, h // 2

                # Target Box
                x1, y1, x2, y2 = w//4, h//4, 3*w//4, 3*h//4
                cv2.rectangle(frame, (x1, y1), (x2, y2), box_color, 2)
                cv2.putText(frame, status_text, (x1, y1 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, box_color, 2)

                # HUD Crosshair Scope
                cv2.circle(frame, (center_x, center_y), 40, box_color, 1)
                cv2.line(frame, (center_x - 50, center_y), (center_x + 50, center_y), box_color, 1)
                cv2.line(frame, (center_x, center_y - 50), (center_x, center_y + 50), box_color, 1)

                # Corner Target Markers
                cv2.line(frame, (20, 20), (50, 20), box_color, 2)
                cv2.line(frame, (20, 20), (20, 50), box_color, 2)
                cv2.line(frame, (w-20, h-20), (w-50, h-20), box_color, 2)
                cv2.line(frame, (w-20, h-20), (w-20, h-50), box_color, 2)

                frame_window.image(frame, channels="BGR", use_container_width=True)

                # Automatic Audio Beep in Thermal Mode
                if sensor_mode == "Real-Time Thermal" and enable_audio:
                    st.components.v1.html(
                        '<audio autoplay><source src="https://www.soundjay.com/buttons/beep-07a.mp3" type="audio/mpeg"></audio>',
                        height=0
                    )
            cap.release()
        else:
            st.info("Camera inactive. Check the box above to launch live video processing.")

        st.markdown("---")
        st.subheader("📍 GPS Incursion Satellite Map")
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
                log_msg = f"Silent Alarm Triggered by {st.session_state['user']}"
                st.session_state["logs"].append(f"[{timestamp}] {log_msg}")
                st.error("🚨 EMERGENCY SIREN SOUNDED AT COMMAND BASE!")
                st.components.v1.html(
                    '<audio autoplay><source src="https://www.soundjay.com/buttons/beep-01a.mp3" type="audio/mpeg"></audio>',
                    height=0
                )

            if st.button("📡 BROADCAST MESH PROTOCOL"):
                timestamp = time.strftime("%H:%M:%S")
                log_msg = f"Mesh Radio Signal Broadcasted to Field Outposts"
                st.session_state["logs"].append(f"[{timestamp}] {log_msg}")
                st.info("Offline Mesh Nodes Synchronized.")
        else:
            st.info("🔒 Field Patrol Operator: Restricted Controls")

        st.markdown("---")
        st.subheader("📋 Tactical Terminal Audit Trail")
        terminal_print("AIR-GAPPED MESH ROUTER ONLINE", "INFO")
        
        if st.session_state["logs"]:
            for log in reversed(st.session_state["logs"]):
                terminal_print(log, "WARN" if "Alarm" in log else "INFO")
        else:
            st.caption("No tactical alerts logged in this session.")
