"""
Configuration for Garmin MCP Server (Poke-compatible)
"""
import os

# Garmin authentication
GARMINTOKENS_BASE64 = os.getenv("GARMINTOKENS_BASE64")
GARMIN_EMAIL = os.getenv("GARMIN_EMAIL")
GARMIN_PASSWORD = os.getenv("GARMIN_PASSWORD")

# Server settings
PORT = int(os.getenv("PORT", 8000))
HOST = os.getenv("HOST", "0.0.0.0")
