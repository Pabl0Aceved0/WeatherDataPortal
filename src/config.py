"""Central configuration: loads Windy API tokens from the environment / .env file.

Token values are never printed or logged.
"""
import logging
import os

from dotenv import load_dotenv

load_dotenv()

logger = logging.getLogger(__name__)

WINDY_API_TOKEN = os.getenv("WINDY_API_TOKEN")
WINDY_API_TOKEN_MAP = os.getenv("WINDY_API_TOKEN_MAP")
WINDY_API_TOKEN_POINT = os.getenv("WINDY_API_TOKEN_POINT")
WINDY_API_TOKEN_WEBCAMS = os.getenv("WINDY_API_TOKEN_WEBCAMS")

REQUIRED_TOKENS = {
    "WINDY_API_TOKEN_MAP": WINDY_API_TOKEN_MAP,
    "WINDY_API_TOKEN_POINT": WINDY_API_TOKEN_POINT,
    "WINDY_API_TOKEN_WEBCAMS": WINDY_API_TOKEN_WEBCAMS,
}


def missing_tokens():
    """Return the names of required tokens that are not set."""
    return [name for name, value in REQUIRED_TOKENS.items() if not value]


if missing_tokens():
    logger.warning(
        "Missing API tokens: %s. Check your .env file.", ", ".join(missing_tokens())
    )
