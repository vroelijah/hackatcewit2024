import io
import streamlit as st
from st_audiorec import st_audiorec
import numpy as np
import librosa
import json
import subprocess
import os
from sklearn.ensemble import RandomForestClassifier
import joblib

st.set_page_config(page_title="Audilert")
st.markdown('''<style>.css-1egvi7u {margin-top: -3rem;}</style>''', unsafe_allow_html=True)
st.markdown('''<style>.stAudio {height: 45px;}</style>''', unsafe_allow_html=True)
st.markdown('''<style>.css-v37k9u a {color: #ff4c4b;}</style>''', unsafe_allow_html=True)
st.markdown('''<style>.css-nlntq9 a {color: #ff4c4b;}</style>''', unsafe_allow_html=True)

def extract_features(audio_data):
    y, sr = librosa.load(io.BytesIO(audio_data), sr=None)
    mfccs = librosa.feature.mfcc(y=y, sr=sr, n_mfcc=13)
    feature_vector = np.mean(mfccs, axis=1)
    return feature_vector

def predict_audio_label(wav_audio_data):
    # Load your pre-trained model here (ensure the model is saved in the same directory or specify the correct path)
    model = joblib.load('path_to_your_pretrained_model.pkl')
    
    # Assuming you have a mapping from labels to IDs
    label_to_id = {"label1": "ID1", "label2": "ID2", ...}  # Fill in your actual labels and corresponding IDs

    if wav_audio_data is not None:
        features = extract_features(wav_audio_data)
        predicted_label = model.predict([features])[0]
        audio_id = label_to_id.get(predicted_label, "Unknown ID")  # Get ID from label, default to "Unknown ID" if not found
        return audio_id, predicted_label
    return "Unknown ID", "No audio data"

def audiorec_demo_app():
    st.title('Audilert Sound Recorder')
    st.write('\n\n')

    wav_audio_data = st_audiorec()

    col_info, col_space = st.columns([0.57, 0.43])
    with col_info:
        st.write('\n')
        st.write('\n')

    if wav_audio_data is not None:
        col_playback, col_space = st.columns([0.58,0.42])
        with(col_playback):
            st.audio(wav_audio_data, format='audio/wav')

    audio_id, diagnosis = predict_audio_label(wav_audio_data)

    st.subheader(f"Diagnosis: {diagnosis}")
    # Pass both audio_id and diagnosis to push.py
    subprocess.Popen(['python', 'push.py', audio_id, diagnosis])

if __name__ == '__main__':
    audiorec_demo_app()
