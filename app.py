import streamlit as st
import torch
from transformers import MusicgenForConditionalGeneration, AutoProcessor
import scipy.io.wavfile
import numpy as np

# --- Page Config ---
st.set_page_config(page_title="Neural Harmony Generator", page_icon="🎵")

# --- Optimized Model Loading ---
@st.cache_resource
def load_music_model():
    # Using 'small' for speed during the live demo
    model = MusicgenForConditionalGeneration.from_pretrained("facebook/musicgen-small")
    processor = AutoProcessor.from_pretrained("facebook/musicgen-small")
    return model, processor

# --- Dictionary ---
emotion_music = {
    "Happy": "upbeat cheerful piano and guitar music",
    "Sad": "slow emotional violin and piano music",
    "Calm": "relaxing meditation flute music",
    "Angry": "fast intense drum and electric guitar music",
    "Focused": "lofi study music with soft beats",
    "Fearful": "dark suspense cinematic music"
}

st.title("🎵 Neural Harmony Generator")

selected_emotion = st.selectbox("Select an emotion", list(emotion_music.keys()))

if st.button("Generate Music"):
    model, processor = load_music_model()
    
    with st.spinner(f"AI is composing a {selected_emotion} track..."):
        # 1. Prepare the input
        inputs = processor(
            text=[emotion_music[selected_emotion]],
            padding=True,
            return_tensors="pt",
        )

        # 2. Generate Audio (approx 10 seconds)
        # max_new_tokens=512 roughly equals 10 seconds of audio
        audio_values = model.generate(**inputs, max_new_tokens=512)

        # 3. Post-process to WAV
        sampling_rate = model.config.audio_encoder.sampling_rate
        audio_data = audio_values[0, 0].cpu().numpy()

        # 4. Save and Play
        output_filename = "neural_harmony.wav"
        scipy.io.wavfile.write(output_filename, rate=sampling_rate, data=audio_data)
        
        st.audio(output_filename)
        st.success(f"Successfully generated {selected_emotion} music!")