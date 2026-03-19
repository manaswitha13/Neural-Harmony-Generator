import streamlit as st
import requests
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# -------------------- CONFIG --------------------
st.set_page_config(
    page_title="Neural Harmony Generator",
    page_icon="🎵",
    layout="wide"
)

# -------------------- CUSTOM UI --------------------
st.markdown("""
    <style>
    .main {
        background-color: #0e1117;
        color: white;
    }
    .stButton>button {
        background-color: #ff4b4b;
        color: white;
        border-radius: 10px;
        height: 3em;
        width: 100%;
    }
    </style>
""", unsafe_allow_html=True)

# -------------------- AUTH --------------------
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# -------------------- LOGIN --------------------
st.title("🔐 Login")
authenticator.login()

name = st.session_state.get("name")
authentication_status = st.session_state.get("authentication_status")

# -------------------- MAIN --------------------
if authentication_status:

    authenticator.logout("Logout", "sidebar")
    st.success(f"Welcome {name} 👋")

    st.title("🎵 Neural Harmony Generator")
    st.subheader("Create AI-generated music from emotions")

    # -------------------- EMOTIONS --------------------
    emotion_music = {
        "Happy": "upbeat cheerful piano and guitar music",
        "Sad": "slow emotional violin and piano music",
        "Calm": "relaxing meditation flute music",
        "Angry": "fast intense drum and electric guitar music",
        "Focused": "lofi study music with soft beats",
        "Fearful": "dark suspense cinematic music"
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
        selected_emotion = st.selectbox(
            "🎭 Select Emotion",
            list(emotion_music.keys())
        )

    with col2:
        st.markdown("### 🎧 Experience AI-generated music instantly")

    st.write(f"Selected Emotion: {emotion_icons[selected_emotion]} {selected_emotion}")

    # -------------------- HUGGING FACE API --------------------
    API_URL = "https://api-inference.huggingface.co/models/facebook/musicgen-small"
    HEADERS = {"Authorization": "Bearer YOUR_HF_TOKEN"}  # 🔑 replace this

    def generate_music(prompt):
        response = requests.post(
            API_URL,
            headers=HEADERS,
            json={"inputs": prompt}
        )
        return response.content

    # -------------------- GENERATE --------------------
    if st.button("🎼 Generate Music"):

        with st.spinner("Generating music... 🎶"):

            audio_bytes = generate_music(emotion_music[selected_emotion])

            with open("output.wav", "wb") as f:
                f.write(audio_bytes)

            st.audio("output.wav")

            with open("output.wav", "rb") as f:
                st.download_button(
                    "⬇ Download Music",
                    f,
                    file_name="neural_harmony.wav"
                )

            st.success(f"{selected_emotion} music generated successfully!")

elif authentication_status == False:
    st.error("❌ Incorrect Username or Password")

elif authentication_status == None:
    st.warning("⚠️ Please enter your login credentials")
