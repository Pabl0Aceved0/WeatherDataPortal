import os
import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template_string, request, send_from_directory

# Load environment variables from .env file
# This should be done early in your application's lifecycle
load_dotenv()

# Get the API tokens
WINDY_API_TOKEN = os.getenv("WINDY_API_TOKEN")
WINDY_API_TOKEN_MAP = os.getenv("WINDY_API_TOKEN_MAP")
WINDY_API_TOKEN_POINT = os.getenv("WINDY_API_TOKEN_POINT")
WINDY_API_TOKEN_WEBCAMS = os.getenv("WINDY_API_TOKEN_WEBCAMS")

if not all([WINDY_API_TOKEN_MAP, WINDY_API_TOKEN_POINT, WINDY_API_TOKEN_WEBCAMS]):
    print("CRITICAL: One or more API tokens are not set. Please check your .env file.")

# Debugging statement to verify token loading
print("Debug: Loaded WINDY_API_TOKEN:", WINDY_API_TOKEN[:4] + "..." if WINDY_API_TOKEN else "None")
print("Debug: Loaded WINDY_API_TOKEN_MAP:", WINDY_API_TOKEN_MAP[:4] + "..." if WINDY_API_TOKEN_MAP else "None")
print("Debug: Loaded WINDY_API_TOKEN_POINT:", WINDY_API_TOKEN_POINT[:4] + "..." if WINDY_API_TOKEN_POINT else "None")
print("Debug: Loaded WINDY_API_TOKEN_WEBCAMS:", WINDY_API_TOKEN_WEBCAMS[:4] + "..." if WINDY_API_TOKEN_WEBCAMS else "None")

# Set static_folder to the correct absolute path
STATIC_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'static'))
app = Flask(__name__, static_folder=STATIC_DIR, static_url_path='/static')

