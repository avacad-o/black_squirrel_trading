"""
Best instrument picker. One position at a time. TPS § 1.1.

At bracket start: scan all 10, rank by confluence score, enter highest only.
"""
from typing import Optional

# TPS § 1.1 — all 10 instruments
INSTRUMENTS = ["MES", "MYM", "M2K", "MGC", "SIL", "MHG", "MCL", "M6E", "MSF", "M6B"]


def select_instrument(
    scores_by_symbol: dict[str, float],
    direction_by_symbol: dict[str, str],
    threshold: float = 65.0,
) -> Optional[tuple[str, float, str]]:
    """
    Rank by confluence score; return (symbol, score, direction) for the best if above threshold.
    Otherwise None (skip or rescan next candle).
    """
    if not scores_by_symbol:
        return None
    best_symbol = max(scores_by_symbol.keys(), key=lambda s: scores_by_symbol[s])
    score = scores_by_symbol[best_symbol]
    if score < threshold:
        return None
    direction = direction_by_symbol.get(best_symbol, "NEUTRAL")
    if direction == "NEUTRAL":
        return None
    return (best_symbol, score, direction)
