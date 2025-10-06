
import numpy as np
from scipy.signal import stft, windows

def compute_spectrogram(audio, sr, nperseg=1024, noverlap=512):
    # mono audio expected as 1-D numpy array
    f, t, Zxx = stft(audio, fs=sr, window='hann', nperseg=nperseg, noverlap=noverlap)
    Sxx = np.abs(Zxx)
    # convert to dB (log)
    Sxx_db = 20 * np.log10(Sxx + 1e-12)
    return f, t, Sxx_db

def detect_activity(Sxx_db, f, t, band=(50, 2000), db_threshold=-40, occupancy_threshold=0.02):
    # Simple rule-based detector:
    # - Look for sustained energy above threshold in a frequency band
    idx = (f >= band[0]) & (f <= band[1])
    band_energy = Sxx_db[idx, :]
    active_frames = (band_energy > db_threshold).sum(axis=0) / band_energy.shape[0]
    active_ratio = (active_frames > 0.05).sum() / len(active_frames)
    detected = {
        'active_ratio': float(active_ratio),
        'band': band,
        'db_threshold': db_threshold,
        'occupancy_ratio': float(active_frames.mean()),
        'suspicious': active_ratio > occupancy_threshold
    }
    return detected

def compute_snr_db(audio, sr, signal_band=(100,1500)):
    # Very rough SNR estimator: ratio of band energy to out-of-band energy
    from scipy.signal import butter, filtfilt
    b, a = butter(4, [signal_band[0]/(0.5*sr), signal_band[1]/(0.5*sr)], btype='band')
    try:
        signal = filtfilt(b, a, audio)
    except Exception:
        signal = audio
    power_signal = np.mean(signal**2)
    power_total = np.mean(audio**2) + 1e-12
    snr = 10 * np.log10(power_signal / (power_total - power_signal + 1e-12) + 1e-12)
    return float(snr)
