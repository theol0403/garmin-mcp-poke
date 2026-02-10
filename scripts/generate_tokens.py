#!/usr/bin/env python3
"""
Generate Garmin Connect OAuth tokens for cloud deployment.

Run this locally to authenticate with Garmin (including MFA),
then copy the output base64 string into your Render env var GARMINTOKENS_BASE64.

Usage:
    python scripts/generate_tokens.py
"""
import sys

from garminconnect import Garmin, GarminConnectAuthenticationError
from garth.exc import GarthHTTPError


def get_mfa():
    """Prompt user for MFA code."""
    print("\nGarmin Connect MFA required. Check your email/phone for the code.")
    return input("Enter MFA code: ")


def main():
    print("=== Garmin Connect Token Generator ===\n")

    email = input("Garmin email: ").strip()
    password = input("Garmin password: ").strip()

    if not email or not password:
        print("ERROR: Email and password are required.", file=sys.stderr)
        sys.exit(1)

    print("\nAuthenticating with Garmin Connect...")

    try:
        garmin = Garmin(
            email=email,
            password=password,
            is_cn=False,
            prompt_mfa=get_mfa,
        )
        garmin.login()
    except (GarthHTTPError, GarminConnectAuthenticationError) as e:
        print(f"\nERROR: Authentication failed: {e}", file=sys.stderr)
        sys.exit(1)

    print("Authentication successful!")

    # Generate base64 token string
    token_base64 = garmin.garth.dumps()

    # Verify tokens work by re-authenticating
    print("Verifying tokens...")
    try:
        verify = Garmin()
        verify.login(token_base64)
        display_name = verify.get_full_name()
        print(f"Token verification successful! Logged in as: {display_name}")
    except Exception as e:
        print(f"WARNING: Token verification failed: {e}", file=sys.stderr)
        print("The tokens were generated but may not work. Try again.", file=sys.stderr)
        sys.exit(1)

    print("\n" + "=" * 60)
    print("GARMINTOKENS_BASE64 value (copy this entire string):")
    print("=" * 60)
    print(token_base64)
    print("=" * 60)
    print(f"\nToken length: {len(token_base64)} characters")
    print("\nNext steps:")
    print("1. Copy the token string above")
    print("2. Set it as GARMINTOKENS_BASE64 in your Render environment variables")
    print("3. Deploy/restart your Render service")
    print("\nTokens typically last ~6 months. Re-run this script to refresh.")


if __name__ == "__main__":
    main()
