import streamlit as st
import torch
from transformers import MusicgenForConditionalGeneration, AutoProcessor
import scipy.io.wavfile
import numpy as np
import streamlit_authenticator as stauth
import yaml
from yaml.loader import SafeLoader

# -------------------- PAGE CONFIG --------------------
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

# -------------------- AUTHENTICATION --------------------
with open('config.yaml') as file:
    config = yaml.load(file, Loader=SafeLoader)

authenticator = stauth.Authenticate(
    config['credentials'],
    config['cookie']['name'],
    config['cookie']['key'],
    config['cookie']['expiry_days']
)

# ✅ FIXED LOGIN
name, authentication_status, username = authenticator.login("Login", "main")

# -------------------- AUTH LOGIC --------------------
if authentication_status:

    authenticator.logout("Logout", "sidebar")
    st.sidebar.title("🎵 Neural Harmony")
    st.sidebar.info("AI-powered music generation based on emotions")

    st.success(f"Welcome {name} 👋")

    # -------------------- MODEL LOADING --------------------
    @st.cache_resource
    def load_music_model():
        model = MusicgenForConditionalGeneration.from_pretrained(
            "facebook/musicgen-small",
            torch_dtype=torch.float32
        )
        processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
        return model, processor

    # -------------------- EMOTION MAP --------------------
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

    # -------------------- UI --------------------
    st.title("🎵 Neural Harmony Generator")
    st.subheader("Create AI-generated music from emotions")

    col1, col2 = st.columns(2)

    with col1:
        selected_emotion = st.selectbox(
            "🎭 Select Emotion",
            list(emotion_music.keys())
        )

    with col2:
        st.markdown("### 🎧 Experience AI-generated music instantly")

    st.write(f"Selected Emotion: {emotion_icons[selected_emotion]} {selected_emotion}")

    # -------------------- GENERATE --------------------
    if st.button("🎼 Generate Music"):

        model, processor = load_music_model()

        with st.spinner(f"AI is composing {selected_emotion} music..."):

            progress = st.progress(0)
            for i in range(100):
                progress.progress(i + 1)

            inputs = processor(
                text=[emotion_music[selected_emotion]],
                padding=True,
                return_tensors="pt",
            )

            with torch.no_grad():
                audio_values = model.generate(**inputs, max_new_tokens=256)

            sampling_rate = model.config.audio_encoder.sampling_rate
            audio_data = audio_values[0, 0].cpu().numpy()

            output_filename = "neural_harmony.wav"
            scipy.io.wavfile.write(output_filename, sampling_rate, audio_data)

            st.audio(output_filename)

            with open(output_filename, "rb") as file:
                st.download_button(
                    "⬇ Download Music",
                    file,
                    file_name="neural_harmony.wav"
                )

            st.success(f"{selected_emotion} music generated successfully!")

elif authentication_status == False:
    st.error("❌ Incorrect Username or Password")

elif authentication_status == None:
    st.warning("⚠️ Please enter your login credentials")