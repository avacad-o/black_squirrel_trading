"""
Best / base / worst case scenario builder. TPS § 2.6, 2.8.
"""
from typing import Tuple


def build_scenarios(
    target_pct: float,
    weeks: int,
    best_case_pct: float | None = None,
    worst_case_pct: float | None = None,
) -> Tuple[float, float, float]:
    """
    Return (best_pct, base_pct, worst_pct). Base = target_pct in weeks.
    If not provided, best/worst are derived from target (e.g. +50% / -50% of target).
    """
    base = target_pct
    best = best_case_pct if best_case_pct is not None else target_pct * 1.8
    worst = worst_case_pct if worst_case_pct is not None else -abs(target_pct) * 1.0
    return (best, base, worst)
