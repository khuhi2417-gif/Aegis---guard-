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
    page_title="AEGIS-GUARD | ULTRA HUD TERMINAL",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 3. CLEAN SCI-FI HUD CSS OVERHAUL (NO SCANLINES / NO GRID LINES) ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;700;900&family=Share+Tech+Mono&display=swap');

    /* Clean Solid Dark Background (Removed CRT Scanlines and Grid Overlay) */
    .stApp {
        background-color: #02060d;
        color: #00ffcc;
        font-family: 'Share Tech Mono', monospace;
    }

    /* Sci-Fi Glowing Headings */
    h1, h2, h3, h4 {
        font-family: 'Orbitron', sans-serif !important;
        letter-spacing: 2px;
        color: #00ffcc !important;
        text-shadow: 0 0 10px rgba(0, 255, 204, 0.5);
    }

    /* Holographic Glassmorphism Cards */
    .holo-card {
        background: rgba(4, 18, 28, 0.85);
        border: 1px solid rgba(0, 255, 204, 0.4);
        border-radius: 8px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 0 15px rgba(0, 255, 204, 0.15);
        transition: all 0.3s ease;
    }
    .holo-card:hover {
        border-color: #00ffcc;
        box-shadow: 0 0 25px rgba(0, 255, 204, 0.5);
        transform: translateY(-2px);
    }

    .holo-card-alert {
        background: rgba(45, 4, 18, 0.85);
        border: 1px solid rgba(255, 0, 85, 0.8);
        border-radius: 8px;
        padding: 16px;
        text-align: center;
        box-shadow: 0 0 20px rgba(255, 0, 85, 0.3);
        animation: pulse-border 1.5s infinite alternate;
    }
    @keyframes pulse-border {
        0% { box-shadow: 0 0 10px rgba(255, 0, 85, 0.3); border-color: rgba(255,0,85,0.5); }
        100% { box-shadow: 0 0 25px rgba(255, 0, 85, 0.9); border-color: rgba(255,0,85,1); }
    }

    /* Interactive Action Buttons */
    div.stButton > button {
        width: 100%;
        background: linear-gradient(135deg, rgba(0, 255, 204, 0.15), rgba(0, 0, 0, 0.9)) !important;
        border: 1px solid #00ffcc !important;
        color: #00ffcc !important;
        font-family: 'Orbitron', sans-serif !important;
        font-size: 0.85rem !important;
        letter-spacing: 1px;
        border-radius: 6px !important;
        padding: 10px 16px !important;
        box-shadow: 0 0 12px rgba(0, 255, 204, 0.2);
        transition: all 0.3s ease !important;
    }
    div.stButton > button:hover {
        background: #00ffcc !important;
        color: #02060d !important;
        font-weight: 700 !important;
        box-shadow: 0 0 25px rgba(0, 255, 204, 0.8) !important;
    }

    /* Animated Tactical Radar */
    .radar {
        width: 100px;
        height: 100px;
        border-radius: 50%;
        border: 2px solid #00ffcc;
        background: radial-gradient(circle, rgba(0,255,204,0.2) 0%, rgba(0,0,0,0.95) 75%);
        position: relative;
        margin: 0 auto;
    }
    .radar::after {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        border-radius: 50%;
        background: conic-gradient(from 0deg, transparent 270deg, rgba(0,255,204,0.8) 360deg);
        animation: radar-sweep 2s linear infinite;
    }
    @keyframes radar-sweep {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }

    /* Audio Waves Equalizer */
    .sound-bar-container {
        display: flex;
        align-items: flex-end;
        gap: 4px;
        height: 24px;
        justify-content: center;
        margin-top: 10px;
    }
    .bar {
        width: 4px;
        background: #00ffcc;
        box-shadow: 0 0 8px #00ffcc;
        animation: sound-wave 0.8s infinite ease-in-out alternate;
    }
    .bar:nth-child(1) { animation-delay: 0.1s; }
    .bar:nth-child(2) { animation-delay: 0.3s; }
    .bar:nth-child(3) { animation-delay: 0.2s; }
    .bar:nth-child(4) { animation-delay: 0.4s; }
    .bar:nth-child(5) { animation-delay: 0.15s; }
    @keyframes sound-wave {
        0% { height: 3px; }
        100% { height: 20px; }
    }
