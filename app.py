
import streamlit as st
import numpy as np
import matplotlib.pyplot as plt
from scipy.io import wavfile
from audio_pipeline import compute_spectrogram, detect_activity, compute_snr_db
from lidar_context import load_zones, compute_proximity_score, plot_zones_map
from fusion import score_risk

st.set_page_config(layout="wide", page_title="AquaSentinel Dashboard")

st.title("AquaSentinel — Underwater Domain Awareness (Demo)")

col1, col2 = st.columns([2,1])

with col1:
    st.header("Acoustic Spectrogram and Detection")
    st.text("Using synthetic `sample_audio.wav`")
    sr, audio = wavfile.read("sample_audio.wav")
    audio = audio.astype(float) / 32768.0
    f, t, Sxx_db = compute_spectrogram(audio, sr)
    fig, ax = plt.subplots(figsize=(8,3))
    im = ax.pcolormesh(t, f, Sxx_db, shading='gouraud')
    ax.set_ylabel('Freq [Hz]'); ax.set_xlabel('Time [sec]')
    ax.set_title('Spectrogram (dB)')
    fig.colorbar(im, ax=ax, format='%+2.0f dB')
    st.pyplot(fig)

    snr_db = compute_snr_db(audio, sr)
    st.metric("Estimated audio SNR (dB)", f"{snr_db:.1f} dB")

    detected = detect_activity(Sxx_db, f, t)
    st.write("Detection summary (simple threshold-based):")
    st.write(detected)

with col2:
    st.header("Geo Context & Risk Alerts")
    zones = load_zones("zones.json")
    # mock current asset position
    asset_pos = {"lat": 12.95, "lon": 77.60}
    st.write("Asset position:", asset_pos)
    fig2 = plot_zones_map(zones, asset_pos)
    st.pyplot(fig2)

    proximity_score = compute_proximity_score(zones, asset_pos)
    st.metric("Proximity score", f"{proximity_score:.2f}")

    final = score_risk(detected, snr_db, proximity_score)
    st.header("Risk Score & Alert")
    st.subheader(f"Risk score: {final['risk_score']:.2f}  — Level: {final['level']}")
    if final['level'] in ('HIGH','CRITICAL'):
        st.error(final['message'])
    elif final['level']=='MEDIUM':
        st.warning(final['message'])
    else:
        st.success(final['message'])

    st.markdown('''---
    **Notes:** This demo uses mocked sensors and very simple fusion logic for illustration only.
    ''')
