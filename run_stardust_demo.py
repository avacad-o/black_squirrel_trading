#!/usr/bin/env python3
"""
Demo: Stardust scoring and signal output. Run from repo root: python run_stardust_demo.py
"""
import sys
from pathlib import Path

root = Path(__file__).resolve().parent
sys.path.insert(0, str(root))

from stardust.scoring.models import score_one_model, SIGNAL_NAMES
from stardust.scoring.composite import composite_score, consensus
from stardust.scoring.events import apply_event_adjustment, EventType
from stardust.signals.threshold import status_from_score, SignalStatus
from stardust.signals.scenarios import build_scenarios
from stardust.signals.output import format_signal


def main():
    # Mock signal scores 0-100
    signal_scores = {n: 70.0 for n in SIGNAL_NAMES}
    signal_scores["insider"] = 80.0
    signal_scores["technical"] = 65.0

    blended, per_model = composite_score(signal_scores)
    print("Blended score:", blended)
    print("Per-model:", per_model)
    print("Consensus:", consensus(per_model))

    adjusted = apply_event_adjustment(blended, EventType.EARNINGS, positive=False)
    print("After earnings (negative):", adjusted)

    status = status_from_score(blended, activation_threshold=70, in_sight_threshold=60)
    print("Status:", status.value)

    best, base, worst = build_scenarios(5.0, 6)
    print("Scenarios: best", best, "base", base, "worst", worst)

    text = format_signal(
        quadrant="REMNANT — Battered Recovery",
        ticker="EXAMPLE",
        target_pct=5.0,
        weeks=6,
        composite_score=blended,
        model_scores=per_model,
        primary_signals=[
            "Insider buying: 3 transactions in last 30 days",
            "RSI: 31 — oversold territory",
        ],
        risk_factors=["Earnings date: 3 weeks out (binary event)"],
        best_pct=9.0,
        base_pct=5.0,
        worst_pct=-8.0,
        status=status,
    )
    print("\n" + text)


if __name__ == "__main__":
    main()