def fetch_real_windy_data(lat=50.4, lon=14.3):
    """Fetch real weather data from Windy Point Forecast API"""
    if not WINDY_API_TOKEN_POINT:
        print("Error: WINDY_API_TOKEN_POINT not configured.")
        return None

    try:
        # Windy Point Forecast API
        url = "https://api.windy.com/api/point-forecast/v2"
        headers = {
            "Content-Type": "application/json"
        }
        
        payload = {
            "lat": lat,
            "lon": lon,
            "model": "gfs",
            "parameters": ["wind", "temp", "dewpoint", "rh", "pressure", "precip"],
            "levels": ["surface"],
            "key": WINDY_API_TOKEN_POINT
        }
        
        print(f"Debug: Making Windy API request for lat={lat}, lon={lon}")
        response = requests.post(url, json=payload, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            print("Debug: Successfully fetched Windy data")
            
            # Parse the data
            if 'data' in data and data['data']:
                current_data = {}
                ts = data['data'][0]['hours']
                if ts and len(ts) > 0:
                    # Get the first (current) time entry
                    current_time = list(ts.keys())[0]
                    current_values = ts[current_time]
                    
                    current_data = {
                        "temperature": current_values.get('temp', 'N/A'),
                        "wind_speed": current_values.get('wind_u', 'N/A'),
                        "pressure": current_values.get('pressure', 'N/A'),
                        "humidity": current_values.get('rh', 'N/A'),
                        "precipitation": current_values.get('precip', 'N/A'),
                        "location": f"Lat: {lat}, Lon: {lon}",
                        "timestamp": current_time,
                        "source": "Windy Point Forecast API"
                    }
                return current_data
            else:
                print("Debug: No data in Windy response")
                return None
                
        else:
            print(f"Debug: Windy API error - Status: {response.status_code}, Response: {response.text}")
            return None
            
    except requests.RequestException as e:
        print(f"Debug: Request error: {e}")
        return None
    except Exception as e:
        print(f"Debug: General error: {e}")
        return None

def fetch_windy_webcams(lat=50.4, lon=14.3, radius=50):
    """Fetch nearby webcams from Windy Webcams API"""
    if not WINDY_API_TOKEN_WEBCAMS:
        print("Error: WINDY_API_TOKEN_WEBCAMS not configured.")
        return []

    try:
        url = f"https://api.windy.com/api/webcams/v2/list/nearby={lat},{lon},{radius}"
        headers = {
            "x-windy-api-key": WINDY_API_TOKEN_WEBCAMS
        }
        
        print(f"Debug: Fetching webcams near lat={lat}, lon={lon}")
        response = requests.get(url, headers=headers, timeout=10)
        
        if response.status_code == 200:
            data = response.json()
            webcams = []
            if 'result' in data and 'webcams' in data['result']:
                for webcam in data['result']['webcams'][:3]:  # Limit to 3 webcams
                    webcams.append({
                        "title": webcam.get('title', 'Unknown'),
                        "location": webcam.get('location', {}).get('city', 'Unknown'),
                        "image": webcam.get('image', {}).get('current', {}).get('preview', ''),
                        "url": webcam.get('url', {}).get('current', {}).get('desktop', '#')
                    })
            return webcams
        else:
            print(f"Debug: Webcam API error - Status: {response.status_code}")
            return []
            
    except Exception as e:
        print(f"Debug: Webcam fetch error: {e}")
        return []

def get_climate_insights(weather_data):
    """Generate 8-bit style climate insights based on weather data"""
    temp = weather_data.get('temperature', 0)
    pressure = weather_data.get('pressure', 1013)
    humidity = weather_data.get('humidity', 50)
    
    insights = []
    
    # Temperature insights
    if temp < 0:
        insights.append("❄️ FREEZE WARNING: Sub-zero temperatures detected!")
    elif temp < 10:
        insights.append("🧊 COLD ALERT: Bundle up for chilly conditions!")
    elif temp > 30:
        insights.append("🔥 HEAT ADVISORY: High temperature conditions!")
    elif 18 <= temp <= 25:
        insights.append("🌟 PERFECT CLIMATE: Optimal comfort zone achieved!")
    
    # Pressure insights
    if pressure < 1000:
        insights.append("📉 LOW PRESSURE: Storm system possible!")
    elif pressure > 1020:
        insights.append("📈 HIGH PRESSURE: Clear skies likely!")
    
    # Humidity insights
    if humidity > 80:
        insights.append("💧 HIGH HUMIDITY: Muggy conditions detected!")
    elif humidity < 30:
        insights.append("🏜️ DRY AIR: Low humidity levels!")
    
    if not insights:
        insights.append("🌤️ STABLE CONDITIONS: Weather systems normal!")
    
    return insights

def fetch_weather_data(lat=50.4, lon=14.3):
    """Fetch weather data - try real API first, fallback to placeholder"""
    # Try to get real data from Windy
    real_data = fetch_real_windy_data(lat, lon)
    if real_data:
        return real_data
    
    # Fallback to placeholder data
    print("Debug: Using placeholder data")
    return {
        "temperature": 25, 
        "condition": "Sunny (Placeholder)", 
        "location": f"Lat: {lat}, Lon: {lon}",
        "source": "Placeholder Data"
    }

@app.route('/')
def index():
    print("Debug: Entered index route")
    lat = request.args.get('lat', 50.4, type=float)
    lon = request.args.get('lon', 14.3, type=float)
    weather = fetch_weather_data(lat, lon)
    climate_insights = get_climate_insights(weather) if weather else []
    windy_map_url = f"https://embed.windy.com/embed2.html?lat={lat}&lon={lon}&detailLat={lat}&detailLon={lon}&width=100%25&height=500&zoom=8&level=surface&overlay=wind&product=ecmwf&menu=&message=true&marker=true&calendar=now&pressure=&type=map&location=coordinates&detail=&metricWind=default&metricTemp=default&radarRange=-1"
    if WINDY_API_TOKEN_MAP:
        windy_map_url += f"&key={WINDY_API_TOKEN_MAP}"
    insights_html = ''.join([f'<li>{insight}</li>' for insight in climate_insights])
    # To avoid f-string brace issues, use doubled braces in JS and CSS blocks
    return f"""
    <!DOCTYPE html>
    <html lang='en'>
    <head>
        <meta charset='UTF-8'>
        <meta name='viewport' content='width=device-width, initial-scale=1.0'>
        <title>Weather Power Portal</title>
        <meta name='theme-color' content='#0077be'>
        <link rel='manifest' href='/static/manifest.json'>
        <link rel='icon' href='https://www.windy.com/img/logo/logo-windy-192.png'>
        <meta property='og:title' content='Windy.com Map Portal'>
        <meta property='og:description' content='Mobile-friendly weather portal with interactive Windy.com map and real-time weather data.'>
        <meta property='og:image' content='https://www.windy.com/img/logo/logo-windy-512.png'>
        <meta property='og:type' content='website'>
        <meta name='apple-mobile-web-app-capable' content='yes'>
        <meta name='apple-mobile-web-app-status-bar-style' content='black-translucent'>
        <meta name='apple-mobile-web-app-title' content='WindyMap'>
        <style>
            :root {{
                --primary: #0057b8;
                --secondary: #00bfae;
                --accent: #ff9800;
                --background: transparent;
                --surface: #ffffffcc;
                --text: #222831;
                --muted: #6c757d;
                --border: #e0e6ed;
                --shadow: 0 2px 8px rgba(0,0,0,0.07);
            }}
            html, body {{
                height: 100%;
                margin: 0;
                padding: 0;
                font-family: 'Segoe UI', 'Roboto', Arial, sans-serif;
                background: var(--background);
                color: var(--text);
                position: relative;
                min-height: 100vh;
            }}
            .bg-video {{
                position: fixed;
                top: 0; left: 0; width: 100vw; height: 100vh;
                object-fit: cover;
                z-index: -2;
                pointer-events: none;
                filter: contrast(1.1) brightness(1.1) saturate(1.2);
            }}
            .bg-fallback {{
                position: fixed;
                top: 0; left: 0; width: 100vw; height: 100vh;
                background: url('https://i.imgur.com/6QKjvQp.gif') repeat center center;
                background-size: cover;
                z-index: -2;
                pointer-events: none;
                opacity: 0.7;
            }}
            header, .container {{
                background: var(--surface);
                backdrop-filter: blur(2px);
            }}
            header {{
                background: linear-gradient(90deg, var(--primary) 60%, var(--secondary) 100%);
                color: #fff;
                padding: 1.2rem 0 1rem 0;
                text-align: center;
                box-shadow: var(--shadow);
            }}
            h1 {{
                margin: 0 0 0.2em 0;
                font-size: 2.2rem;
                font-weight: 700;
                letter-spacing: 1px;
            }}
            .container {{
                max-width: 480px;
                margin: 1.5rem auto;
                background: var(--surface);
                border-radius: 1.2rem;
                box-shadow: var(--shadow);
                padding: 1.5rem 1.2rem 1.2rem 1.2rem;
            }}
            .weather-info {{
                display: flex;
                flex-direction: column;
                gap: 0.7rem;
                margin-bottom: 1.2rem;
            }}
            .weather-info strong {{
                color: var(--primary);
            }}
            .map-container {{
                width: 100%;
                aspect-ratio: 1.2/1;
                border-radius: 1rem;
                overflow: hidden;
                box-shadow: var(--shadow);
                margin-bottom: 1.2rem;
            }}
            .actions {{
                display: flex;
                gap: 0.7rem;
                justify-content: center;
                margin-top: 1rem;
            }}
            button, .share-btn {{
                background: var(--accent);
                color: #fff;
                border: none;
                border-radius: 2em;
                padding: 0.7em 1.5em;
                font-size: 1.1em;
                font-weight: 600;
                cursor: pointer;
                box-shadow: 0 2px 6px rgba(0,0,0,0.08);
                transition: background 0.2s, transform 0.2s;
            }}
            button:hover, .share-btn:hover {{
                background: var(--secondary);
                transform: translateY(-2px) scale(1.04);
            }}
            .coords {{
                font-size: 1em;
                color: var(--muted);
                margin-bottom: 0.5em;
            }}
            @media (max-width: 600px) {{
                .container {{
                    max-width: 98vw;
                    padding: 1.1rem 0.5rem 1rem 0.5rem;
                }}
                h1 {{
                    font-size: 1.4rem;
                }}
                .map-container {{
                    aspect-ratio: 1/1.1;
                }}
            }}
            .accent-bar {{
                height: 4px;
                width: 100%;
                background: linear-gradient(90deg, var(--accent), var(--secondary));
                animation: accent-move 2.5s linear infinite alternate;
            }}
            @keyframes accent-move {{
                0% {{ filter: brightness(1.1); }}
                100% {{ filter: brightness(1.4); }}
            }}
        </style>
        <script>
          if ('serviceWorker' in navigator) {{
            window.addEventListener('load', function() {{
              navigator.serviceWorker.register('/static/service-worker.js');
            }});
          }}
          function sharePortal() {{
            const shareData = {{
              title: 'Windy.com Map Portal',
              text: 'Check out this interactive weather map!',
              url: window.location.href
            }};
            if (navigator.share) {{
              navigator.share(shareData).catch(function() {{{{}}}});
            }} else {{
              navigator.clipboard.writeText(window.location.href);
              alert('Link copied to clipboard!');
            }}
          }}
        </script>
    </head>
    <body>
        <video class='bg-video' autoplay loop muted playsinline poster='https://i.imgur.com/6QKjvQp.gif'>
            <source src='https://cdn.pixabay.com/video/2023/03/14/156661-810282209_large.mp4' type='video/mp4'>
        </video>
        <div class='bg-fallback'></div>
        <header>
            <h1>Weather Power Portal</h1>
            <div class='accent-bar'></div>
        </header>
        <main>
            <div class='container'>
                <div class='coords'>Lat: {lat:.5f}, Lon: {lon:.5f}</div>
                <div class='map-container'>
                    <iframe id='windy-iframe' src='{windy_map_url}' allowfullscreen title='Windy.com Weather Map'></iframe>
                </div>
                <div class='weather-info'>
                    <div><strong>Temperature:</strong> {weather.get('temperature', 'N/A')} °C</div>
                    <div><strong>Condition:</strong> {weather.get('condition', 'N/A')}</div>
                    <div><strong>Pressure:</strong> {weather.get('pressure', 'N/A')} hPa</div>
                    <div><strong>Humidity:</strong> {weather.get('humidity', 'N/A')}%</div>
                    <div style='color:#666;font-size:0.95em;margin-top:0.7em;'>Source: {weather.get('source', 'Unknown')}</div>
                </div>
                <div class='climate-insights'>
                    <b>Climate Insights:</b>
                    <ul style='margin:0.5em 0 0 1.2em;padding:0;'>
                        {insights_html}
                    </ul>
                </div>
                <div class='actions'>
                    <button onclick='window.location.reload()'>Refresh</button>
                    <button class='share-btn' onclick='sharePortal()'>Share</button>
                    <button onclick='getLocation()' style='background:var(--secondary);color:#fff;'>Use My Location</button>
                    <button onclick='enablePickMode()' style='background:var(--primary);color:#fff;'>Pick Location on Map</button>
                </div>
            </div>
        </main>
        <div class='footer'>
            &copy; 2025 Windy.com | <a href='https://www.w3schools.com/html/html_responsive.asp' target='_blank'>Responsive Design Info</a>
        </div>
        <script>
        function getLocation() {{
            if (navigator.geolocation) {{
                navigator.geolocation.getCurrentPosition(function(pos) {{
                    const lat = pos.coords.latitude.toFixed(5);
                    const lon = pos.coords.longitude.toFixed(5);
                    window.location.href = `/?lat=${{lat}}&lon=${{lon}}`;
                }}, function(err) {{
                    alert('Could not get your location.');
                }});
            }} else {{
                alert('Geolocation is not supported by your browser.');
            }}
        }}
        function enablePickMode() {{
            alert('Click anywhere on the map to pick a new location.');
            var iframe = document.getElementById('windy-iframe');
            iframe.contentWindow.postMessage({{ action: 'pickLocationMode' }}, '*');
        }}
        window.addEventListener('message', function(event) {{
            if (event.data && event.data.lat && event.data.lon) {{
                var lat = event.data.lat.toFixed(5);
                var lon = event.data.lon.toFixed(5);
                window.location.href = `/?lat=${{lat}}&lon=${{lon}}`;
            }}
        }});
        </script>
    </body>
    </html>
    """.replace('function() {{}}', 'function() {{}}'.replace('{', '{{').replace('}', '}}'))

@app.route('/map')
def full_map():
    """Full screen Windy map"""
    lat = request.args.get('lat', 50.4, type=float)
    lon = request.args.get('lon', 14.3, type=float)
    
    windy_map_url = f"https://embed.windy.com/embed2.html?lat={lat}&lon={lon}&detailLat={lat}&detailLon={lon}&width=100%&height=100%&zoom=8&level=surface&overlay=wind&product=ecmwf&menu=&message=true&marker=true&calendar=now&pressure=&type=map&location=coordinates&detail=&metricWind=default&metricTemp=default&radarRange=-1"
    
    if WINDY_API_TOKEN_MAP:
        windy_map_url += f"&key={WINDY_API_TOKEN_MAP}"
    
    return f"""
    <!DOCTYPE html>
    <html>
    <head>
        <title>Windy Map - Full Screen</title>
        <style>
            body, html {{ margin: 0; padding: 0; height: 100%; }}
            iframe {{ width: 100%; height: 100vh; border: none; }}
        </style>
    </head>
    <body>
        <iframe src="{windy_map_url}" allowfullscreen></iframe>
    </body>
    </html>
    """

@app.route('/api/weather')
def api_weather():
    """API endpoint that returns weather data as JSON"""
    print("Debug: Entered API weather route")
    lat = request.args.get('lat', 50.4, type=float)
    lon = request.args.get('lon', 14.3, type=float)
    
    weather = fetch_weather_data(lat, lon)
    if weather:
        return jsonify({
            "status": "success",
            "coordinates": {"latitude": lat, "longitude": lon},
            "data": weather
        })
    return jsonify({"status": "error", "message": "Could not fetch weather data"}), 500

@app.route('/api/windy/point')
def api_windy_point():
    """Direct Windy Point Forecast API endpoint"""
    lat = request.args.get('lat', 50.4, type=float)
    lon = request.args.get('lon', 14.3, type=float)
    
    data = fetch_real_windy_data(lat, lon)
    if data:
        return jsonify({
            "status": "success",
            "source": "Windy Point Forecast API",
            "coordinates": {"latitude": lat, "longitude": lon},
            "data": data
        })
    return jsonify({
        "status": "error", 
        "message": "Could not fetch data from Windy API",
        "coordinates": {"latitude": lat, "longitude": lon}
    }), 500

@app.route('/api/climate-insights')
def api_climate_insights():
    """API endpoint for real-time climate insights"""
    lat = request.args.get('lat', 50.4, type=float)
    lon = request.args.get('lon', 14.3, type=float)
    
    weather = fetch_weather_data(lat, lon)
    if weather:
        insights = get_climate_insights(weather)
        return jsonify({
            "status": "success",
            "coordinates": {"latitude": lat, "longitude": lon},
            "weather_data": weather,
            "climate_insights": insights,
            "timestamp": weather.get('timestamp', 'N/A'),
            "data_source": weather.get('source', 'Unknown')
        })
    return jsonify({"status": "error", "message": "Could not fetch climate data"}), 500

@app.route('/tokens')
def token_status():
    """Endpoint to check token configuration status"""
    token_status = {
        "WINDY_API_TOKEN": "Configured" if WINDY_API_TOKEN else "Missing",
        "WINDY_API_TOKEN_MAP": "Configured" if WINDY_API_TOKEN_MAP else "Missing",
        "WINDY_API_TOKEN_POINT": "Configured" if WINDY_API_TOKEN_POINT else "Missing",
        "WINDY_API_TOKEN_WEBCAMS": "Configured" if WINDY_API_TOKEN_WEBCAMS else "Missing"
    }
    return f"""
    <html>
    <head><title>Token Status</title></head>
    <body>
        <h1>API Token Status</h1>
        <ul>
            <li>WINDY_API_TOKEN: {token_status['WINDY_API_TOKEN']}</li>
            <li>WINDY_API_TOKEN_MAP: {token_status['WINDY_API_TOKEN_MAP']}</li>
            <li>WINDY_API_TOKEN_POINT: {token_status['WINDY_API_TOKEN_POINT']}</li>
            <li>WINDY_API_TOKEN_WEBCAMS: {token_status['WINDY_API_TOKEN_WEBCAMS']}</li>
        </ul>
        <p><a href="/">Back to Home</a></p>
    </body>
    </html>
    """

@app.route('/health')
def health_check():
    """Health check endpoint"""
    return jsonify({"status": "healthy", "message": "Weather Portal is running"})

# Serve static files for Waitress (production) if needed
@app.route('/static/<path:filename>')
def static_files(filename):
    return send_from_directory(STATIC_DIR, filename)

if __name__ == "__main__":
    if not all([WINDY_API_TOKEN_MAP, WINDY_API_TOKEN_POINT, WINDY_API_TOKEN_WEBCAMS]):
        print("Please configure all required API tokens in a .env file.")
    else:
        print("Windy API Tokens loaded successfully.")
        # Example usage
        weather = fetch_weather_data()
        if weather:
            print(f"Current weather: {weather}")

    print("Debug: Flask application is running on http://localhost:8080")
    app.run(host="0.0.0.0", port=8080, debug=True)