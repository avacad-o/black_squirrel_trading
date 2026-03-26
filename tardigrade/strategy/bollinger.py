"""
Bollinger Band signals per timeframe. TPS § 1.4.

Position: above mid / below mid / outside upper band / outside lower band.
"""
from typing import Literal

BandPosition = Literal["above_upper", "above_mid", "below_mid", "below_lower", "at_mid"]


def bollinger_position(price: float, mid: float, upper: float, lower: float) -> BandPosition:
    """Classify price relative to bands. Assumes upper > mid > lower."""
    if mid == upper == lower:
        return "at_mid"
    if price >= upper:
        return "above_upper"
    if price > mid:
        return "above_mid"
    if price < lower:
        return "below_lower"
    if price < mid:
        return "below_mid"
    return "at_mid"


def bollinger_direction(position: BandPosition) -> str:
    """Map band position to directional bias for confluence: LONG, SHORT, or NEUTRAL."""
    if position == "below_lower":
        return "LONG"
    if position == "above_upper":
        return "SHORT"
    if position == "above_mid":
        return "LONG"
    if position == "below_mid":
        return "SHORT"
    return "NEUTRAL"


def compute_bands(prices: list[float], period: int = 20, k: float = 2.0) -> tuple[float, float, float]:
    """Standard BB: mid = SMA(period), std = stddev(period), upper = mid + k*std, lower = mid - k*std."""
    if len(prices) < period:
        return (0.0, 0.0, 0.0)
    slice_p = prices[-period:]
    mid = sum(slice_p) / period
    variance = sum((x - mid) ** 2 for x in slice_p) / period
    std = variance ** 0.5
    upper = mid + k * std
    lower = mid - k * std
    return (mid, upper, lower)
