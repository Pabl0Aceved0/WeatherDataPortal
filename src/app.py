import os
from dotenv import load_dotenv
from flask import Flask

# Load environment variables from .env file
# This should be done early in your application's lifecycle
load_dotenv()

# Get the API tokens
WINDY_API_TOKEN_MAP = os.getenv("WINDY_API_TOKEN_MAP")
WINDY_API_TOKEN_POINT = os.getenv("WINDY_API_TOKEN_POINT")
WINDY_API_TOKEN_WEBCAMS = os.getenv("WINDY_API_TOKEN_WEBCAMS")

if not all([WINDY_API_TOKEN_MAP, WINDY_API_TOKEN_POINT, WINDY_API_TOKEN_WEBCAMS]):
    print("CRITICAL: One or more API tokens are not set. Please check your .env file.")

app = Flask(__name__)

def fetch_weather_data():
    if not WINDY_API_TOKEN_MAP:
        print("Error: WINDY_API_TOKEN_MAP not configured.")
        return None

    # Example: Use the token to make an API call
    print(f"Fetching weather data using token: {WINDY_API_TOKEN_MAP[:4]}...")
    return {"temperature": 25, "condition": "Sunny"}  # Placeholder data

@app.route('/')
def index():
    print("Debug: Entered index route")
    weather = fetch_weather_data()
    print("Debug: Weather data fetched:", weather)
    if weather:
        return f"Current weather: {weather}"
    return "Error fetching weather data."

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
    app.run(host="0.0.0.0", port=8080)