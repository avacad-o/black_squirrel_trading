"""
Blended composite score from all four models. TPS § 2.5.
"""
from stardust.scoring.models import score_one_model, SIGNAL_NAMES


def composite_score(signal_scores: dict[str, float]) -> tuple[float, dict[str, float]]:
    """
    signal_scores: 0-100 per signal (insider, institutional, ...).
    Returns (blended 0-100, per-model scores A/B/C/D).
    """
    per_model: dict[str, float] = {}
    for m in "A", "B", "C", "D":
        per_model[m] = score_one_model(signal_scores, m)
    blended = (per_model["A"] + per_model["B"] + per_model["C"] + per_model["D"]) / 4.0
    return (min(100.0, max(0.0, blended)), per_model)


def consensus(per_model: dict[str, float], tolerance: float = 5.0) -> str:
    """High / medium / low consensus based on spread of model scores."""
    if not per_model:
        return "unknown"
    vals = list(per_model.values())
    spread = max(vals) - min(vals)
    if spread <= tolerance:
        return "high"
    if spread <= 15:
        return "medium"
    return "low"
