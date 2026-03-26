"""
Databento tick feed handler for Tardigrade. TPS § 1.11.

Real-time price feed for all 10 instruments. Feeds multi-timeframe candle build and 3-min execution.
"""
import os
from typing import Callable, Optional

INSTRUMENTS = ["MES", "MYM", "M2K", "MGC", "SIL", "MHG", "MCL", "M6E", "MSF", "M6B"]


def _api_key() -> str:
    return os.environ.get("DATABENTO_API_KEY", "")


def stream_ticks(
    symbols: list[str],
    on_tick: Callable[[str, float, float, int], None],
) -> None:
    """
    Stream ticks: on_tick(symbol, price, size, ts_ns).
    Blocking; run in thread or process. Replace with real Databento client when key is set.
    """
    if not _api_key():
        return
    # TODO: databento.DBNStore or live subscription; call on_tick for each tick
    pass
