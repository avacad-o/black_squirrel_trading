"""
Trading time bracket logic. All times EST. TPS § 1.2.

Pre-Market 7:00–9:15 (no entry after 9:12), Open 9:45–10:30 (after 10:27),
Close 3:00–4:00 (after 3:57), London 2:00–4:00 (after 3:57).
No entry < 3 min remaining; all positions closed at bracket cutoff.
"""
from dataclasses import dataclass
from datetime import time, datetime
from enum import Enum
from typing import Optional

# All times EST. Use naive time for simplicity; caller passes EST now.


class BracketName(str, Enum):
    PRE_MARKET = "pre_market"
    OPEN = "open"
    CLOSE = "close"
    LONDON = "london"
    NONE = "none"


@dataclass
class Bracket:
    """Single trading window."""
    name: BracketName
    start: time
    end: time
    no_entry_after: time  # 3 min before end


BRACKETS: list[Bracket] = [
    Bracket(BracketName.PRE_MARKET, time(7, 0), time(9, 15), time(9, 12)),
    Bracket(BracketName.OPEN, time(9, 45), time(10, 30), time(10, 27)),
    Bracket(BracketName.CLOSE, time(15, 0), time(16, 0), time(15, 57)),
    Bracket(BracketName.LONDON, time(2, 0), time(4, 0), time(3, 57)),
]


def _to_time(est_now: datetime) -> time:
    """Extract time component (assume est_now is in EST)."""
    return est_now.time()


def get_current_bracket(est_now: datetime) -> Optional[Bracket]:
    """Return the bracket that contains est_now, or None if between brackets."""
    t = _to_time(est_now)
    for b in BRACKETS:
        if b.start <= b.end:
            if b.start <= t < b.end:
                return b
        else:
            # overnight (e.g. London 2:00–4:00)
            if t >= b.start or t < b.end:
                return b
    return None


def can_enter_new_trade(est_now: datetime) -> bool:
    """True if we are inside a bracket and at least 3 minutes remain before no_entry_after."""
    b = get_current_bracket(est_now)
    if b is None:
        return False
    t = _to_time(est_now)
    # Must be strictly before no_entry_after
    if b.no_entry_after > b.start:
        return t < b.no_entry_after
    # Overnight: no_entry_after 3:57, end 4:00
    return t < b.no_entry_after or t >= b.end


def minutes_remaining(est_now: datetime) -> Optional[float]:
    """Minutes until bracket end. None if not in a bracket."""
    b = get_current_bracket(est_now)
    if b is None:
        return None
    t = _to_time(est_now)
    end_sec = b.end.hour * 3600 + b.end.minute * 60 + b.end.second
    now_sec = t.hour * 3600 + t.minute * 60 + t.second
    if b.start <= b.end:
        rem = end_sec - now_sec
    else:
        if t >= b.start:
            rem = (24 * 3600 - now_sec) + (end_sec)
        else:
            rem = end_sec - now_sec
    if rem <= 0:
        return 0.0
    return rem / 60.0


def is_cutoff(est_now: datetime) -> bool:
    """True if we are at or past bracket end (flatten position)."""
    b = get_current_bracket(est_now)
    if b is None:
        return True  # between brackets => treat as cutoff, no new trades
    t = _to_time(est_now)
    if b.start <= b.end:
        return t >= b.end
    return t >= b.end and t < b.start