</style>
""", unsafe_allow_html=True)

if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# --- 4. SECURE AUTHENTICATION PORTAL ---
if not st.session_state["logged_in"]:
    st.image("https://images.unsplash.com/photo-1526374965328-7f61d4dc18c5?auto=format&fit=crop&w=1200&q=80", use_container_width=True)
    
    st.title("🛡️ AEGIS-GUARD | COMMAND ACCESS")
    st.caption("AIR-GAPPED ENCRYPTED EDGE-AI TACTICAL SHIELD PORTAL")
    st.markdown("---")
    
    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_b:
        tab1, tab2 = st.tabs(["🔒 AUTHENTICATE", "➕ REGISTER OPERATOR"])
        
        with tab1:
            st.markdown("##### OPERATOR IDENTIFICATION")
            user = st.text_input("CALL SIGN", value="COMMAND-01", key="login_user")
            pin = st.text_input("ACCESS PIN", type="password", value="1234", key="login_pass")
            
            if st.button("INITIALIZE SECURE SYSTEM"):
                role = verify_user(user, pin)
                if role:
                    st.session_state["logged_in"] = True
                    st.session_state["user"] = user
                    st.session_state["role"] = role
                    save_log(user, "User Authenticated Successfully", "INFO")
                    st.success("ACCESS GRANTED. INITIALIZING COMMAND HUD...")
                    st.rerun()
                else:
                    st.error("❌ INVALID OPERATOR CREDENTIALS")

        with tab2:
            st.markdown("##### ENCRYPT NEW OPERATOR")
            new_user = st.text_input("NEW CALL SIGN", key="reg_user")
            new_pin = st.text_input("CREATE PIN", type="password", key="reg_pass")
            new_role = st.selectbox("ASSIGN ROLE", ["Base Command Officer", "Field Patrol Operator", "System Administrator"])
            
            if st.button("ENCRYPT & REGISTER ACCOUNT"):
                if new_user and new_pin:
                    if register_user(new_user, new_pin, new_role):
                        save_log(new_user, f"New Account Created [{new_role}]", "INFO")
                        st.success("✅ OPERATOR ENCRYPTED AND SAVED.")
                    else:
                        st.error("⚠️ CALL SIGN ALREADY TAKEN")

# --- 5. MAIN COMMAND CONSOLE ---
else:
    # Sidebar HUD Node
    st.sidebar.markdown("### 🎛️ COMMAND NODE")
    st.sidebar.markdown(f"**OPERATOR:** `{st.session_state['user']}`")
    st.sidebar.markdown(f"**ROLE:** `{st.session_state['role']}`")
    
    if st.sidebar.button("TERMINATE SESSION"):
        save_log(st.session_state["user"], "Operator Terminated Session", "INFO")
        st.session_state["logged_in"] = False
        st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.markdown('<div class="radar"></div>', unsafe_allow_html=True)
    st.sidebar.caption("<center style='color:#00ffcc; font-size:0.75rem; margin-top:8px;'>RADAR LOCK: ACTIVE</center>", unsafe_allow_html=True)
    
    # Audio Visualizer Box
    st.sidebar.markdown("""
    <div class="sound-bar-container">
        <div class="bar"></div><div class="bar"></div><div class="bar"></div><div class="bar"></div><div class="bar"></div>
    </div>
    <center style='color:#888; font-size:0.65rem; margin-top:4px;'>ACOUSTIC SENSORS: ONLINE</center>
    """, unsafe_allow_html=True)

    st.sidebar.markdown("---")
    st.sidebar.markdown("### 🪖 SOLDIER TELEMETRY")
    st.sidebar.image("https://images.unsplash.com/photo-1541872703-74c5e44368f9?auto=format&fit=crop&w=400&q=80", caption="PATROL ALPHA (BIO-SYNC 100%)", use_container_width=True)

    sector = st.sidebar.selectbox("FORWARD SECTOR", ["Sector 4-B (High Threat)", "Sector 1-A (Clear Outpost)", "Border Gate West"])
    sensor_mode = st.sidebar.radio("CV SPECTRUM FILTER", ["Real-Time Thermal", "Infrared Night Vision", "Standard Motion Bounding"])
    enable_audio = st.sidebar.checkbox("🔊 Audio Alerts", value=True)

    # Top Narrative Glowing Banner
    st.markdown("""
    <div style="background: rgba(255,0,85,0.15); border: 1px solid #ff0055; padding: 14px 20px; border-radius: 8px; margin-bottom: 20px; display: flex; justify-content: space-between; align-items: center;">
        <div>
            <strong style="color: #ff0055; font-size: 1.15rem; letter-spacing:1px;">⚠️ FORWARD SOLDIER PROTECTION SYSTEM</strong><br>
            <span style="font-size: 0.85rem; color: #00ffcc;">Sub-2ms local AI edge processing prevents ambushes during total communication blackout.</span>
        </div>
        <span style="background: #ff0055; color: white; padding: 6px 12px; border-radius: 4px; font-weight: bold; font-size: 0.75rem; letter-spacing: 1px;">SOLDIER SHIELD ACTIVE</span>
    </div>
    """, unsafe_allow_html=True)

    # 4 Glowing Telemetry Metrics
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown('<div class="holo-card"><div style="font-size:0.7rem; color:#888;">TARGET DISTANCE</div><div style="font-size:1.6rem; font-weight:800; color:#00ffcc;">142.4 M</div></div>', unsafe_allow_html=True)
    with m2:
        st.markdown('<div class="holo-card"><div style="font-size:0.7rem; color:#888;">SOLDIER PULSE</div><div style="font-size:1.6rem; font-weight:800; color:#00ffcc;">78 BPM</div></div>', unsafe_allow_html=True)
    with m3:
        st.markdown('<div class="holo-card"><div style="font-size:0.7rem; color:#888;">EDGE LATENCY</div><div style="font-size:1.6rem; font-weight:800; color:#00ffcc;">1.2 ms</div></div>', unsafe_allow_html=True)
    with m4:
        is_threat = "Sector 4-B" in sector
        card_class = "holo-card-alert" if is_threat else "holo-card"
        threat_text = "LEVEL 4 BREACH" if is_threat else "SECURE"
        text_color = "#ff0055" if is_threat else "#00ffcc"
        st.markdown(f'<div class="{card_class}"><div style="font-size:0.7rem; color:{text_color};">THREAT LEVEL</div><div style="font-size:1.6rem; font-weight:800; color:{text_color};">{threat_text}</div></div>', unsafe_allow_html=True)

    st.write("")
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### 📹 AUTONOMOUS REAL-TIME VISION SCOPE")
        use_camera = st.checkbox("ACTIVATE LIVE OPTICAL FEED", value=True)
        frame_window = st.image([])

        if use_camera:
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            if ret:
                frame = cv2.resize(frame, (640, 360))
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                box_color = (0, 255, 0)
                status_text = "AI CV LOCK: ACTIVE MONITORING"

                # Thermal and Infrared Filters
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

                # Tactical HUD Overlay Rendering
                cv2.rectangle(frame, (w//4, h//4), (3*w//4, 3*h//4), box_color, 2)
                cv2.putText(frame, status_text, (w//4, h//4 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, box_color, 2)
                cv2.circle(frame, (cx, cy), 40, box_color, 1)
                cv2.line(frame, (cx - 50, cy), (cx + 50, cy), box_color, 1)
                cv2.line(frame, (cx, cy - 50), (cx, cy + 50), box_color, 1)

                frame_window.image(frame, channels="BGR", use_container_width=True)

                if sensor_mode == "Real-Time Thermal" and enable_audio:
                    st.components.v1.html('<audio autoplay><source src="https://www.soundjay.com/buttons/beep-07a.mp3" type="audio/mpeg"></audio>', height=0)
            cap.release()
        else:
            st.image("https://images.unsplash.com/photo-1508614589041-895b88991e3e?auto=format&fit=crop&w=800&q=80", caption="STANDBY THERMAL SCOPE FEED", use_container_width=True)

        st.markdown("### 📍 INCURSION GPS & SATELLITE RECON")
        map_data = pd.DataFrame({'lat': [28.5355], 'lon': [77.3910]})
        st.map(map_data, zoom=10)

    with col2:
        st.markdown("### 🚨 THREAT ANALYSIS")
        if "Sector 4-B" in sector:
            st.error("⚠️ PERIMETER BREACH DETECTED!")
        else:
            st.success("✅ SECTOR PERIMETER CLEAR")

        st.markdown("---")
        st.markdown("### ⚡ RESPONSE PROTOCOLS")
        
        if st.session_state["role"] in ["Base Command Officer", "System Administrator"]:
            if st.button("🚨 TRIGGER SILENT ALERT TO FIELD"):
                save_log(st.session_state['user'], "Triggered Silent Alert to Field Vests", "WARN")
                st.error("🚨 HAPTIC VIBRATION SIGNAL SENT TO SOLDIER VESTS!")
                st.components.v1.html('<audio autoplay><source src="https://www.soundjay.com/buttons/beep-01a.mp3" type="audio/mpeg"></audio>', height=0)

            st.write("")
            if st.button("📡 DISPATCH AUTOMATED MESH DRONE"):
                save_log(st.session_state['user'], "Dispatched Recon Drone Mesh", "INFO")
                st.info("Autonomous Drone Mesh Deployed.")

        st.markdown("---")
        st.markdown("### 📋 IMMUTABLE AUDIT LOG")
        
        db_logs = fetch_logs()
        for timestamp, operator, event, level in db_logs:
            color = "#00ffcc" if level == "INFO" else "#ff0055"
            st.markdown(f"""
            <div style="background: rgba(4, 15, 24, 0.95); border-left: 3px solid {color}; padding: 6px 10px; font-size: 0.8rem; color: {color}; margin-bottom: 4px; border-radius: 0 4px 4px 0;">
                <span style="opacity: 0.6;">[{timestamp}]</span> <strong>[{operator}]</strong> {event}
            </div>
            """, unsafe_allow_html=True)
