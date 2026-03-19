import streamlit as st
import numpy as np
import scipy.io.wavfile as wavfile
import tempfile

# ---------------- PAGE CONFIG ----------------
st.set_page_config(
    page_title="Neural Harmony Generator",
    page_icon="🎵",
    layout="wide"
)

# ---------------- SESSION STATE ----------------
if "users" not in st.session_state:
    st.session_state.users = {}

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "username" not in st.session_state:
    st.session_state.username = ""

# ---------------- CUSTOM UI ----------------
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: white;
    }
    .title {
        font-size: 40px;
        font-weight: bold;
        text-align: center;
    }
    .stButton>button {
        background-color: #ff4b4b;
        color: white;
        border-radius: 10px;
        height: 3em;
        width: 100%;
        font-size: 16px;
    }
    </style>
""", unsafe_allow_html=True)

# ---------------- AUTH SYSTEM ----------------
if not st.session_state.logged_in:

    st.markdown("<div class='title'>🔐 Login / Signup</div>", unsafe_allow_html=True)

    tab1, tab2 = st.tabs(["Login", "Signup"])

    # ---------- LOGIN ----------
    with tab1:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")

        if st.button("Login"):
            if username in st.session_state.users and st.session_state.users[username] == password:
                st.session_state.logged_in = True
                st.session_state.username = username
                st.success("Login successful!")
                st.rerun()
            else:
                st.error("Invalid credentials")

    # ---------- SIGNUP ----------
    with tab2:
        new_user = st.text_input("Create Username")
        new_pass = st.text_input("Create Password", type="password")

        if st.button("Signup"):
            if new_user in st.session_state.users:
                st.warning("User already exists")
            else:
                st.session_state.users[new_user] = new_pass
                st.success("Account created! Please login")

# ---------------- MAIN APP ----------------
else:

    # Logout button
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    st.title("🎵 Neural Harmony Generator")
    st.subheader(f"Welcome {st.session_state.username} 👋")

    # ---------------- EMOTION MAP ----------------
    emotion_music = {
        "Happy": 440,
        "Sad": 220,
        "Calm": 330,
        "Angry": 550,
        "Focused": 400,
        "Fearful": 180
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

    # ---------------- AUDIO FUNCTION ----------------
    def generate_music(freq, duration=3, sample_rate=44100):
        t = np.linspace(0, duration, int(sample_rate * duration))
        audio = 0.5 * np.sin(2 * np.pi * freq * t)
        return (audio * 32767).astype(np.int16)

    # ---------------- GENERATE BUTTON ----------------
    if st.button("🎼 Generate Music"):

        with st.spinner("Generating music... 🎶"):

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
