"""
Doppler secrets management. TPS § 3.5.

Load env from Doppler (or fallback to os.environ). All API keys and credentials.
"""
import os
from typing import Optional


def get_secret(name: str, default: Optional[str] = None) -> Optional[str]:
    """Return secret from environment (Doppler injects into env in production)."""
    return os.environ.get(name, default)


def get_required(name: str) -> str:
    """Return secret or raise if missing."""
    val = os.environ.get(name)
    if not val:
        raise RuntimeError(f"Missing required env var: {name}")
    return val


# TPS § 3.5 — convenience accessors (call get_secret/get_required as needed)
def tardigrade_env() -> dict[str, str]:
    """Tradovate + Databento keys."""
    return {
        "TRADOVATE_API_KEY": get_secret("TRADOVATE_API_KEY") or "",
        "TRADOVATE_API_SECRET": get_secret("TRADOVATE_API_SECRET") or "",
        "TRADOVATE_ACCOUNT_ID": get_secret("TRADOVATE_ACCOUNT_ID") or "",
        "TRADOVATE_ENV": get_secret("TRADOVATE_ENV", "sim") or "sim",
        "DATABENTO_API_KEY": get_secret("DATABENTO_API_KEY") or "",
    }


def stardust_env() -> dict[str, str]:
    """Polygon, FMP, Unusual Whales, Reddit, Anthropic."""
    return {
        "POLYGON_API_KEY": get_secret("POLYGON_API_KEY") or "",
        "FMP_API_KEY": get_secret("FMP_API_KEY") or "",
        "UNUSUAL_WHALES_API_KEY": get_secret("UNUSUAL_WHALES_API_KEY") or "",
        "REDDIT_CLIENT_ID": get_secret("REDDIT_CLIENT_ID") or "",
        "REDDIT_CLIENT_SECRET": get_secret("REDDIT_CLIENT_SECRET") or "",
        "ANTHROPIC_API_KEY": get_secret("ANTHROPIC_API_KEY") or "",
    }


def shared_env() -> dict[str, str]:
    """TimescaleDB, Redis, Grafana."""
    return {
        "TIMESCALE_URL": get_secret("TIMESCALE_URL") or "",
        "REDIS_URL": get_secret("REDIS_URL", "redis://localhost:6379") or "redis://localhost:6379",
        "GRAFANA_ADMIN_PASSWORD": get_secret("GRAFANA_ADMIN_PASSWORD") or "",
    }
