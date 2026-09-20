import streamlit as st
import cv2
import numpy as np

# Page configuration
st.set_page_config(
    page_title="AEGIS-GUARD | AI Border Defense Shield",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom Styling for Tactical Dark Mode
st.markdown("""
<style>
    .stApp { background-color: #0b0f19; color: #ffffff; }
    .stButton>button { width: 100%; background-color: #d9534f; color: white; border-radius: 5px; font-weight: bold; }
    .stButton>button:hover { background-color: #c9302c; color: white; }
</style>
""", unsafe_allow_html=True)

# Sidebar - Command Controls
st.sidebar.title("🎛️ Command Controls")
st.sidebar.subheader("System Status")
st.sidebar.success("AIR-GAPPED MESH: ONLINE")
st.sidebar.info("BASE LOCATION: SECTOR 4-NORTH")

st.sidebar.markdown("---")
sensitivity = st.sidebar.slider("Sensor Sensitivity Level", 1, 100, 75)
alert_threshold = st.sidebar.slider("Motion Detection Threshold (m)", 0.5, 5.0, 1.2)

# Main Title Header
st.title("🛡️ AEGIS-GUARD: Zero-Network AI Border Defense Shield")
st.caption("Team Guardian | Real-Time Tactical Motion & Thermal Surveillance")
st.markdown("---")

# Main Dashboard Columns
col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📹 Live Tactical Surveillance Feed")
    feed_mode = st.radio(
        "Select Sensor Mode:", 
        ["Thermal Simulation", "Motion Detection Radar", "Standard Night Vision"], 
        horizontal=True
    )
    
    run_feed = st.checkbox("Activate Sensor Feed", value=True)
    frame_placeholder = st.empty()
    
    if run_feed:
        # Create simulated tactical video frame
        img = np.zeros((360, 640, 3), dtype=np.uint8)
        
        if feed_mode == "Thermal Simulation":
            # Simulate a thermal heat signatures
            cv2.circle(img, (320, 180), 60, (0, 0, 255), -1)
            cv2.circle(img, (320, 180), 30, (0, 165, 255), -1)
            cv2.putText(img, "THERMAL TARGET LOCK", (160, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        elif feed_mode == "Motion Detection Radar":
            # Simulate a motion tracking bounding box
            cv2.rectangle(img, (200, 100), (440, 280), (0, 255, 0), 2)
            cv2.line(img, (320, 100), (320, 280), (0, 255, 0), 1)
            cv2.line(img, (200, 190), (440, 190), (0, 255, 0), 1)
            cv2.putText(img, "MOTION LOCK: SECTOR 4-B", (150, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        else:
            # Simulate night vision filter
            img[:, :, 1] = 120
            cv2.putText(img, "NIGHT VISION ACTIVE (INFRARED)", (120, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        frame_placeholder.image(img, channels="BGR", use_container_width=True)

with col2:
    st.subheader("🚨 Sector Threat Alert System")
    st.error("⚠️ CRITICAL ALERT: Intrusion Detected in Sector 4-B")
    st.warning(f"Sensor Sensitivity Set To: {sensitivity}%")
    st.info(f"Target Velocity: {alert_threshold} m/s | Lock Status: HELD")
    
    st.markdown("---")
    st.subheader("⚡ Tactical Actions")
    if st.button("🚨 TRIGGER SILENT ALARM"):
        st.success("Silent Alert Transmitted to Base Command!")
    
    if st.button("📡 BROADCAST MESH REPEAT"):
        st.info("Mesh Signal Broadcasted Across Offline Nodes.")
