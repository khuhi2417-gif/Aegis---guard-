import streamlit as st
import cv2
import numpy as np

st.set_page_config(
    page_title="AEGIS-GUARD | AI Border Defense",
    page_icon="🛡️",
    layout="wide"
)

st.markdown("""
<style>
    .stApp { background-color: #0b0f19; color: #ffffff; }
    .stButton>button { width: 100%; font-weight: bold; }
    .stTextInput>div>div>input { background-color: #1e293b; color: white; }
</style>
""", unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False
if "username" not in st.session_state:
    st.session_state["username"] = ""
if "role" not in st.session_state:
    st.session_state["role"] = ""

if not st.session_state["logged_in"]:
    st.title("🛡️ AEGIS-GUARD: Secure Access Portal")
    st.caption("Zero-Network AI Border Defense System | Tactical Authentication")
    st.markdown("---")
    
    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_b:
        st.subheader("🔑 Operator Login")
        user_input = st.text_input("Operator Call Sign / Username", value="Command-01")
        pass_input = st.text_input("Access PIN / Password", type="password", value="1234")
        role_input = st.selectbox("Assign Role", ["Base Command Officer", "Field Patrol Operator", "System Administrator"])
        
        if st.button("LOGIN TO TACTICAL DASHBOARD"):
            if user_input and pass_input:
                st.session_state["logged_in"] = True
                st.session_state["username"] = user_input
                st.session_state["role"] = role_input
                st.rerun()
            else:
                st.error("Please enter valid credentials.")

else:
    st.sidebar.title("🎛️ Command Center")
    st.sidebar.write(f"**Operator:** {st.session_state['username']}")
    st.sidebar.write(f"**Role:** {st.session_state['role']}")
    
    if st.sidebar.button("Logout"):
        st.session_state["logged_in"] = False
        st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.subheader("📡 Offline Mesh Telemetry")
    st.sidebar.success("AIR-GAPPED MESH: ACTIVE")
    st.sidebar.info("LATENCY: <2ms (LOCAL EDGE)")
    
    sector_select = st.sidebar.selectbox("Active Sector", ["Sector 4-B (High Threat)", "Sector 1-A (Clear)", "Border Gate West"])
    sensitivity = st.sidebar.slider("AI Motion Detection Threshold", 10, 100, 75)

    st.title("🛡️ AEGIS-GUARD Tactical Surveillance")
    st.caption(f"Connected Sector: {sector_select} | Offline AI Inference Engine")
    st.markdown("---")

    col1, col2 = st.columns([2, 1])

    with col1:
        st.subheader("📹 Real-Time Edge Surveillance Feed")
        feed_mode = st.radio("Sensor Mode:", ["Thermal Simulation", "Motion Detection Radar", "Standard Night Vision"], horizontal=True)
        
        img = np.zeros((360, 640, 3), dtype=np.uint8)
        
        if feed_mode == "Thermal Simulation":
            cv2.circle(img, (320, 180), 65, (0, 0, 255), -1)
            cv2.circle(img, (320, 180), 30, (0, 165, 255), -1)
            cv2.putText(img, "THERMAL LOCK: HUMAN SIGNATURE", (120, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        elif feed_mode == "Motion Detection Radar":
            cv2.rectangle(img, (200, 100), (440, 280), (0, 255, 0), 2)
            cv2.line(img, (320, 100), (320, 280), (0, 255, 0), 1)
            cv2.line(img, (200, 190), (440, 190), (0, 255, 0), 1)
            cv2.putText(img, f"MOTION SENSITIVITY: {sensitivity}%", (160, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        else:
            img[:, :, 1] = 110
            cv2.putText(img, "INFRARED NIGHT VISION ACTIVE", (140, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        st.image(img, channels="BGR", use_container_width=True)

    with col2:
        st.subheader("🚨 Threat & Protocol Status")
        if "Sector 4-B" in sector_select:
            st.error("⚠️ CRITICAL ALERT: Perimeter Breach Detected")
            st.warning("Target Trajectory: Heading North-West")
        else:
            st.success("✅ Sector Perimeter Secure")
            st.info("No Anomalies Detected")

        st.markdown("---")
        st.subheader("⚡ Tactical Response Protocols")
        
        if st.session_state["role"] in ["Base Command Officer", "System Administrator"]:
            if st.button("🚨 TRIGGER SILENT BASE ALARM"):
                st.success("Silent Emergency Signal Sent to Command HQ!")
            if st.button("📡 BROADCAST MESH PROTOCOL"):
                st.info("Mesh Nodes Synchronized Across Offline Network.")
        else:
            st.info("🔒 Field Patrol Role: Read-Only Emergency Controls")
