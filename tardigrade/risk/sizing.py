"""
Position sizing by account tier. TPS § 1.5.

Tiers: $500–999 → 1; $1k–2.5k → 1–2; $2.5k–5k → 2–3; $5k–10k → 3–5; $10k+ → 5–10.
Commission-aware: min size must clear round-trip commission and spread.
"""
from typing import Tuple

# (min_balance, max_balance, min_contracts, max_contracts)
TIERS: list[Tuple[float, float, int, int]] = [
    (500, 999, 1, 1),
    (1000, 2499, 1, 2),
    (2500, 4999, 2, 3),
    (5000, 9999, 3, 5),
    (10000, 1e9, 5, 10),
]


def contracts_for_balance(account_balance: float) -> Tuple[int, int]:
    """Return (min_contracts, max_contracts) for the account tier."""
    for lo, hi, cmin, cmax in TIERS:
        if lo <= account_balance <= hi:
            return (cmin, cmax)
    return (1, 1)


def round_trip_commission_per_contract() -> float:
    """Placeholder: replace with real broker round-trip. Used to check min viable size."""
    return 1.0  # example $1 R/T


def min_viable_contracts(
    account_balance: float,
    target_pct_per_trade: float = 0.15,
    round_trip_commission: float | None = None,
) -> int:
    """
    Minimum contracts so that net profit (after commission) still meets target %.
    Simplification: target_pct applies to notional at risk; commission must be covered.
    """
    comm = round_trip_commission or round_trip_commission_per_contract()
    cmin, cmax = contracts_for_balance(account_balance)
    # Gross needed to cover commission and hit target: gross - comm * n >= target_pct * risk_per_contract * n
    # For now return tier min; plug in real tick value and commission in production.
    return cmin
