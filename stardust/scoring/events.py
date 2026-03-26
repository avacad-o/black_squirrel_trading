"""
External event weighting for Stardust. TPS § 2.8.

Fed ±15%, CPI/Jobs ±10%, Earnings ±20%, Election ±15%, Geopolitical ±25%, Regulation ±12%.
"""
from enum import Enum
from typing import Optional

class EventType(str, Enum):
    FED = "fed"
    CPI_JOBS = "cpi_jobs"
    EARNINGS = "earnings"
    ELECTION = "election"
    GEOPOLITICAL = "geopolitical"
    REGULATION = "regulation"


# Score impact in points (added or subtracted from composite)
EVENT_IMPACT: dict[EventType, float] = {
    EventType.FED: 15.0,
    EventType.CPI_JOBS: 10.0,
    EventType.EARNINGS: 20.0,
    EventType.ELECTION: 15.0,
    EventType.GEOPOLITICAL: 25.0,
    EventType.REGULATION: 12.0,
}


def apply_event_adjustment(
    base_score: float,
    event_type: EventType,
    positive: bool,
) -> float:
    """Adjust composite by event. positive=True => add impact, False => subtract."""
    impact = EVENT_IMPACT.get(event_type, 0.0)
    delta = impact if positive else -impact
    return min(100.0, max(0.0, base_score + delta))


def scenario_scores(
    base_score: float,
    event_type: EventType,
) -> tuple[float, float, float]:
    """Best / base / worst case (e.g. for earnings: beat / inline / miss)."""
    impact = EVENT_IMPACT.get(event_type, 0.0)
    best = min(100.0, base_score + impact)
    base_val = base_score
    worst = max(0.0, base_score - impact)
    return (best, base_val, worst)
