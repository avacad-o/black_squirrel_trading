#!/usr/bin/env python3
"""
Demo: Tardigrade logic (no live data). Run from repo root: python run_tardigrade_demo.py
"""
import sys
from datetime import datetime
from pathlib import Path

# Ensure repo root is on path
root = Path(__file__).resolve().parent
sys.path.insert(0, str(root))

from tardigrade.execution.brackets import (
    get_current_bracket,
    can_enter_new_trade,
    BracketName,
)
from tardigrade.strategy.timeframes import TimeframeSignal, Direction
from tardigrade.strategy.confluence import compute_confluence, is_actionable
from tardigrade.strategy.selector import select_instrument, INSTRUMENTS
from tardigrade.risk.sizing import contracts_for_balance
from tardigrade.risk.streaks import streak_action, StreakAction


def main():
    # Bracket: use 9:50 AM EST (during Open bracket)
    class EST(datetime):
        pass

    est_now = datetime(2025, 3, 17, 9, 50, 0)
    b = get_current_bracket(est_now)
    print("Current bracket:", b.name if b else None)
    print("Can enter new trade:", can_enter_new_trade(est_now))

    # Confluence: mock 7 timeframes LONG
    signals = [
        TimeframeSignal(tf, Direction.LONG, {})
        for tf in ["1D", "4H", "1H", "30M", "15M", "5M", "3M"]
    ]
    score, direction = compute_confluence(signals)
    print("Confluence score:", score, "direction:", direction.value)
    print("Actionable (>=65):", is_actionable(score))

    # Selector: mock scores
    scores = {s: 72.0 for s in INSTRUMENTS}
    scores["MES"] = 81.0
    dirs = {s: "LONG" for s in INSTRUMENTS}
    sel = select_instrument(scores, dirs)
    print("Selected instrument:", sel)

    # Sizing
    print("Contracts for $3000:", contracts_for_balance(3000))

    # Streaks
    print("3 losses ->", streak_action(["loss", "loss", "loss"]))
    print("3 wins ->", streak_action(["win", "win", "win"]))


if __name__ == "__main__":
    main()
