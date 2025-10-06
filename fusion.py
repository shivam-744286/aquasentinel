
def score_risk(detected, snr_db, proximity_score):
    # detected: dict from audio pipeline
    # snr_db: float
    # proximity_score: 0-1
    # Simple weighted scoring
    activity_weight = 0.5
    snr_weight = 0.2
    proximity_weight = 0.3

    activity_score = min(1.0, detected.get('active_ratio',0.0) * 5.0)
    snr_score = max(0.0, min(1.0, (snr_db + 30.0) / 60.0))  # map -30..30 dB to 0..1
    prox_score = float(proximity_score)

    risk_score = activity_weight*activity_score + snr_weight*snr_score + proximity_weight*prox_score
    level = 'LOW'
    msg = 'No immediate risk detected.'
    if risk_score > 0.75:
        level = 'CRITICAL'; msg = 'High-confidence threat indicators. Immediate attention required.'
    elif risk_score > 0.5:
        level = 'HIGH'; msg = 'Suspicious acoustic activity with concerning proximity.'
    elif risk_score > 0.25:
        level = 'MEDIUM'; msg = 'Elevated activity — monitor and collect more data.'

    return {'risk_score': risk_score, 'level': level, 'message': msg, 'components': {'activity':activity_score, 'snr':snr_score, 'proximity':prox_score}}
