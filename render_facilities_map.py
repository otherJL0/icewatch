#!/usr/bin/env python3
"""
Render a static HTML map of facilities using Leaflet.js.
Popups show name, address, and rounded criminal/non-criminal counts.
"""
import json
import argparse
from pathlib import Path
from math import isnan

def load_facilities(path):
    with open(path, 'r', encoding='utf-8') as f:
        data = json.load(f)
    return data.get('facilities', [])

def safe_int(val):
    try:
        if val is None or (isinstance(val, float) and isnan(val)):
            return 0
        return int(round(float(val)))
    except Exception:
        return 0

def make_popup(fac):
    name = fac.get('Name', 'Unknown')
    addr = fac.get('Address', '')
    city = fac.get('City', '')
    state = fac.get('State', '')
    zipc = fac.get('Zip', '')
    criminals = safe_int(fac.get('Male Crim')) + safe_int(fac.get('Female Crim'))
    noncriminals = safe_int(fac.get('Male Non-Crim')) + safe_int(fac.get('Female Non-Crim'))
    total = criminals + noncriminals
    if total > 0:
        pct_criminal = f"{round(100 * criminals / total)}%"
    else:
        pct_criminal = "N/A"
    lines = [
        f'<b>{name}</b>',
        f'{addr}, {city}, {state} {zipc}',
        f'Criminals: <b>{criminals}</b>',
        f'Non-Criminals: <b>{noncriminals}</b>',
        f'Percentage Criminal: <b>{pct_criminal}</b>'
    ]
    return '<br/>'.join(lines)

def render_html(facilities, output_path):
    # Center on US
    center_lat, center_lon = 39.8283, -98.5795
    html = f'''<!DOCTYPE html>
<html>
<head>
    <meta charset="utf-8" />
    <title>ICE Facilities Map</title>
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <style>
        html, body {{
            margin: 0;
            padding: 0;
            font-family: system-ui, sans-serif;
            background: #f8f9fa;
            height: 100%;
        }}
        body {{
            min-height: 100vh;
            display: flex;
            flex-direction: column;
        }}
        #header-bar {{
            display: flex;
            align-items: center;
            justify-content: space-between;
            background: #f5f5f5;
            color: #222;
            padding: 0.5em 1.5em;
            height: 64px;
            border-bottom: 1px solid #e0e0e0;
            flex-shrink: 0;
        }}
        #header-title {{
            font-size: 2em;
            font-weight: 700;
            letter-spacing: 0.01em;
            color: #222;
        }}
        #donate-link {{
            background: #ff5a1f;
            color: #fff;
            text-decoration: none;
            padding: 0.5em 1.2em;
            border-radius: 24px;
            font-weight: 600;
            font-size: 1em;
            transition: background 0.2s;
            border: none;
        }}
        #donate-link:hover {{
            background: #e04a13;
        }}
        #map {{
            flex: 1 1 auto;
            height: 100%;
            width: 100vw;
        }}
        #footer-bar {{
            display: flex;
            flex-direction: column;
            align-items: center;
            justify-content: center;
            background: #f5f5f5;
            color: #222;
            padding: 1.5em 0 1em 0;
            border-top: 1px solid #e0e0e0;
            flex-shrink: 0;
        }}
        #footer-logo {{
            height: 80px;
            width: auto;
            margin-bottom: 0.5em;
        }}
        @media (max-width: 600px) {{
            #header-bar {{ flex-direction: column; height: auto; padding: 1em; }}
            #header-title {{ font-size: 1.3em; }}
            #map {{ height: 70vh; }}
            #footer-logo {{ height: 48px; }}
        }}
    </style>
</head>
<body>
    <div id="header-bar">
        <div id="header-title">ICE Custody Data</div>
        <a id="donate-link" href="https://opencollective.com/lockdown-systems" target="_blank" rel="noopener">Donate</a>
    </div>
    <div id="map"></div>
    <div id="footer-bar">
        <a href="https://lockdown.systems/" target="_blank" rel="noopener">
            <img id="footer-logo" src="img/logo-wide.svg" alt="Lockdown Systems logo" />
        </a>
    </div>
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <script>
    var map = L.map('map').setView([{center_lat}, {center_lon}], 4);
    L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
        maxZoom: 18,
        attribution: '© OpenStreetMap contributors'
    }}).addTo(map);
    '''
    for fac in facilities:
        lat = fac.get('latitude')
        lon = fac.get('longitude')
        if lat is None or lon is None:
            continue
        popup = make_popup(fac).replace("'", "&#39;").replace("\n", " ")
        html += f"""
    L.marker([{lat}, {lon}]).addTo(map)
        .bindPopup('{popup}');
    """
    html += """
    </script>
</body>
</html>
"""
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    print(f"Map written to: {output_path}")

def main():
    parser = argparse.ArgumentParser(description="Render a static HTML map of facilities.")
    parser.add_argument('--input', required=True, help='Input geocoded facilities JSON file')
    parser.add_argument('--output', help='Output HTML file (default: docs/index.html)')
    args = parser.parse_args()
    input_path = Path(args.input)
    if args.output:
        output_path = args.output
    else:
        output_path = Path('docs/index.html')
    # Ensure the output directory exists
    Path(output_path).parent.mkdir(parents=True, exist_ok=True)
    facilities = load_facilities(input_path)
    render_html(facilities, output_path)

if __name__ == "__main__":
    main()