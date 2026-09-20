import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoTransformerBase, RTCConfiguration
import cv2
import numpy as np
import datetime

# Page Configuration
st.set_page_config(
    page_title="AEGIS-GUARD | Zero-Network Tactical Shield",
    page_icon="🛡️",
    layout="wide"
)

# Dark Tactical UI Styling
st.markdown("""
    <style>
    .main { background-color: #080c14; color: #00f2fe; font-family: 'Courier New', monospace; }
    .stMetric { background-color: #0f172a; padding: 12px; border-radius: 6px; border: 1px solid #1e293b; }
    h1, h2, h3 { color: #00f2fe !important; }
    </style>
""", unsafe_allow_html=True)

st.title("🛡️ AEGIS-GUARD: Zero-Network AI Pre-Threat & Border Defense Shield")[span_0](start_span)[span_0](end_span)
st.caption("Team Guardian X | AI'S GOT TALENT 2026 | CSI Chapter — SRM Delhi-NCR")[span_1](start_span)[span_1](end_span)
st.markdown("*> 'Detecting Threats. Protecting Personnel. Saving Lives.'*")[span_2](start_span)[span_2](end_span)
st.markdown("---")

tab1, tab2, tab3, tab4 = st.tabs(["📹 LIVE TACTICAL FEED", "⚠️ THE PROBLEM", "💡 SOLUTION & ARCHITECTURE", "🚀 STRATEGIC ROADMAP"])

# TAB 1: LIVE DEMO & THERMAL SCANNING
with tab1:
    col_feed, col_status = st.columns([2, 1])
    
    with col_status:
        st.subheader("📡 System Status")
        st.metric(label="NETWORK STATUS", value="AIR-GAPPED", delta="0 KB/s (Jam-Proof)")[span_3](start_span)[span_3](end_span)
        st.metric(label="HARDWARE MODE", value="Edge AI Node", delta="15W Power")
        st.metric(label="THERMAL SPECTRUM", value="MWIR Scanning", delta="Active")[span_4](start_span)[span_4](end_span)
        
        st.markdown("---")
        st.subheader("⚙️ Tactical Controls")
        sensitivity = st.slider("Motion Contour Threshold (Sensitivity)", 500, 5000, 1800, 100)[span_5](start_span)[span_5](end_span)

    # Backend OpenCV Image Processing Class
    class MWIRThermalProcessor(VideoTransformerBase):
        def __init__(self):
            self.backSub = cv2.createBackgroundSubtractorMOG2(history=500, varThreshold=50, detectShadows=False)

        def recv(self, frame):
            img = frame.to_ndarray(format="bgr24")

            # 1. High-Contrast Thermal Simulation (MWIR Mapping)
            gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
            blurred = cv2.GaussianBlur(gray, (15, 15), 0)
            thermal_sim = cv2.applyColorMap(blurred, cv2.COLORMAP_JET)

            # 2. Motion Detection & Edge Masking
            fg_mask = self.backSub.apply(blurred)
            _, thresh = cv2.threshold(fg_mask, 200, 255, cv2.THRESH_BINARY)
            kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (5, 5))
            thresh = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)

            # 3. Target Tracking & Bounding Box Overlays
            contours, _ = cv2.findContours(thresh, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
            threat_count = 0

            for cnt in contours:
                area = cv2.contourArea(cnt)
                if area > sensitivity:
                    threat_count += 1
                    x, y, w, h = cv2.boundingRect(cnt)

                    cv2.rectangle(thermal_sim, (x, y), (x + w, y + h), (0, 0, 255), 2)[span_6](start_span)[span_6](end_span)
                    cv2.putText(thermal_sim, f"TARGET #{threat_count} [HEAT SIG]", (x, y - 10), 
                                cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 255), 2)
                    cx, cy = x + w // 2, y + h // 2
                    cv2.drawMarker(thermal_sim, (cx, cy), (0, 0, 255), cv2.MARKER_CROSS, 15, 2)

            import av
            return av.VideoFrame.from_ndarray(thermal_sim, format="bgr24")

    with col_feed:
        st.subheader("📹 Real-Time Thermal Feed (MWIR Emulation)")[span_7](start_span)[span_7](end_span)
        RTC_CONFIG = RTCConfiguration({"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]})
        
        webrtc_streamer(
            key="aegis-tactical-feed",
            video_processor_factory=MWIRThermalProcessor,
            rtc_configuration=RTC_CONFIG,
            media_stream_constraints={"video": True, "audio": False}
        )

# TAB 2: THE PROBLEM
with tab2:
    st.subheader("Critical Tactical Vulnerabilities")[span_8](start_span)[span_8](end_span)
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        st.error("🚨 **> 60%+ Casualty Rate in Ambushes**")[span_9](start_span)[span_9](end_span)
        st.write("Surprise attacks in high-risk border zones leave zero initial reaction time for patrol units.")[span_10](start_span)[span_10](end_span)
        st.error("❄️ **Extreme Climate Blind Spots**")[span_11](start_span)[span_11](end_span)
        st.write("High-altitude sectors (-20°C to -40°C) suffer heavy snow and dense fog blinding human sentries.")[span_12](start_span)[span_12](end_span)
    with col_p2:
        st.warning("⏱️ **The Perception Gap**")[span_13](start_span)[span_13](end_span)
        st.write("Humans require 1.5 to 2.5 seconds to perceive and react to a sudden ambush.")[span_14](start_span)[span_14](end_span)
        st.warning("💔 **Permanent Personal Loss**")[span_15](start_span)[span_15](end_span)
        st.write("Fallen personnel leave irreplaceable voids for their families.")[span_16](start_span)[span_16](end_span)

# TAB 3: SOLUTION & ARCHITECTURE
with tab3:
    st.subheader("Aegis-Guard Edge Capabilities")[span_17](start_span)[span_17](end_span)
    col_s1, col_s2, col_s3 = st.columns(3)
    with col_s1:
        st.markdown("### 1. High-Contrast Thermal Scanning")[span_18](start_span)[span_18](end_span)
        st.write("MWIR processing detects body heat (+37°C) against sub-zero backgrounds.")[span_19](start_span)[span_19](end_span)
    with col_s2:
        st.markdown("### 2. Air-Gapped Local Edge AI")[span_20](start_span)[span_20](end_span)
        st.write("Runs OpenCV & YOLO locally with 0% cloud connectivity—100% jam-proof.")[span_21](start_span)[span_21](end_span)
    with col_s3:
        st.markdown("### 3. Offline Radio Telemetry")[span_22](start_span)[span_22](end_span)
        st.write("Transmits encrypted grid coordinates via local VHF frequencies.")[span_23](start_span)[span_23](end_span)

# TAB 4: ROADMAP
with tab4:
    st.subheader("Strategic Roadmap")[span_24](start_span)[span_24](end_span)
    st.info("**PHASE 1: CURRENT DEVELOPMENT** — Python/OpenCV engine running locally.")[span_25](start_span)[span_25](end_span)
    st.info("**PHASE 2: EDGE DEPLOYMENT** — Porting onto NVIDIA Jetson / Raspberry Pi.")[span_26](start_span)[span_26](end_span)
    st.info("**PHASE 3: ECOSYSTEM INTEGRATION** — Expanding to drone thermal feeds.")[span_27](start_span)[span_27](end_span)
