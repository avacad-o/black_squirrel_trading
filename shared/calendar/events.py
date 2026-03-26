"""
Market calendar and event flags. TPS § 1.3.

Fed, jobs, CPI, earnings, session opens. Events do NOT block trading; they ARE logged
as warning flags in trade record for post-trade analysis.
"""
from dataclasses import dataclass
from datetime import datetime, timedelta
from typing import Callable

# Use UTC or EST consistently; Tardigrade uses EST for brackets.
# Caller can pass naive EST datetime or timezone-aware; we use timedelta for "in N minutes".


@dataclass
class CalendarEvent:
    """Single high-impact event for flagging."""
    name: str
    at: datetime  # when it occurs (store in UTC or EST per your convention)
    flag_template: str  # e.g. "Jobs report releasing in {minutes} minutes — elevated volatility expected"


def format_flag(event: CalendarEvent, now: datetime) -> str:
    """Produce [CALENDAR] flag string. now and event.at should be same tz."""
    delta = event.at - now
    minutes = max(0, int(delta.total_seconds() / 60))
    if minutes >= 60:
        hours = minutes // 60
        return f"[CALENDAR] {event.name} in {hours} hours — {event.flag_template}"
    return f"[CALENDAR] {event.name} in {minutes} minutes — {event.flag_template}"


def active_event_flags(now: datetime, events: list[CalendarEvent], window_minutes: int = 120) -> list[str]:
    """
    Return list of flag strings for events within the next window_minutes.
    Events in the past are ignored. Used for trade log calendar_flags field.
    """
    out: list[str] = []
    for ev in events:
        delta = (ev.at - now).total_seconds()
        if 0 <= delta <= window_minutes * 60:
            out.append(format_flag(ev, now))
    return out


# Example event definitions (times would be loaded from DB or config in production)
EXAMPLE_FLAG_TEMPLATES = {
    "jobs_report": "elevated volatility expected",
    "cpi": "expect abnormal volume",
    "fed": "expect abnormal volume",
    "nyse_open": "monitor for increased spread",
    "london_open": "forex liquidity elevated",
}
