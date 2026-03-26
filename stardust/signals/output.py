"""
Stardust trade idea output format. TPS § 2.6.
"""
from typing import Optional

from stardust.scoring.composite import consensus
from stardust.signals.threshold import SignalStatus


def format_signal(
    quadrant: str,
    ticker: str,
    target_pct: float,
    weeks: int,
    composite_score: float,
    model_scores: dict[str, float],
    primary_signals: list[str],
    risk_factors: list[str],
    best_pct: float,
    base_pct: float,
    worst_pct: float,
    status: SignalStatus,
) -> str:
    """Produce the STARDUST SIGNAL block as in TPS § 2.6."""
    cons = consensus(model_scores, tolerance=5.0)
    model_str = "  ".join(f"{k}={int(v)}" for k, v in sorted(model_scores.items()))
    lines = [
        "STARDUST SIGNAL",
        "───────────────────────────────",
        f"Quadrant:         {quadrant}",
        f"Ticker:           {ticker}",
        f"Target return:    {target_pct}% in {weeks} weeks",
        f"Composite score:  {composite_score:.0f} / 100",
        f"Model scores:     {model_str}  — {'High' if cons == 'high' else cons.capitalize()} consensus",
        "",
        "PRIMARY SIGNALS",
    ]
    for s in primary_signals:
        lines.append(f"  • {s}")
    lines.append("")
    lines.append("RISK FACTORS")
    for r in risk_factors:
        lines.append(f"  • {r}")
    lines.extend([
        "",
        "SCENARIOS",
        f"  Best case:   +{best_pct:.1f}%   (catalyst resolves positively)",
        f"  Base case:   +{base_pct:.1f}%   (steady recovery)",
        f"  Worst case:   {worst_pct:.1f}%   (macro shock or failed catalyst)",
        "",
        f"STATUS: {status.value}",
        "───────────────────────────────",
    ])
    return "\n".join(lines)
