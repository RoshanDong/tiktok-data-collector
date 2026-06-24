#!/usr/bin/env python3
"""
TikTok Token Refresh Script
Run this via cron every 6 days to refresh the access token before it expires.
Access token expires in 7 days, so we refresh every 6 days as a safety margin.
"""

import json
import sys
import urllib.request
import urllib.parse
from datetime import datetime

CONFIG_PATH = ".kol-agent/tiktok-config.json"
LOG_PATH = ".kol-agent/tiktok-data/logs/token_refresh.log"


def load_config():
    with open(CONFIG_PATH, "r") as f:
        return json.load(f)


def save_config(config):
    with open(CONFIG_PATH, "w") as f:
        json.dump(config, f, indent=2)


def refresh_token(app_key, app_secret, refresh_token):
    """Call TikTok token refresh endpoint."""
    params = {
        "app_key": app_key,
        "app_secret": app_secret,
        "refresh_token": refresh_token,
        "grant_type": "refresh_token"
    }

    url = "https://auth.tiktok-shops.com/api/v2/token/refresh?" + urllib.parse.urlencode(params)

    with urllib.request.urlopen(url, timeout=30) as response:
        return json.loads(response.read().decode())


def log_message(message):
    """Log to file and print."""
    timestamp = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
    log_line = f"[{timestamp}] {message}"
    print(log_line)

    import os
    os.makedirs(".kol-agent/tiktok-data/logs", exist_ok=True)
    with open(LOG_PATH, "a") as f:
        f.write(log_line + "\n")


def main():
    log_message("Starting token refresh...")

    config = load_config()
    api_config = config.get("tiktok_api", {})

    app_key = api_config.get("client_key")
    app_secret = api_config.get("client_secret")
    current_refresh_token = api_config.get("refresh_token")

    if not all([app_key, app_secret, current_refresh_token]):
        log_message("ERROR: Missing required config values")
        sys.exit(1)

    try:
        result = refresh_token(app_key, app_secret, current_refresh_token)

        if result.get("code") == 0:
            data = result.get("data", {})
            api_config["access_token"] = data.get("access_token")
            api_config["refresh_token"] = data.get("refresh_token")
            api_config["token_expire_in"] = data.get("access_token_expire_in")

            save_config(config)

            log_message(f"SUCCESS: Token refreshed")
            log_message(f"  Seller: {data.get('seller_name')}")
            log_message(f"  New access_token expires: {data.get('access_token_expire_in')}")
            log_message(f"  New refresh_token expires: {data.get('refresh_token_expire_in')}")
        else:
            log_message(f"ERROR: Refresh failed - {result.get('message')}")
            sys.exit(1)

    except Exception as e:
        log_message(f"ERROR: {str(e)}")
        sys.exit(1)


if __name__ == "__main__":
    main()