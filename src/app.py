import os
from dotenv import load_dotenv
from flask import Flask

# Load environment variables from .env file
# This should be done early in your application's lifecycle
load_dotenv()

# Get the API token
WINDY_API_TOKEN = os.getenv("WINDY_API_TOKEN")

if not WINDY_API_TOKEN:
    print("CRITICAL: WINDY_API_TOKEN is not set. Please check your .env file.")

app = Flask(__name__)

def fetch_weather_data():
    if not WINDY_API_TOKEN:
        print("Error: WINDY_API_TOKEN not configured.")
        return None

    # Example: Use the token to make an API call
    # (This is a placeholder for actual API interaction logic)
    print(f"Fetching weather data using token: {WINDY_API_TOKEN[:4]}...")
    # response = requests.get(f"https://api.windy.com/..., headers={"X-Windy-API-Key": WINDY_API_TOKEN})
    # data = response.json()
    # return data
    return {"temperature": 25, "condition": "Sunny"} # Placeholder data

@app.route('/')
def index():
    print("Debug: Entered index route")
    weather = fetch_weather_data()
    print("Debug: Weather data fetched:", weather)
    if weather:
        return f"Current weather: {weather}"
    return "Error fetching weather data."

if __name__ == "__main__":
    print("Debug: Flask application is running on http://localhost:8080")
    app.run(host="0.0.0.0", port=8080)