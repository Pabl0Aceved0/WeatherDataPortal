import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Debugging statements
print("Debug: Attempting to load .env file...")
print("Debug: WINDY_API_TOKEN loaded from .env file:", os.getenv("WINDY_API_TOKEN"))

# Get the API token
WINDY_API_TOKEN = os.getenv("WINDY_API_TOKEN") or "your_actual_windy_api_key"

# Final value debug
print("Debug: Final WINDY_API_TOKEN value:", WINDY_API_TOKEN)

if not WINDY_API_TOKEN:
    print("CRITICAL: WINDY_API_TOKEN is not set. Please check your .env file.")
