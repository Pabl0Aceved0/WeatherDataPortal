import os
from dotenv import load_dotenv

# Load environment variables from .env file
# This should be done early in your application's lifecycle
load_dotenv()

# Get the API token
WINDY_API_TOKEN = os.getenv("WINDY_API_TOKEN")

if not WINDY_API_TOKEN:
    print("CRITICAL: WINDY_API_TOKEN is not set. Please check your .env file.")

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

if __name__ == "__main__":
    if not WINDY_API_TOKEN:
        print("Please configure your WINDY_API_TOKEN in a .env file.")
    else:
        print(f"Windy API Token loaded successfully: {WINDY_API_TOKEN[:4]}...")
        # Example usage
        weather = fetch_weather_data()
        if weather:
            print(f"Current weather: {weather}")

    # Your application's main logic would continue here