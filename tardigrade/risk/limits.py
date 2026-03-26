"""
Daily target, max loss, halt logic. TPS § 1.7, 1.8.

$750/day target; when hit, stop all trading. $500 drawdown in cycle = stop.
"""
from typing import Optional

DAILY_TARGET = 750.0
MAX_DRAWDOWN_PER_CYCLE = 500.0


def daily_target_hit(daily_pnl: float, target: float = DAILY_TARGET) -> bool:
    return daily_pnl >= target


def drawdown_hit(cycle_start_balance: float, current_balance: float) -> bool:
    """True if drawdown from cycle start >= $500."""
    return (cycle_start_balance - current_balance) >= MAX_DRAWDOWN_PER_CYCLE


def cycle_doubled(start: float, current: float) -> bool:
    """Cycle = account doubles without intervention."""
    return current >= 2.0 * start
