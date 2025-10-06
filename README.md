# AquaSentinel — LiDAR + Sonar + AI for Underwater Domain Awareness

**Project name:** AquaSentinel — LiDAR + Sonar + AI for Underwater Domain Awareness 

## Goals
AquaSentinel is a hackathon-ready scaffold demonstrating a lightweight prototype for fusing acoustic (sonar-like) signal detection with LiDAR/geospatial proximity context to produce simple risk alerts for underwater threats (e.g., divers, UUVs, small craft). This repository is intended for demo and research use only — **not** for operational deployment without proper testing, validation, and approvals.

## Structure
```
AquaSentinel/
├─ app.py                   # Streamlit demo dashboard
├─ audio_pipeline.py        # STFT feature extraction and simple detection logic
├─ lidar_context.py         # Mock LiDAR/geo proximity context & scoring
├─ fusion.py                # Risk scoring combining detection, SNR, proximity
├─ sample_audio.wav         # Synthetic ambient + motor-like audio sample (10s)
├─ zones.json               # Mock geo-zones for proximity scoring
├─ architecture.png         # Simple architecture diagram (matplotlib-generated)
├─ README.md                # This file
└─ requirements.txt         # Suggested Python packages
```

## Quickstart (local)
1. Create a Python virtual environment and install dependencies:
```bash
python -m venv venv
source venv/bin/activate      # or venv\Scripts\activate on Windows
pip install -r requirements.txt
```
2. Run the Streamlit demo:
```bash
streamlit run app.py
```
3. The demo will display the spectrogram (from `sample_audio.wav`), a mock geo-map with zones, and a risk alert panel computed by `fusion.py`.


## Extending the project (ideas)
- Replace mock LiDAR with real point-cloud ingestion and occupancy detection.
- Integrate ML-based acoustic classifiers (CNNs on spectrograms) and calibrate with labeled data.
- Add temporal tracking and sensor fusion with Kalman filters or particle filters.
- Implement secure logging, authentication, and role-based access controls for operators.


