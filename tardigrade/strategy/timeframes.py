"""
Multi-timeframe definitions and weights for confluence scoring. TPS § 1.4.

Timeframes: 1D 20%, 4H 18%, 1H 15%, 30m 13%, 15m 12%, 5m 12%, 3m 10%.
Signals per TF: Bollinger position, candle sequence, volume vs 20-avg, EMA (20/50), RSI zone.
Output per TF: LONG | SHORT | NEUTRAL.
"""
from enum import Enum
from typing import NamedTuple

# Minutes per bar for each timeframe (for candle aggregation from ticks)
TF_1D = 24 * 60
TF_4H = 4 * 60
TF_1H = 60
TF_30M = 30
TF_15M = 15
TF_5M = 5
TF_3M = 3

TIMEFRAME_NAMES = ["1D", "4H", "1H", "30M", "15M", "5M", "3M"]
TIMEFRAME_MINUTES = [TF_1D, TF_4H, TF_1H, TF_30M, TF_15M, TF_5M, TF_3M]

# Weights (sum = 100). Order matches TIMEFRAME_NAMES.
WEIGHTS: list[float] = [20.0, 18.0, 15.0, 13.0, 12.0, 12.0, 10.0]


class Direction(str, Enum):
    LONG = "LONG"
    SHORT = "SHORT"
    NEUTRAL = "NEUTRAL"


class TimeframeSignal(NamedTuple):
    """Per-timeframe result for confluence."""
    timeframe: str
    direction: Direction
    details: dict  # e.g. {"bollinger": "below_lower", "rsi": 32, "candle_streak": 2}
