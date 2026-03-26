"""
Data structures for Stardust ingestion. TPS § 2.3–2.5.
"""
from dataclasses import dataclass, field
from typing import Any, Optional


@dataclass
class StockUniverse:
    """Base criteria + quadrant filter. TPS § 2.3."""
    symbol: str
    market_cap: float
    avg_daily_volume: float
    price: float
    quadrant: str  # REMNANT | STASIS | SMOLDER | ROGUE
    tier: int = 1  # 1–4


@dataclass
class SignalInputs:
    """Raw scores 0–100 per signal layer for composite. TPS § 2.5."""
    insider: float = 0.0
    institutional: float = 0.0
    options: float = 0.0
    technical: float = 0.0
    fundamental: float = 0.0
    sentiment: float = 0.0
    analyst: float = 0.0

    def to_dict(self) -> dict[str, float]:
        return {
            "insider": self.insider,
            "institutional": self.institutional,
            "options": self.options,
            "technical": self.technical,
            "fundamental": self.fundamental,
            "sentiment": self.sentiment,
            "analyst": self.analyst,
        }
