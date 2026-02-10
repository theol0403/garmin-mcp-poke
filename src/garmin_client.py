"""
Garmin Connect authentication wrapper for cloud deployment.

Handles token-based and credential-based authentication for the Garmin API.
"""
import io
import sys

from garminconnect import Garmin, GarminConnectAuthenticationError
from garth.exc import GarthHTTPError

from config import GARMINTOKENS_BASE64, GARMIN_EMAIL, GARMIN_PASSWORD


def init_garmin_client():
    """Initialize and return an authenticated Garmin client.

    Authentication priority:
    1. GARMINTOKENS_BASE64 env var (base64-encoded OAuth tokens, recommended for cloud)
    2. GARMIN_EMAIL + GARMIN_PASSWORD (direct credentials, only works without MFA)

    Returns:
        Authenticated Garmin client instance, or None on failure.
    """
    if GARMINTOKENS_BASE64:
        return _auth_with_tokens(GARMINTOKENS_BASE64)

    if GARMIN_EMAIL and GARMIN_PASSWORD:
        return _auth_with_credentials(GARMIN_EMAIL, GARMIN_PASSWORD)

    print(
        "ERROR: No Garmin credentials configured.\n"
        "Set GARMINTOKENS_BASE64 (recommended) or GARMIN_EMAIL + GARMIN_PASSWORD.\n"
        "Run 'python scripts/generate_tokens.py' to generate tokens.",
        file=sys.stderr,
    )
    return None


def _auth_with_tokens(token_base64: str):
    """Authenticate using base64-encoded OAuth tokens."""
    # Suppress garth stderr noise during token validation
    old_stderr = sys.stderr
    sys.stderr = io.StringIO()

    try:
        garmin = Garmin()
        garmin.login(token_base64)
    except (FileNotFoundError, GarthHTTPError, GarminConnectAuthenticationError) as e:
        sys.stderr = old_stderr
        print(f"ERROR: Token authentication failed: {e}", file=sys.stderr)
        print(
            "Tokens may be expired. Re-run 'python scripts/generate_tokens.py' to refresh.",
            file=sys.stderr,
        )
        return None
    finally:
        sys.stderr = old_stderr

    print("Garmin client authenticated via tokens.", file=sys.stderr)
    return garmin


def _auth_with_credentials(email: str, password: str):
    """Authenticate using email and password (no MFA support in cloud)."""
    try:
        garmin = Garmin(email=email, password=password, is_cn=False)
        garmin.login()
    except (GarthHTTPError, GarminConnectAuthenticationError) as e:
        print(f"ERROR: Credential authentication failed: {e}", file=sys.stderr)
        print(
            "If your account has MFA, use GARMINTOKENS_BASE64 instead.",
            file=sys.stderr,
        )
        return None

    print("Garmin client authenticated via credentials.", file=sys.stderr)
    return garmin
