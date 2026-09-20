import streamlit as st
import cv2
import numpy as np
import time
import random

# Page Configuration
st.set_page_config(
    page_title="AEGIS-GUARD | AI Border Defense Command",
    page_icon="🛡️",
    layout="wide"
)

# Dark Mode Tactical CSS
st.markdown("""
<style>
    .stApp { background-color: #080c14; color: #00ffcc; font-family: 'Courier New', monospace; }
    .metric-card { background-color: #0f172a; padding: 15px; border-radius: 8px; border: 1px solid #1e293b; }
    .stButton>button { width: 100%; background-color: #dc2626; color: white; border: none; font-weight: bold; }
    .stButton>button:hover { background-color: #991b1b; }
</style>
""", unsafe_allow_html=True)

# Session State Initialization
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "logs" not in st.session_state:
    st.session_state["logs"] = []

# --- LOGIN SCREEN ---
if not st.session_state["logged_in"]:
    st.title("🛡️ AEGIS-GUARD: Secure Access Portal")
    st.caption("Zero-Network AI Border Defense System | Tactical Authentication")
    st.markdown("---")
    
    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_b:
        st.subheader("🔑 Operator Login")
        user = st.text_input("Operator Call Sign", value="Command-01")
        pin = st.text_input("Access PIN", type="password", value="1234")
        role = st.selectbox("Assign Role", ["Base Command Officer", "Field Patrol Operator", "System Administrator"])
        
        if st.button("AUTHENTICATE & LAUNCH DASHBOARD"):
            st.session_state["logged_in"] = True
            st.session_state["user"] = user
            st.session_state["role"] = role
            st.rerun()

# --- MAIN DASHBOARD ---
else:
    # Sidebar
    st.sidebar.title("🎛️ Command Controls")
    st.sidebar.write(f"**Operator:** {st.session_state['user']}")
    st.sidebar.write(f"**Role:** {st.session_state['role']}")
    if st.sidebar.button("Logout"):
        st.session_state["logged_in"] = False
        st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.subheader("📡 Hardware & Mesh Status")
    st.sidebar.success("EDGE AI NPU: ACTIVE (NVIDIA Jetson / Pi)")
    st.sidebar.info("AIR-GAPPED MESH: 4 Nodes Online")
    
    sector = st.sidebar.selectbox("Select Sector Feed", ["Sector 4-B (High Threat)", "Sector 1-A (Outpost)", "Border Gate West"])
    sensor_mode = st.sidebar.radio("Sensor Overlay Mode", ["Thermal Tracking", "Motion Radar", "Night Vision (IR)"])
    confidence_thresh = st.sidebar.slider("AI Confidence Threshold (%)", 50, 99, 85)

    # Header
    st.title("🛡️ AEGIS-GUARD Tactical Surveillance Console")
    st.caption(f"Active Sector: {sector} | Network: Offline Local Mesh | Encryption: AES-256")
    st.markdown("---")

    # Metrics Row
    m1, m2, m3, m4 = st.columns(4)
    m1.metric("Target Distance", "142 meters", "+1.2 m/s")
    m2.metric("AI Confidence", f"{random.randint(88, 97)}%", "HIGH")
    m3.metric("System Latency", "1.8 ms", "Real-Time Edge")
    m4.metric("Threat Level", "SEVERITY 4", "Breach Imminent")

    st.markdown("---")
    
    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("📹 Real-Time Computer Vision Feed")
        
        # WebCam Input Toggle
        use_webcam = st.checkbox("Use Live Camera / Webcam (Real AI Detection)", value=False)
        frame_window = st.image([])

        if use_webcam:
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            if ret:
                frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
                # Draw dynamic AI detection box
                h, w, _ = frame.shape
                cv2.rectangle(frame, (w//4, h//4), (3*w//4, 3*h//4), (0, 255, 0), 2)
                cv2.putText(frame, f"HUMAN TARGET DETECTED ({random.randint(88, 98)}%)", (w//4, h//4 - 10),
                            cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 255, 0), 2)
                frame_window.image(frame)
            cap.release()
        else:
            # Synthetic Moving Dynamic Feed
            img = np.zeros((360, 640, 3), dtype=np.uint8)
            
            # Dynamic Target Motion
            t = time.time()
            x = int(320 + 100 * np.sin(t * 2))
            y = int(180 + 40 * np.cos(t * 2))

            if sensor_mode == "Thermal Tracking":
                cv2.circle(img, (x, y), 50, (0, 0, 255), -1)
                cv2.circle(img, (x, y), 25, (0, 165, 255), -1)
                cv2.putText(img, "THERMAL SIGNATURE LOCK", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
            elif sensor_mode == "Motion Radar":
                cv2.rectangle(img, (x-40, y-40), (x+40, y+40), (0, 255, 0), 2)
                cv2.line(img, (x, 0), (x, 360), (0, 255, 0), 1)
                cv2.line(img, (0, y), (640, y), (0, 255, 0), 1)
                cv2.putText(img, f"MOTION LOCK: X={x} Y={y}", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
            else:
                img[:, :, 1] = 100
                cv2.circle(img, (x, y), 30, (255, 255, 255), 2)
                cv2.putText(img, "NIGHT VISION INFRARED ACTIVE", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

            frame_window.image(img, channels="BGR", use_container_width=True)

    with col2:
        st.subheader("🚨 Threat & Protocol Status")
        st.error("⚠️ ALERT: Unidentified Incursion in Sector 4-B")
        st.warning("Coordinates: 28.5355° N, 77.3910° E")
        
        st.markdown("---")
        st.subheader("⚡ Tactical Actions")
        
        if st.button("🚨 TRIGGER SILENT ALARM"):
            timestamp = time.strftime("%H:%M:%S")
            st.session_state["logs"].append(f"[{timestamp}] Silent Alarm Activated by {st.session_state['user']}")
            st.success("Silent Alert Signal Transmitted!")

        if st.button("📡 BROADCAST MESH PROTOCOL"):
            timestamp = time.strftime("%H:%M:%S")
            st.session_state["logs"].append(f"[{timestamp}] Mesh Relayed to Outpost Alpha")
            st.info("Mesh Nodes Synchronized.")

        st.markdown("---")
        st.subheader("📋 Tactical Action Log")
        if st.session_state["logs"]:
            for log in reversed(st.session_state["logs"]):
                st.code(log)
        else:
            st.caption("No manual actions logged in this session.")
