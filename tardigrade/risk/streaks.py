"""
Win/loss streak rules. TPS § 1.7.

3 consecutive losses → pause until next bracket.
3 consecutive wins → continue until first loss then stop for bracket.
1W–1L alternating → continue.
Daily target hit → stop day. $500 drawdown in cycle → stop + review. 3 losing cycles → halt.
"""
from enum import Enum
from typing import Literal

Result = Literal["win", "loss"]


class StreakAction(str, Enum):
    CONTINUE = "continue"
    PAUSE_UNTIL_NEXT_BRACKET = "pause_until_next_bracket"
    STOP_FOR_DAY = "stop_for_day"
    HALT_PROGRAM = "halt_program"


def streak_action(
    last_results: list[Result],
    daily_target_hit: bool = False,
    drawdown_500_hit: bool = False,
    losing_cycles_count: int = 0,
) -> StreakAction:
    """
    last_results: most recent first, e.g. [win, loss, win].
    Returns action for this bracket.
    """
    if losing_cycles_count >= 3:
        return StreakAction.HALT_PROGRAM
    if daily_target_hit:
        return StreakAction.STOP_FOR_DAY
    if drawdown_500_hit:
        return StreakAction.STOP_FOR_DAY  # full system review

    if len(last_results) < 3:
        return StreakAction.CONTINUE

    recent = last_results[:3]
    if all(r == "loss" for r in recent):
        return StreakAction.PAUSE_UNTIL_NEXT_BRACKET
    if all(r == "win" for r in recent):
        # Continue until first loss, then stop for bracket (handled by "after first loss" logic at call site)
        return StreakAction.CONTINUE

    return StreakAction.CONTINUE


def should_stop_after_win_streak_then_loss(last_results: list[Result]) -> bool:
    """After 3 wins, on first loss we stop for the bracket."""
    if len(last_results) < 4:
        return False
    if last_results[0] != "loss":
        return False
    return all(r == "win" for r in last_results[1:4])
