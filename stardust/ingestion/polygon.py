"""
Polygon.io market data: price, volume, options flow, news. TPS § 2.4, 2.12.
"""
import os
from typing import Any, Optional

# Set POLYGON_API_KEY in env or Doppler.


def _api_key() -> str:
    return os.environ.get("POLYGON_API_KEY", "")


def get_bars(symbol: str, timeframe: str = "day", limit: int = 100) -> list[dict]:
    """OHLCV bars. Replace with real Polygon client when key is set."""
    if not _api_key():
        return []
    # TODO: requests.get(f"https://api.polygon.io/v2/aggs/ticker/{symbol}/range/...", params={"apiKey": _api_key()})
    return []


def get_news(symbol: str, limit: int = 10) -> list[dict]:
    """News for symbol."""
    if not _api_key():
        return []
    return []
