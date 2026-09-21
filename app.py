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
    # Users table
    c.execute('''
        CREATE TABLE IF NOT EXISTS users (
            username TEXT PRIMARY KEY,
            password_hash TEXT NOT NULL,
            role TEXT NOT NULL
        )
    ''')
    # Audit logs table
    c.execute('''
        CREATE TABLE IF NOT EXISTS logs (
            id INTEGER PRIMARY KEY AUTOINCREMENT,
            timestamp TEXT NOT NULL,
            operator TEXT NOT NULL,
            event TEXT NOT NULL,
            level TEXT NOT NULL
        )
    ''')
    
    # Create default admin account if table is empty
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

# Initialize Database
init_db()

# --- 2. PAGE CONFIGURATION ---
st.set_page_config(
    page_title="AEGIS-GUARD | Secure Tactical AI",
    page_icon="🛡️",
    layout="wide",
    initial_sidebar_state="expanded"
)

# --- 3. ADVANCED STYLES & CRT HUD EFFECT ---
st.markdown("""
<style>
    @import url('https://fonts.googleapis.com/css2?family=Orbitron:wght@400;600;800;900&family=Share+Tech+Mono&display=swap');

    /* CRT Radar Overlay */
    .stApp::before {
        content: " ";
        display: block;
        position: fixed;
        top: 0; left: 0; bottom: 0; right: 0;
        background: linear-gradient(rgba(18, 16, 16, 0) 50%, rgba(0, 0, 0, 0.25) 50%), 
                    linear-gradient(90deg, rgba(255, 0, 0, 0.03), rgba(0, 255, 0, 0.01), rgba(0, 0, 255, 0.03));
        z-index: 999;
        background-size: 100% 3px, 6px 100%;
        pointer-events: none;
    }

    /* Dark Theme Setup */
    .stApp {
        background-color: #03070d;
        background-image: 
            radial-gradient(circle at 50% 50%, rgba(0, 255, 204, 0.05) 0%, transparent 80%),
            linear-gradient(rgba(0, 255, 204, 0.03) 1px, transparent 1px),
            linear-gradient(90deg, rgba(0, 255, 204, 0.03) 1px, transparent 1px);
        background-size: 100% 100%, 40px 40px, 40px 40px;
        color: #00ffcc;
        font-family: 'Share Tech Mono', monospace;
    }

    h1, h2, h3, h4 {
        font-family: 'Orbitron', sans-serif !important;
        letter-spacing: 2px;
        color: #00ffcc !important;
        text-shadow: 0 0 10px rgba(0, 255, 204, 0.5);
    }

    /* Glass Cards */
    .hud-card {
        background: rgba(6, 18, 26, 0.7);
        backdrop-filter: blur(8px);
        border: 1px solid rgba(0, 255, 204, 0.3);
        border-radius: 8px;
        padding: 15px;
        text-align: center;
        box-shadow: 0 0 15px rgba(0, 255, 204, 0.15);
    }
    .hud-card-critical {
        background: rgba(30, 5, 12, 0.7);
        border: 1px solid rgba(255, 0, 85, 0.5);
        box-shadow: 0 0 15px rgba(255, 0, 85, 0.2);
    }

    /* Tactical Buttons */
    div.stButton > button {
        width: 100%;
        background: linear-gradient(135deg, rgba(0, 255, 204, 0.1), rgba(0, 0, 0, 0.8)) !important;
        border: 1px solid #00ffcc !important;
        color: #00ffcc !important;
        font-family: 'Orbitron', sans-serif !important;
        border-radius: 4px !important;
        padding: 10px 16px !important;
        transition: all 0.3s ease !important;
    }
    div.stButton > button:hover {
        background: #00ffcc !important;
        color: #03070d !important;
        font-weight: 900 !important;
        box-shadow: 0 0 25px rgba(0, 255, 204, 0.8) !important;
    }

    /* Radar animation */
    .radar {
        width: 100px;
        height: 100px;
        border-radius: 50%;
        border: 1px solid #00ffcc;
        background: radial-gradient(circle, rgba(0,255,204,0.15) 0%, rgba(0,0,0,0.9) 70%);
        position: relative;
        margin: 0 auto;
    }
    .radar::after {
        content: "";
        position: absolute;
        top: 0; left: 0; right: 0; bottom: 0;
        border-radius: 50%;
        background: conic-gradient(from 0deg, transparent 280deg, rgba(0,255,204,0.8) 360deg);
        animation: radar-sweep 2.5s linear infinite;
    }
    @keyframes radar-sweep {
        from { transform: rotate(0deg); }
        to { transform: rotate(360deg); }
    }
</style>
""", unsafe_allow_html=True)

