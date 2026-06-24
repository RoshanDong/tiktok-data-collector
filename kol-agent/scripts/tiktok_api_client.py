"""
TikTok Shop API Client
Handles authentication and API requests to TikTok Shop Seller API.
"""

import json
import time
from datetime import datetime
from pathlib import Path
from typing import Optional, Dict, Any, List
import requests
from tenacity import retry, stop_after_attempt, wait_exponential

# Config path
CONFIG_PATH = Path(__file__).parent.parent / "tiktok-config.json"

# API Endpoints
TOKEN_URL = "https://open.tiktokapis.com/v2/oauth/token/"
ORDER_LIST_URL = "https://open.tiktokapis.com/v2/order/list/"


class TikTokAPIClient:
    """Client for TikTok Shop Seller API"""

    def __init__(self, config_path: Optional[Path] = None):
        self.config_path = config_path or CONFIG_PATH
        self.config = self._load_config()
        self.access_token: Optional[str] = None
        self.token_expires_at: float = 0

    def _load_config(self) -> Dict[str, Any]:
        """Load configuration from JSON file"""
        with open(self.config_path, 'r', encoding='utf-8') as f:
            return json.load(f)

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=5, max=60)
    )
    def authenticate(self) -> str:
        """
        Authenticate with TikTok API using client credentials.
        Returns access token.
        """
        api_config = self.config['tiktok_api']

        payload = {
            "client_key": api_config['client_key'],
            "client_secret": api_config['client_secret'],
            "grant_type": "client_credentials"
        }

        response = requests.post(TOKEN_URL, data=payload, timeout=30)

        if response.status_code == 200:
            data = response.json()
            self.access_token = data['access_token']
            self.token_expires_at = time.time() + data.get('expires_in', 3600)
            return self.access_token
        else:
            raise TikTokAPIError(
                f"Authentication failed: {response.status_code} - {response.text}"
            )

    def is_token_valid(self) -> bool:
        """Check if current access token is still valid"""
        if not self.access_token:
            return False
        return time.time() < self.token_expires_at - 60  # 60s buffer

    def get_access_token(self) -> str:
        """Get valid access token, re-authenticating if needed"""
        if not self.is_token_valid():
            return self.authenticate()
        return self.access_token

    @retry(
        stop=stop_after_attempt(3),
        wait=wait_exponential(multiplier=1, min=5, max=60)
    )
    def fetch_orders(
        self,
        start_time: int,
        end_time: int,
        page_size: int = 100
    ) -> Dict[str, Any]:
        """
        Fetch orders from TikTok Shop API.

        Args:
            start_time: Unix timestamp for start date
            end_time: Unix timestamp for end date
            page_size: Number of orders per page (default 100, max 1000)

        Returns:
            Dict containing orders and pagination info
        """
        token = self.get_access_token()

        headers = {
            "Authorization": f"Bearer {token}",
            "Content-Type": "application/json"
        }

        params = {
            "create_time_start": start_time,
            "create_time_end": end_time,
            "page_size": page_size
        }

        response = requests.get(
            ORDER_LIST_URL,
            headers=headers,
            params=params,
            timeout=30
        )

        if response.status_code == 200:
            return response.json()
        elif response.status_code == 429:
            raise RateLimitError("Rate limit exceeded")
        elif response.status_code == 401:
            # Token expired, re-authenticate and retry
            self.access_token = None
            raise TikTokAPIError("Token expired, need re-authentication")
        else:
            raise TikTokAPIError(
                f"Failed to fetch orders: {response.status_code} - {response.text}"
            )

    def fetch_all_orders_for_date(self, date_str: str) -> List[Dict]:
        """
        Fetch all orders for a specific date.

        Args:
            date_str: Date in YYYY-MM-DD format

        Returns:
            List of order dictionaries
        """
        from datetime import datetime, timezone

        # Parse date
        date = datetime.strptime(date_str, '%Y-%m-%d')

        # Start of day (00:00:00) in UTC
        start_time = int(date.replace(hour=0, minute=0, second=0, microsecond=0).timestamp())
        # End of day (23:59:59) in UTC
        end_time = int(date.replace(hour=23, minute=59, second=59, microsecond=999999).timestamp())

        all_orders = []
        has_more = True
        next_page_token = None

        while has_more:
            params = {
                "create_time_start": start_time,
                "create_time_end": end_time,
                "page_size": 100
            }
            if next_page_token:
                params["page_token"] = next_page_token

            result = self.fetch_orders(start_time, end_time)

            orders = result.get('data', {}).get('orders', [])
            all_orders.extend(orders)

            has_more = result.get('data', {}).get('has_more', False)
            next_page_token = result.get('data', {}).get('next_page_token')

        return all_orders


class TikTokAPIError(Exception):
    """Custom exception for TikTok API errors"""
    pass


class RateLimitError(TikTokAPIError):
    """Exception for rate limit (429) responses"""
    pass


if __name__ == "__main__":
    # Test authentication
    try:
        client = TikTokAPIClient()
        print("API Client initialized successfully")
    except Exception as e:
        print(f"Error initializing client: {e}")