"""
Four weighted scoring variants (Model A–D). TPS § 2.5.

Signals: Insider, Institutional, Options, Technical, Fundamental, Sentiment, Analyst.
"""
from typing import NamedTuple

SIGNAL_NAMES = [
    "insider",
    "institutional",
    "options",
    "technical",
    "fundamental",
    "sentiment",
    "analyst",
]

# Rows = signals, cols = Model A, B, C, D (each column sums to 100)
WEIGHT_MATRIX: list[list[float]] = [
    [20, 15, 10, 25],  # insider
    [18, 20, 15, 20],  # institutional
    [15, 20, 10, 15],  # options
    [15, 10, 25, 10],  # technical
    [12, 15, 20, 10],  # fundamental
    [10, 10, 10, 10],  # sentiment
    [10, 10, 10, 10],  # analyst
]


def model_weights(model: str) -> dict[str, float]:
    """Return signal -> weight for model A/B/C/D. Weights in 0-100 scale."""
    idx = {"A": 0, "B": 1, "C": 2, "D": 3}.get(model.upper(), 0)
    return {name: WEIGHT_MATRIX[i][idx] for i, name in enumerate(SIGNAL_NAMES)}


def score_one_model(signal_scores: dict[str, float], model: str) -> float:
    """Weighted sum for one model. signal_scores: 0-100 per signal."""
    w = model_weights(model)
    total = 0.0
    for name, weight in w.items():
        total += (weight / 100.0) * signal_scores.get(name, 0.0)
    return min(100.0, max(0.0, total))
