
import json
import matplotlib.pyplot as plt

def load_zones(path='zones.json'):
    with open(path,'r') as f:
        zones = json.load(f)
    return zones

def compute_proximity_score(zones, asset_pos):
    # zones: list of dict with lat,lon, radius_m, severity
    # asset_pos: dict with lat, lon
    # score is min normalized distance-weighted severity
    import math
    lat0, lon0 = asset_pos['lat'], asset_pos['lon']
    scores = []
    for z in zones:
        # rough equirectangular approx (not for production)
        dx = (z['lon'] - lon0) * 111320 * math.cos(lat0*math.pi/180)
        dy = (z['lat'] - lat0) * 110574
        dist = math.hypot(dx, dy)
        norm = max(0.0, 1.0 - dist / (z['radius_m'] + 1.0))
        scores.append(norm * z.get('severity',1.0))
    # return aggregated proximity score between 0-1
    return min(1.0, sum(scores)/len(scores) if scores else 0.0)

def plot_zones_map(zones, asset_pos):
    # Simple matplotlib scatter representing zones and the asset
    fig, ax = plt.subplots(figsize=(4,4))
    lats = [z['lat'] for z in zones]
    lons = [z['lon'] for z in zones]
    radii = [z['radius_m']/1000.0 for z in zones]
    for z in zones:
        circle = plt.Circle((z['lon'], z['lat']), z['radius_m']/100000.0, alpha=0.2)
        ax.add_patch(circle)
        ax.text(z['lon'], z['lat'], z['name'], fontsize=8)
    ax.scatter([asset_pos['lon']],[asset_pos['lat']], c='red', s=40)
    ax.set_xlabel('Longitude'); ax.set_ylabel('Latitude')
    ax.set_title('Mock geo-zones (not to scale)')
    ax.set_xlim(min(lons)-0.02, max(lons)+0.02)
    ax.set_ylim(min(lats)-0.02, max(lats)+0.02)
    return fig
