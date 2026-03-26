"""
Order management: place, modify, cancel; track fills. TPS § 1.6, 1.9.
"""
from typing import Optional

from tardigrade.execution.tradovate import place_bracket_order, close_position


def open_trade(
    symbol: str,
    direction: str,
    contracts: int,
    entry_price: float,
    target_price: float,
    stop_price: float,
) -> Optional[str]:
    """Place bracket order; return order_id or None."""
    side = "Buy" if direction == "LONG" else "Sell"
    result = place_bracket_order(symbol, side, contracts, entry_price, target_price, stop_price)
    return result.get("orderId") if result else None


def close_trade(symbol: str, contracts: int) -> bool:
    """Flatten position at market."""
    return close_position(symbol, contracts)
