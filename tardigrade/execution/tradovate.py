"""
Tradovate broker API client. TPS § 1.11.

Env: TRADOVATE_API_KEY, TRADOVATE_API_SECRET, TRADOVATE_ACCOUNT_ID, TRADOVATE_ENV (sim|live).
"""
import os
from typing import Optional


def is_sim() -> bool:
    return os.environ.get("TRADOVATE_ENV", "sim").lower() == "sim"


def place_market_order(symbol: str, side: str, quantity: int) -> Optional[dict]:
    """Place market order. Returns order info or None. Implement with Tradovate REST when key set."""
    # TODO: POST to Tradovate API
    return None


def place_bracket_order(
    symbol: str,
    side: str,
    quantity: int,
    entry: float,
    target: float,
    stop: float,
) -> Optional[dict]:
    """Place order with target and stop. Broker may use OCO or separate orders."""
    return place_market_order(symbol, side, quantity)


def get_positions() -> list[dict]:
    """Current positions."""
    return []


def close_position(symbol: str, quantity: int) -> bool:
    """Close position at market."""
    return False
