import streamlit as st
import cv2
import numpy as np
import pandas as pd
import time
import sqlite3
import hashlib

# --- 1. SECURE DATABASE INITIALIZATION ---
DB_NAME = "aegis_secure.db"

def init_db():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')
    c.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            operator TEXT NOT NULL,
            event TEXT NOT NULL,
            level TEXT NOT NULL
        )
    ''')
    
    c.execute('SELECT COUNT(*) FROM users')
    if c.fetchone()[0] == 0:
        default_hash = hashlib.sha256("1234".encode()).hexdigest()
        c.execute('INSERT INTO users VALUES (?, ?, ?)', ("COMMAND-01", default_hash, "Base Command Officer"))
    
    conn.commit()
    conn.close()

def verify_user(username, password):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    pwd_hash = hashlib.sha256(password.encode()).hexdigest()
    c.execute('SELECT role FROM users WHERE username = ? AND password_hash = ?', (username, pwd_hash))
    result = c.fetchone()
    conn.close()
    return result[0] if result else None

def register_user(username, password, role):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    pwd_hash = hashlib.sha256(password.encode()).hexdigest()
    try:
        c.execute('INSERT INTO users VALUES (?, ?, ?)', (username, pwd_hash, role))
        conn.commit()
        conn.close()
        return True
    except sqlite3.IntegrityError:
        conn.close()
        return False

def save_log(operator, event, level="INFO"):
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    ts = time.strftime("%Y-%m-%d %H:%M:%S")
    c.execute('INSERT INTO logs (timestamp, operator, event, level) VALUES (?, ?, ?, ?)', (ts, operator, event, level))
    conn.commit()
    conn.close()

def fetch_logs():
    conn = sqlite3.connect(DB_NAME)
    c = conn.cursor()
    c.execute('SELECT timestamp, operator, event, level FROM logs ORDER BY id DESC LIMIT 15')
    rows = c.fetchall()
    conn.close()
    return rows

init_db()

# --- 2. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AEGIS-GUARD | Sci-Fi AI Defense",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 3. ULTRA-FANCY CYBERPUNK HUD STYLES ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800;900&family=Share+Tech+Mono&display=swap');

    /* CRT Radar Scanline Overlay */
    .stApp::before {
        content: " ";
        display: block;
        position: fixed;
        top: 0; left: 0; bottom: 0; right: 0;
        background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.3) 50%), 
                    linear-gradient(90deg, rgba(255, 0, 0, 0.03), rgba(0, 255, 0, 0.01), rgba(0, 0, 255, 0.03));
        z-index: 999;
        background-size: 100% 3px, 6px 100%;
        pointer-events: none;
    }

    /* Sci-Fi Hexagonal Glow Background */
    .stApp {
        background-color: #03070d;
        background-image: 
            radial-gradient(circle at 50% 50%, rgba(0, 255, 204, 0.08) 0%, transparent 80%),
            radial-gradient(circle at 10% 20%, rgba(255, 0, 85, 0.05) 0%, transparent 50%),
            linear-gradient(rgba(0, 255, 204, 0.04) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 204, 0.04) 1px, transparent 1px);
        background-size: 100% 100%, 100% 100%, 30px 30px, 30px 30px;
        color: #00ffcc;
        font-family: 'Share Tech Mono', monospace;
    }

    /* Headings Styling */
    h1, h2, h3, h4 {
        font-family: 'Orbitron', sans-serif !important;
        letter-spacing: 3px;
        color: #00ffcc !important;
        text-shadow: 0 0 15px rgba(0, 255, 204, 0.6);
    }

    /* Fancy Glassmorphism Cards with Neon Glow */
    .fancy-card {
        background: rgba(6, 20, 30, 0.75);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(0, 255, 204, 0.4);
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 0 20px rgba(0, 255, 204, 0.2), inset 0 0 15px rgba(0, 255, 204, 0.1);
        transition: all 0.3s ease;
    }
    .fancy-card:hover {
        border-color: #00ffcc;
        box-shadow: 0 0 30px rgba(0, 255, 204, 0.6);
        transform: translateY(-3px);
    }

    .fancy-card-alert {
        background: rgba(40, 5, 15, 0.8);
        backdrop-filter: blur(12px);
        border: 1px solid rgba(255, 0, 85, 0.7);
        border-radius: 12px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 0 20px rgba(255, 0, 85, 0.3);
        animation: pulse-alert 1.8s infinite alternate;
    }
    @keyframes pulse-alert {
        0% { box-shadow: 0 0 15px rgba(255, 0, 85, 0.3); }
        100% { box-shadow: 0 0 30px rgba(255, 0, 85, 0.8); }
    }

    /* Neon Gradient Action Buttons */
    div.stButton > button {
        width: 100%;
        background: linear-gradient(135deg, rgba(0, 255, 204, 0.15), rgba(0, 0, 0, 0.9)) !important;
        border: 1px solid #00ffcc !important;
        color: #00ffcc !important;
        font-family: 'Orbitron', sans-serif !important;
        font-size: 0.85rem !important;
        letter-spacing: 2px;
        border-radius: 6px !important;
        padding: 12px 18px !important;
        box-shadow: 0 0 15px rgba(0, 255, 204, 0.25);
        transition: all 0.3s ease !important;
    }
    div.stButton > button:hover {
        background: #00ffcc !important;
        color: #03070d !important;
        font-weight: 900 !important;
        box-shadow: 0 0 30px rgba(0, 255, 204, 0.9) !important;
    }

    /* Radar animation */
    .radar {
        width: 110px;
        height: 110px;
        border-radius: 50%;
        border: 2px solid #00ffcc;
        background: radial-gradient(circle, rgba(0,255,204,0.2) 0%, rgba(0,0,0,0.95) 75%),
                    repeating-radial-gradient(circle, transparent 0, transparent 18px, rgba(0,255,204,0.15) 19px);
        position: relative;
        margin: 0 auto;
        box-shadow: 0 0 20px rgba(0, 255, 204, 0.4);
    }
    .radar::after {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        border-radius: 50%;
        background: conic-gradient(from 0deg, transparent 280deg, rgba(0,255,204,0.85) 360deg);
        animation: radar-sweep 2.2s linear infinite;
    }
    @keyframes radar-sweep {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }

    /* Animated Audio Visualizer Bar */
    .sound-bar-container {
        display: flex;
        align-items: flex-end;
        gap: 3px;
        height: 25px;
        justify-content: center;
        margin-top: 8px;
    }
    .bar {
        width: 4px;
        background: #00ffcc;
        box-shadow: 0 0 8px #00ffcc;
        animation: sound-wave 1s infinite ease-in-out alternate;
    }
    .bar:nth-child(1) { animation-delay: 0.1s; }
    .bar:nth-child(2) { animation-delay: 0.3s; }
    .bar:nth-child(3) { animation-delay: 0.2s; }
    .bar:nth-child(4) { animation-delay: 0.4s; }
    .bar:nth-child(5) { animation-delay: 0.15s; }
    @keyframes sound-wave {
        0% { height: 4px; }
        100% { height: 22px; }
    }
</style>
""", unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# --- 4. SECURE AUTHENTICATION PORTAL ---
if not st.session_state["logged_in"]:
    st.image("https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=1200&q=80", use_container_width=True)
    
    st.title("🛡️ AEGIS-GUARD | AI TACTICAL SHIELD")
    st.caption("FUTURISTIC AIR-GAPPED DEFENSE SYSTEM FOR SOLDIER SURVIVABILITY")
    st.markdown("---")
    
    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_b:
        tab1, tab2 = st.tabs(["🔒 SECURE AUTHENTICATION", "➕ REGISTER OPERATOR"])
        
        with tab1:
            st.markdown("##### OPERATOR ACCESS PORTAL")
            user = st.text_input("CALL SIGN", value="COMMAND-01", key="login_user")
            pin = st.text_input("ACCESS PIN / PASSWORD", type="password", value="1234", key="login_pass")
            
            if st.button("INITIALIZE SECURE SESSION"):
                role = verify_user(user, pin)
                if role:
                    st.session_state["logged_in"] = True
                    st.session_state["user"] = user
                    st.session_state["role"] = role
                    save_log(user, "User Authenticated Successfully", "INFO")
                    st.success("AUTHENTICATION SUCCESSFUL. LOADING HUD...")
                    st.rerun()
                else:
                    st.error("❌ INVALID CALL SIGN OR PIN")

        with tab2:
            st.markdown("##### ENCRYPTED CREDENTIAL CREATION")
            new_user = st.text_input("NEW CALL SIGN", key="reg_user")
            new_pin = st.text_input("CREATE ACCESS PIN", type="password", key="reg_pass")
            new_role = st.selectbox("ASSIGN ROLE", ["Base Command Officer", "Field Patrol Operator", "System Administrator"])
            
            if st.button("REGISTER OPERATOR ACCOUNT"):
                if new_user and new_pin:
                    if register_user(new_user, new_pin, new_role):
                        save_log(new_user, f"New Account Created [{new_role}]", "INFO")
                        st.success("✅ OPERATOR REGISTERED SUCCESSFULLY!")
                    else:
                        st.error("⚠️ CALL SIGN ALREADY TAKEN")

# --- 5. MAIN COMMAND CONSOLE ---
else:
    # Sidebar Setup
    st.sidebar.markdown("### 🎛️ SYSTEM COMMAND NODE")
    st.sidebar.markdown(f"**OPERATOR:** `{st.session_state['user']}`")
    st.sidebar.markdown(f"**ROLE:** `{st.session_state['role']}`")
    
    if st.sidebar.button("SECURE LOGOUT"):
        save_log(st.session_state["user"], "Operator Terminated Session", "INFO")
        st.session_state["logged_in"] = False
        st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.markdown('<div class="radar"></div>', unsafe_allow_html=True)
    st.sidebar.caption("<center style='color:#00ffcc; font-size:0.75rem; margin-top:6px;'>ACTIVE RADAR SWEEP</center>", unsafe_allow_html=True)
    
    # Animated Audio Equalizer Visualizer
    st.sidebar.markdown("""
    <div class="sound-bar-container">
        <div class="bar"></div><div class="bar"></div><div class="bar"></div><div class="bar"></div><div class="bar"></div>
    </div>
    <center style='color:#888; font-size:0.65rem;'>ACOUSTIC FEED: LIVE</center>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🪖 SOLDIER TELEMETRY")
    st.sidebar.image("https://images.unsplash.com/photo-1541872703-74c5e44368f9?auto=format&fit=crop&w=400&q=80", caption="PATROL TEAM ALPHA (BIO-SYNC 100%)", use_container_width=True)

    sector = st.sidebar.selectbox("FORWARD SECTOR", ["Sector 4-B (High Threat)", "Sector 1-A (Clear Outpost)", "Border Gate West"])
    sensor_mode = st.sidebar.radio("CV SPECTRUM FILTER", ["Real-Time Thermal", "Infrared Night Vision", "Standard Motion Bounding"])
    enable_audio = st.sidebar.checkbox("🔊 Tactical Audio Alerts", value=True)

    # Glowing Header Banner
    st.markdown("""
    <div style="background: linear-gradient(90deg, rgba(255,0,85,0.25), rgba(0,255,204,0.15), rgba(255,0,85,0.25)); border: 1px solid #ff0055; padding: 14px 20px; border-radius: 8px; margin-bottom: 20px; box-shadow: 0 0 25px rgba(255,0,85,0.4); display: flex; justify-content: space-between; align-items: center;">
        <div>
            <strong style="color: #ff0055; font-size: 1.15rem; letter-spacing:1px;">⚠️ FORWARD SOLDIER PROTECTION SYSTEM</strong><br>
            <span style="font-size: 0.85rem; color: #00ffcc;">Sub-2ms local AI edge processing prevents ambushes during total communication blackout.</span>
        </div>
        <span style="background: #ff0055; color: white; padding: 6px 12px; border-radius: 4px; font-weight: bold; font-size: 0.75rem; letter-spacing: 1px;">SOLDIER SHIELD ACTIVE</span>
    </div>
    """, unsafe_allow_html=True)

    # 4 Glowing HUD Metrics Cards
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown('<div class="fancy-card"><div style="font-size:0.7rem; color:#888;">TARGET DISTANCE</div><div style="font-size:1.6rem; font-weight:800; color:#00ffcc;">142.4 M</div></div>', unsafe_allow_html=True)
    with m2:
        st.markdown('<div class="fancy-card"><div style="font-size:0.7rem; color:#888;">SOLDIER PULSE</div><div style="font-size:1.6rem; font-weight:800; color:#00ffcc;">78 BPM</div></div>', unsafe_allow_html=True)
    with m3:
        st.markdown('<div class="fancy-card"><div style="font-size:0.7rem; color:#888;">EDGE LATENCY</div><div style="font-size:1.6rem; font-weight:800; color:#00ffcc;">1.2 ms</div></div>', unsafe_allow_html=True)
    with m4:
        is_threat = "Sector 4-B" in sector
        card_class = "fancy-card-alert" if is_threat else "fancy-card"
        threat_text = "LEVEL 4 BREACH" if is_threat else "SECURE"
        text_color = "#ff0055" if is_threat else "#00ffcc"
        st.markdown(f'<div class="{card_class}"><div style="font-size:0.7rem; color:{text_color};">THREAT LEVEL</div><div style="font-size:1.6rem; font-weight:800; color:{text_color};">{threat_text}</div></div>', unsafe_allow_html=True)

    st.write("")
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### 📹 AUTONOMOUS VISION SCOPE")
        use_camera = st.checkbox("ACTIVATE OPTICAL STREAM", value=True)
        frame_window = st.image([])

        if use_camera:
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            if ret:
                frame = cv2.resize(frame, (640, 360))
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                box_color = (0, 255, 0)
                status_text = "AI CV LOCK: MONITORING"

                if sensor_mode == "Real-Time Thermal":
                    frame = cv2.applyColorMap(gray, cv2.COLORMAP_JET)
                    box_color = (0, 255, 255)
                    status_text = "THERMAL HEAT TRACKING LOCK"
                elif sensor_mode == "Infrared Night Vision":
                    frame = cv2.applyColorMap(gray, cv2.COLORMAP_SUMMER)
                    box_color = (0, 255, 0)
                    status_text = "INFRARED MOTION LOCK"

                h, w, _ = frame.shape
                cx, cy = w // 2, h // 2

                # HUD Crosshairs
                cv2.rectangle(frame, (w//4, h//4), (3*w//4, 3*h//4), box_color, 2)
                cv2.putText(frame, status_text, (w//4, h//4 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, box_color, 2)
                cv2.circle(frame, (cx, cy), 35, box_color, 1)
                cv2.line(frame, (cx - 45, cy), (cx + 45, cy), box_color, 1)

                frame_window.image(frame, channels="BGR", use_container_width=True)

                if sensor_mode == "Real-Time Thermal" and enable_audio:
                    st.components.v1.html('<audio autoplay><source src="https://www.soundjay.com/buttons/beep-07a.mp3" type="audio/mpeg"></audio>', height=0)
            cap.release()
        else:
            st.image("https://images.unsplash.com/photo-1508614589041-895b88991e3e?auto=format&fit=crop&w=800&q=80", caption="STANDBY SAMPLE THERMAL SCOPE STREAM", use_container_width=True)

        st.markdown("### 📍 GPS INCURSION MAP & SATELLITE RECON")
        map_data = pd.DataFrame({'lat': [28.5355], 'lon': [77.3910]})
        st.map(map_data, zoom=10)

    with col2:
        st.markdown("### 🚨 REAL-TIME THREAT ALERT")
        if "Sector 4-B" in sector:
            st.error("⚠️ PERIMETER BREACH DETECTED!")
        else:
            st.success("✅ SECTOR PERIMETER CLEAR")

        st.markdown("---")
        st.markdown("### ⚡ SOLDIER PROTECTION PROTOCOLS")
        
        if st.session_state["role"] in ["Base Command Officer", "System Administrator"]:
            if st.button("🚨 TRIGGER SILENT ALERT TO FIELD"):
                save_log(st.session_state['user'], "Triggered Silent Alert to Soldiers", "WARN")
                st.error("🚨 HAPTIC VIBRATION DISPATCHED TO FIELD VESTS!")
                st.components.v1.html('<audio autoplay><source src="https://www.soundjay.com/buttons/beep-01a.mp3" type="audio/mpeg"></audio>', height=0)

            st.write("")
            if st.button("📡 DISPATCH AUTOMATED MESH DRONE"):
                save_log(st.session_state['user'], "Dispatched Recon Drone Mesh", "INFO")
                st.info("Autonomous Recon Drone Mesh Dispatched.")

        st.markdown("---")
        st.markdown("### 📋 IMMUTABLE AUDIT TRAIL")
        
        db_logs = fetch_logs()
        for timestamp, operator, event, level in db_logs:
            color = "#00ffcc" if level == "INFO" else "#ff0055"
            st.markdown(f"""
            <div style="background: rgba(5, 15, 22, 0.95); border-left: 3px solid {color}; padding: 6px 10px; font-size: 0.8rem; color: {color}; margin-bottom: 4px; border-radius: 0 4px 4px 0;">
                <span style="opacity: 0.6;">[{timestamp}]</span> <strong>[{operator}]</strong> {event}
            </div>
            """, unsafe_allow_html=True)
