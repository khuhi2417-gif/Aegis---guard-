st.markdown("""
<style>
    /* Dark Military Grid Background */
    .stApp {
        background-color: #050a0e;
        background-image: linear-gradient(rgba(0, 255, 204, 0.03) 1px, transparent 1px),
                          linear-gradient(90deg, rgba(0, 255, 204, 0.03) 1px, transparent 1px);
        background-size: 30px 30px;
        color: #00ffcc;
        font-family: 'Share Tech Mono', monospace;
    }

    /* Glowing Card Effect */
    div[data-testid="stMetricValue"] {
        font-size: 2rem !important;
        color: #00ffcc !important;
        text-shadow: 0 0 10px rgba(0, 255, 204, 0.5);
    }

    /* Red Tactical Alert Box */
    .stAlert {
        border: 1px solid #ff0055 !important;
        box-shadow: 0 0 15px rgba(255, 0, 85, 0.4);
        background-color: rgba(255, 0, 85, 0.1) !important;
    }

    /* Glowing Buttons */
    .stButton>button {
        background: linear-gradient(180deg, #1f2937, #111827);
        border: 1px solid #00ffcc !important;
        color: #00ffcc !important;
        box-shadow: 0 0 8px rgba(0, 255, 204, 0.3);
        transition: all 0.3s ease;
    }
    
    .stButton>button:hover {
        background: #00ffcc !important;
        color: #000 !important;
        box-shadow: 0 0 20px rgba(0, 255, 204, 0.8);
    }
</style>
""", unsafe_allow_html=True)