# Session State Initializer
if "logged_in" not in st.session_state:
    st.session_state["logged_in"] = False

# --- 4. SECURE AUTHENTICATION PORTAL ---
if not st.session_state["logged_in"]:
    st.title("🛡️ AEGIS-GUARD: SECURE PORTAL")
    st.caption("AIR-GAPPED ENCRYPTED AUTHENTICATION MATRIX")
    st.markdown("---")
    
    col_a, col_b, col_c = st.columns([1, 2, 1])
    with col_b:
        tab1, tab2 = st.tabs(["🔒 SECURE LOGIN", "➕ REGISTER OPERATOR"])
        
        with tab1:
            st.markdown("##### ENTER OPERATOR CREDENTIALS")
            user = st.text_input("CALL SIGN", value="COMMAND-01", key="login_user")
            pin = st.text_input("ACCESS PIN / PASSWORD", type="password", value="1234", key="login_pass")
            
            if st.button("AUTHENTICATE SYSTEM"):
                role = verify_user(user, pin)
                if role:
                    st.session_state["logged_in"] = True
                    st.session_state["user"] = user
                    st.session_state["role"] = role
                    save_log(user, "User Authenticated Successfully", "INFO")
                    st.success("AUTHENTICATION SUCCESSFUL. LOADING CONSOLE...")
                    st.rerun()
                else:
                    st.error("❌ INVALID CALL SIGN OR PIN")

        with tab2:
            st.markdown("##### CREATE ENCRYPTED ACCOUNT")
            new_user = st.text_input("NEW CALL SIGN", key="reg_user")
            new_pin = st.text_input("CREATE ACCESS PIN", type="password", key="reg_pass")
            new_role = st.selectbox("ASSIGN ROLE", ["Base Command Officer", "Field Patrol Operator", "System Administrator"])
            
            if st.button("ENCRYPT & REGISTER ACCOUNT"):
                if new_user and new_pin:
                    if register_user(new_user, new_pin, new_role):
                        save_log(new_user, f"New Account Created [{new_role}]", "INFO")
                        st.success("✅ OPERATOR REGISTERED! YOU CAN NOW LOGIN.")
                    else:
                        st.error("⚠️ CALL SIGN ALREADY TAKEN")

