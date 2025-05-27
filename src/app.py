import os
import requests
from dotenv import load_dotenv
from flask import Flask, jsonify, render_template_string, request

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

app = Flask(__name__)

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
    return f"""
    <!DOCTYPE html>
    <html lang='en'>
    <head>
        <meta charset='UTF-8'>
        <meta name='viewport' content='width=device-width, initial-scale=1.0'>
        <title>Weather Portal - Responsive</title>
        <style>
            html, body {{ margin: 0; padding: 0; height: 100%; width: 100vw; box-sizing: border-box; background: #f5f7fa; }}
            body {{ font-family: 'Segoe UI', Arial, sans-serif; min-height: 100vh; width: 100vw; display: flex; flex-direction: column; }}
            .header {{ position: sticky; top: 0; z-index: 10; background: linear-gradient(135deg, #667eea 0%, #764ba2 100%); color: #fff; padding: 1.1rem 0.7rem; border-radius: 0 0 16px 16px; text-align: center; box-shadow: 0 2px 8px rgba(0,0,0,0.07); }}
            .container {{ flex: 1 1 auto; width: 100%; max-width: 480px; margin: 0 auto; padding: 1rem 0.5rem 0.5rem 0.5rem; display: flex; flex-direction: column; gap: 1.1rem; }}
            .weather-card, .climate-insights {{ background: #fff; border-radius: 10px; padding: 1.1rem 0.7rem; box-shadow: 0 2px 8px rgba(0,0,0,0.07); }}
            .weather-grid {{ display: flex; flex-wrap: wrap; gap: 0.7rem; justify-content: space-between; }}
            .weather-item {{ flex: 1 1 45%; min-width: 120px; background: #f8f9fa; border-radius: 8px; padding: 0.8rem; text-align: center; margin-bottom: 0.5rem; }}
            .weather-value {{ font-size: 1.4em; font-weight: bold; color: #667eea; }}
            .coordinates {{ background: #e3f2fd; padding: 0.6rem; border-radius: 5px; margin-bottom: 0.7rem; font-family: monospace; text-align: center; }}
            .map-container {{ background: #fff; border-radius: 10px; overflow: hidden; box-shadow: 0 2px 8px rgba(0,0,0,0.07); width: 100%; }}
            .map-container iframe {{ width: 100%; min-width: 200px; height: 220px; border: none; display: block; }}
            .nav-links {{ display: flex; flex-wrap: wrap; gap: 0.6rem; justify-content: center; margin: 0.7rem 0 0.2rem 0; }}
            .nav-links a {{ flex: 1 1 40%; min-width: 120px; text-align: center; padding: 0.8rem 0.5rem; background: #667eea; color: #fff; text-decoration: none; border-radius: 6px; font-size: 1.1em; transition: background 0.2s; }}
            .nav-links a:hover, .nav-links a:focus {{ background: #5a6fd8; outline: none; }}
            .climate-insights {{ background: #e3f2fd; color: #222; border-left: 5px solid #667eea; font-size: 1.08em; }}
            .footer {{ text-align: center; color: #888; font-size: 0.95em; padding: 1.2rem 0 0.5rem 0; }}
            @media (max-width: 700px) {{ .container {{ max-width: 100vw; padding: 0.5rem; }} .header {{ font-size: 1.1rem; padding: 0.7rem 0.5rem; }} .weather-grid {{ flex-direction: column; gap: 0.5rem; }} .weather-item {{ min-width: 90px; padding: 0.7rem; }} .nav-links a {{ font-size: 1em; padding: 0.7rem 0.3rem; }} .map-container iframe {{ height: 160px; }} }}
        </style>
    </head>
    <body>
        <div class='header'>
            <h1 style='margin:0;font-size:2em;'>🌤️ Weather Portal</h1>
            <div style='font-size:1.1em;'>Live weather powered by Windy.com</div>
        </div>
        <div class='container'>
            <div class='weather-card'>
                <div class='coordinates' style='font-size:1.1em;'>
                    <span style="color:#0077be;font-weight:bold;">📍 Map Point:</span>
                    <span style="font-family:monospace;">Lat: {lat:.5f}°, Lon: {lon:.5f}°</span>
                </div>
                <div class='weather-grid'>
                    <div class='weather-item'><div class='weather-value'>{weather.get('temperature', 'N/A')}</div><div>Temperature (°C)</div></div>
                    <div class='weather-item'><div class='weather-value'>{weather.get('wind_speed', weather.get('condition', 'N/A'))}</div><div>Wind/Condition</div></div>
                    <div class='weather-item'><div class='weather-value'>{weather.get('pressure', 'N/A')}</div><div>Pressure (hPa)</div></div>
                    <div class='weather-item'><div class='weather-value'>{weather.get('humidity', 'N/A')}</div><div>Humidity (%)</div></div>
                </div>
                <div style='color:#666;font-size:0.95em;margin-top:0.7em;'>Source: {weather.get('source', 'Unknown')}</div>
            </div>
            <div class='map-container'>
                <iframe id='windy-iframe' src='{windy_map_url}' allowfullscreen title='Windy.com Weather Map'></iframe>
                <div style='text-align:center;font-size:0.98em;color:#555;margin-top:0.3em;'>
                    <b>Tip:</b> Haz clic en el mapa para mover el punto y ver el clima de otra ubicación.
                </div>
            </div>
            <div class='climate-insights'>
                <b>Climate Insights:</b>
                <ul style='margin:0.5em 0 0 1.2em;padding:0;'>
                    {''.join([f'<li>{insight}</li>' for insight in climate_insights])}
                </ul>
            </div>
            <div class='nav-links'>
                <a href='/api/weather?lat={lat}&lon={lon}'>📊 Raw JSON</a>
                <a href='/tokens'>🔑 API Status</a>
                <a href='/map'>🗺️ Full Map</a>
                <a href='/health'>💚 Health</a>
            </div>
        </div>
        <div class='footer'>
            &copy; 2025 Windy.com | <a href='https://www.w3schools.com/html/html_responsive.asp' target='_blank'>Responsive Info</a>
        </div>
        <script>
        window.addEventListener('message', function(event) {{
            try {{
                if (typeof event.data === 'string' && event.data.includes('lat') && event.data.includes('lon')) {{
                    var latMatch = event.data.match(/lat=([-\d.]+)/);
                    var lonMatch = event.data.match(/lon=([-\d.]+)/);
                    if (latMatch && lonMatch) {{
                        var lat = latMatch[1];
                        var lon = lonMatch[1];
                        window.location.search = '?lat=' + lat + '&lon=' + lon;
                    }}
                }}
            }} catch (e) {{ /* ignore */ }}
        }});
        function sendMapClickHandler() {{
            var iframe = document.getElementById('windy-iframe');
            if (!iframe) return;
            iframe.contentWindow.postMessage(JSON.stringify({{ action: 'on', event: 'click', callback: true }}), '*');
        }}
        window.onload = function() {{
            setTimeout(sendMapClickHandler, 1200);
        }};
        </script>
    </body>
    </html>
    """

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