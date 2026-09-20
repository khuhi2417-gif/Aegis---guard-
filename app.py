import streamlit as st
import cv2
import numpy as np

st.set_page_config(page_title="AEGIS-GUARD", layout="wide")

st.markdown("""
<style>
    .stApp { background-color: #0b0f19; color: #ffffff; }
</style>
""", unsafe_allow_html=True)

st.title("🛡️ AEGIS-GUARD: Zero-Network AI Border Defense Shield")
st.caption("Team Guardian | Real-Time Tactical Motion & Thermal Surveillance")
st.markdown("---")

col1, col2 = st.columns([2, 1])

with col1:
    st.subheader("📹 Live Tactical Surveillance Feed")
    feed_mode = st.radio("Select Sensor Mode:", ["Thermal Simulation", "Motion Detection Radar", "Standard Night Vision"], horizontal=True)
    
    run_feed = st.checkbox("Activate Sensor Feed", value=True)
    frame_placeholder = st.empty()
    
    if run_feed:
        # Generate simulated camera feed frame
        img = np.zeros((360, 640, 3), dtype=np.uint8)
        
        if feed_mode == "Thermal Simulation":
            cv2.circle(img, (320, 180), 80, (0, 0, 255), -1)
            cv2.putText(img, "THERMAL TARGET DETECTED", (150, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        elif feed_mode == "Motion Detection Radar":
            cv2.rectangle(img, (200, 100), (440, 280), (0, 255, 0), 2)
            cv2.putText(img, "MOTION LOCK: SECTOR 4", (180, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        else:
            img[:, :, 1] = 100
            cv2.putText(img, "NIGHT VISION ACTIVE", (200, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

        frame_placeholder.image(img, channels="BGR", use_container_width=True)

with col2:
    st.subheader("🚨 Sector Threat Alert System")
    st.error("ALERT: Intrusion Detected in Sector 4-B")
    st.warning("Network Status: Air-Gapped / Offline Mesh Active")
    st.info("Threat Level: HIGH | Target Velocity: 1.2 m/s")
    
    st.markdown("---")
    if st.button("Trigger Silent Alarm"):
        st.success("Silent Alert Sent to Local Base Command!")
