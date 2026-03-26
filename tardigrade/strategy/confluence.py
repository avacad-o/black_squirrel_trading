"""
Weighted confluence score calculator. TPS § 1.4.

Per-timeframe directional signal (LONG/SHORT/NEUTRAL) × weight → final score 0–100.
Above 65 = actionable; below 65 = skip.
"""
from tardigrade.strategy.timeframes import Direction, TimeframeSignal, WEIGHTS, TIMEFRAME_NAMES


def compute_confluence(signals: list[TimeframeSignal]) -> tuple[float, Direction]:
    """
    Aggregate per-TF signals with weights. Returns (score 0–100, overall direction).
    If signals length != 7, weights are applied in order; missing TFs contribute 0.
    """
    if not signals:
        return (0.0, Direction.NEUTRAL)

    long_score = 0.0
    short_score = 0.0
    for i, sig in enumerate(signals):
        w = WEIGHTS[i] / 100.0 if i < len(WEIGHTS) else 0.0
        if sig.direction == Direction.LONG:
            long_score += w
        elif sig.direction == Direction.SHORT:
            short_score += w
        # NEUTRAL adds to neither

    # Score 0–100 = conviction; direction = winning side
    total_weight = sum(WEIGHTS) / 100.0
    winning = max(long_score, short_score)
    if winning > 0 and total_weight > 0:
        score = 50 + 50 * (winning / total_weight)
        direction = Direction.LONG if long_score >= short_score else Direction.SHORT
    else:
        score = 50.0
        direction = Direction.NEUTRAL

    return (min(100.0, max(0.0, score)), direction)


def is_actionable(score: float, threshold: float = 65.0) -> bool:
    """Score above threshold = actionable (enter); below = skip."""
    return score >= threshold
