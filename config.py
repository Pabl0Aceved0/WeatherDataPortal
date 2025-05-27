import os
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Debugging statements
print("Debug: Attempting to load .env file...")
print("Debug: WINDY_API_TOKEN_MAP loaded from .env file:", os.getenv("WINDY_API_TOKEN_MAP"))
print("Debug: WINDY_API_TOKEN_POINT loaded from .env file:", os.getenv("WINDY_API_TOKEN_POINT"))
print("Debug: WINDY_API_TOKEN_WEBCAMS loaded from .env file:", os.getenv("WINDY_API_TOKEN_WEBCAMS"))

# Get the API tokens
WINDY_API_TOKEN_MAP = os.getenv("WINDY_API_TOKEN_MAP")
WINDY_API_TOKEN_POINT = os.getenv("WINDY_API_TOKEN_POINT")
WINDY_API_TOKEN_WEBCAMS = os.getenv("WINDY_API_TOKEN_WEBCAMS")

# Final value debug
print("Debug: Final WINDY_API_TOKEN_MAP value:", WINDY_API_TOKEN_MAP)
print("Debug: Final WINDY_API_TOKEN_POINT value:", WINDY_API_TOKEN_POINT)
print("Debug: Final WINDY_API_TOKEN_WEBCAMS value:", WINDY_API_TOKEN_WEBCAMS)

if not all([WINDY_API_TOKEN_MAP, WINDY_API_TOKEN_POINT, WINDY_API_TOKEN_WEBCAMS]):
    print("CRITICAL: One or more API tokens are not set. Please check your .env file.")