# --- 5. MAIN COMMAND CONSOLE ---
else:
    # Sidebar Setup
    st.sidebar.markdown("### 🎛️ COMMAND NODE")
    st.sidebar.markdown(f"**OPERATOR:** `{st.session_state['user']}`")
    st.sidebar.markdown(f"**ROLE:** `{st.session_state['role']}`")
    
    if st.sidebar.button("SECURE LOGOUT"):
        save_log(st.session_state["user"], "Operator Terminated Session", "INFO")
        st.session_state["logged_in"] = False
        st.rerun()

    st.sidebar.markdown("---")
    st.sidebar.markdown('<div class="radar"></div>', unsafe_allow_html=True)
    st.sidebar.caption("<center>RADAR SWEEP: ACTIVE</center>", unsafe_allow_html=True)
    st.sidebar.markdown("---")

    sector = st.sidebar.selectbox("FORWARD SECTOR", ["Sector 4-B (High Threat)", "Sector 1-A (Clear Outpost)", "Border Gate West"])
    sensor_mode = st.sidebar.radio("CV SPECTRUM FILTER", ["Real-Time Thermal", "Infrared Night Vision", "Standard Motion Bounding"])
    enable_audio = st.sidebar.checkbox("🔊 Audio Alerts", value=True)

    # Narrative Banner
    st.markdown("""
    <div style="background: rgba(255,0,85,0.15); border: 1px solid #ff0055; padding: 10px 15px; border-radius: 6px; margin-bottom: 15px;">
        <strong style="color: #ff0055;">⚠️ SOLDIER PROTECTION SYSTEM ACTIVE</strong><br>
        <span style="font-size: 0.85rem; color: #00ffcc;">Edge AI local processing prevents ambush risks in air-gapped blackout zones.</span>
    </div>
    """, unsafe_allow_html=True)

    # HUD Metrics
    m1, m2, m3, m4 = st.columns(4)
    with m1:
        st.markdown('<div class="hud-card"><div style="font-size:0.7rem; color:#888;">TARGET DISTANCE</div><div style="font-size:1.5rem; font-weight:800; color:#00ffcc;">142.4 M</div></div>', unsafe_allow_html=True)
    with m2:
        st.markdown('<div class="hud-card"><div style="font-size:0.7rem; color:#888;">SOLDIER PULSE</div><div style="font-size:1.5rem; font-weight:800; color:#00ffcc;">78 BPM</div></div>', unsafe_allow_html=True)
    with m3:
        st.markdown('<div class="hud-card"><div style="font-size:0.7rem; color:#888;">EDGE LATENCY</div><div style="font-size:1.5rem; font-weight:800; color:#00ffcc;">1.2 ms</div></div>', unsafe_allow_html=True)
    with m4:
        is_threat = "Sector 4-B" in sector
        card_class = "hud-card-critical" if is_threat else "hud-card"
        threat_text = "LEVEL 4 BREACH" if is_threat else "SECURE"
        text_color = "#ff0055" if is_threat else "#00ffcc"
        st.markdown(f'<div class="{card_class}"><div style="font-size:0.7rem; color:{text_color};">THREAT LEVEL</div><div style="font-size:1.5rem; font-weight:800; color:{text_color};">{threat_text}</div></div>', unsafe_allow_html=True)

    st.write("")
    col1, col2 = st.columns([2, 1])

    with col1:
        st.markdown("### 📹 AUTONOMOUS VISION SCOPE")
        use_camera = st.checkbox("ACTIVATE OPTICAL CAMERA STREAM", value=True)
        frame_window = st.image([])

        if use_camera:
            cap = cv2.VideoCapture(0)
            ret, frame = cap.read()
            if ret:
                frame = cv2.resize(frame, (640, 360))
                gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                box_color = (0, 255, 0)
                status_text = "AI CV LOCK: ACTIVE"

                if sensor_mode == "Real-Time Thermal":
                    frame = cv2.applyColorMap(gray, cv2.COLORMAP_JET)
                    box_color = (0, 255, 255)
                    status_text = "THERMAL HEAT SIGNATURE LOCK"
                elif sensor_mode == "Infrared Night Vision":
                    frame = cv2.applyColorMap(gray, cv2.COLORMAP_SUMMER)
                    box_color = (0, 255, 0)
                    status_text = "INFRARED LOCK"

                h, w, _ = frame.shape
                cx, cy = w // 2, h // 2

                # HUD Overlay
                cv2.rectangle(frame, (w//4, h//4), (3*w//4, 3*h//4), box_color, 2)
                cv2.putText(frame, status_text, (w//4, h//4 - 10), cv2.FONT_HERSHEY_SIMPLEX, 0.45, box_color, 2)
                cv2.circle(frame, (cx, cy), 35, box_color, 1)

                frame_window.image(frame, channels="BGR", use_container_width=True)

                if sensor_mode == "Real-Time Thermal" and enable_audio:
                    st.components.v1.html('<audio autoplay><source src="https://www.soundjay.com/buttons/beep-07a.mp3" type="audio/mpeg"></audio>', height=0)
            cap.release()

        st.markdown("### 📍 INCURSION GPS MAP")
        map_data = pd.DataFrame({'lat': [28.5355], 'lon': [77.3910]})
        st.map(map_data, zoom=10)

    with col2:
        st.markdown("### 🚨 REAL-TIME THREAT ALERT")
        if "Sector 4-B" in sector:
            st.error("⚠️ PERIMETER INCURSION DETECTED!")
        else:
            st.success("✅ SECTOR PERIMETER CLEAR")

        st.markdown("---")
        st.markdown("### ⚡ RESPONSE PROTOCOLS")
        
        if st.session_state["role"] in ["Base Command Officer", "System Administrator"]:
            if st.button("🚨 TRIGGER SILENT ALERT TO FIELD"):
                save_log(st.session_state['user'], "Triggered Silent Alert to Soldiers", "WARN")
                st.error("🚨 ALERT DISPATCHED TO SOLDIER HAPTIC VESTS!")
                st.components.v1.html('<audio autoplay><source src="https://www.soundjay.com/buttons/beep-01a.mp3" type="audio/mpeg"></audio>', height=0)

            st.write("")
            if st.button("📡 DISPATCH MESH RECON DRONE"):
                save_log(st.session_state['user'], "Dispatched Recon Drone Mesh", "INFO")
                st.info("Drone Mesh Deployed for Reconnaissance.")

        st.markdown("---")
        st.markdown("### 📋 PERSISTENT AUDIT TRAIL")
        
        # Pull live audit logs from SQLite Database
        db_logs = fetch_logs()
        for timestamp, operator, event, level in db_logs:
            color = "#00ffcc" if level == "INFO" else "#ff0055"
            st.markdown(f"""
            <div style="background: rgba(5, 15, 22, 0.9); border-left: 3px solid {color}; padding: 6px 10px; font-size: 0.8rem; color: {color}; margin-bottom: 4px;">
                <span style="opacity: 0.6;">[{timestamp}]</span> <strong>[{operator}]</strong> {event}
            </div>
            """, unsafe_allow_html=True)
