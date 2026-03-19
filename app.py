import streamlit as st
import numpy as np
import scipy.io.wavfile as wavfile
import tempfile
import json
import os

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Neural Harmony Generator",
    page_icon="🎵",
    layout="wide"
)

# ---------------- STYLING ----------------
st.markdown("""
<style>
.main {
    background: linear-gradient(135deg, #0e1117, #1c1f2b);
    color: white;
}
.title {
    font-size: 42px;
    font-weight: bold;
    text-align: center;
}
.card {
    background: rgba(255,255,255,0.05);
    padding: 20px;
    border-radius: 15px;
    backdrop-filter: blur(10px);
}
.stButton>button {
    background: linear-gradient(90deg, #ff4b4b, #ff7b7b);
    color: white;
    border-radius: 12px;
    height: 3em;
    width: 100%;
    font-size: 16px;
}
</style>
""", unsafe_allow_html=True)

# ---------------- USER DATABASE ----------------
USER_FILE = "users.json"

def load_users():
    if os.path.exists(USER_FILE):
        with open(USER_FILE, "r") as f:
            return json.load(f)
    return {}

def save_users(users):
    with open(USER_FILE, "w") as f:
        json.dump(users, f)

users = load_users()

# ---------------- SESSION ----------------
if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# ---------------- AUTH ----------------
if not st.session_state.logged_in:

    st.markdown("<div class='title'>🎵 Neural Harmony Generator</div>", unsafe_allow_html=True)
    st.markdown("### 🔐 Login / Signup")

    tab1, tab2 = st.tabs(["Login", "Signup"])

    # LOGIN
    with tab1:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if username in users and users[username] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid credentials")

    # SIGNUP
    with tab2:
        new_user = st.text_input("Create Username")
        new_pass = st.text_input("Create Password", type="password")

        if st.button("Signup"):
            if new_user in users:
                st.warning("User already exists")
            else:
                users[new_user] = new_pass
                save_users(users)
                st.success("Account created! Please login")

# ---------------- MAIN APP ----------------
else:

    # SIDEBAR
    st.sidebar.success(f"👋 {st.session_state.username}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    st.markdown("<div class='title'>🎵 Neural Harmony Generator</div>", unsafe_allow_html=True)
    st.markdown("### Create AI-generated music from emotions")

    # ---------------- EMOTION MAP ----------------
    emotion_music = {
        "Happy": [440, 550, 660],
        "Sad": [220, 261, 329],
        "Calm": [330, 392, 440],
        "Angry": [500, 600, 700],
        "Focused": [400, 480, 520],
        "Fearful": [180, 200, 220]
    }

    emotion_icons = {
        "Happy": "😊",
        "Sad": "😢",
        "Calm": "😌",
        "Angry": "😠",
        "Focused": "🧠",
        "Fearful": "😨"
    }

    col1, col2 = st.columns(2)

    with col1:
        selected_emotion = st.selectbox("🎭 Select Emotion", list(emotion_music.keys()))

    with col2:
        st.markdown("### 🎧 Experience AI-generated music instantly")

    st.write(f"Selected Emotion: {emotion_icons[selected_emotion]} {selected_emotion}")

    # ---------------- MUSIC GENERATOR ----------------
    def generate_music(freqs, duration=4, sample_rate=44100):
        t = np.linspace(0, duration, int(sample_rate * duration))
        audio = np.zeros_like(t)

        for f in freqs:
            audio += np.sin(2 * np.pi * f * t)

        audio = audio / len(freqs)
        return (audio * 32767).astype(np.int16)

    # ---------------- GENERATE ----------------
    if st.button("🎼 Generate Music"):

        with st.spinner("Generating AI music... 🎶"):

            progress = st.progress(0)
            for i in range(100):
                progress.progress(i + 1)

            audio_data = generate_music(emotion_music[selected_emotion])

            temp_file = tempfile.NamedTemporaryFile(delete=False, suffix=".wav")
            wavfile.write(temp_file.name, 44100, audio_data)

            st.audio(temp_file.name)

            with open(temp_file.name, "rb") as f:
                st.download_button(
                    "⬇ Download Music",
                    f,
                    file_name="neural_harmony.wav"
                )

            st.success(f"{selected_emotion} music generated successfully!")
