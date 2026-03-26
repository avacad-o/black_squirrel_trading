"""
Redis client for internal state, position tracking, session data. TPS § 1.11.
"""
import os
from typing import Any, Optional

try:
    import redis
    _HAS_REDIS = True
except ImportError:
    _HAS_REDIS = False

_client: Optional["redis.Redis"] = None


def _get_url() -> str:
    return os.environ.get("REDIS_URL", "redis://localhost:6379")


def get_client() -> "redis.Redis":
    if not _HAS_REDIS:
        raise RuntimeError("Install redis package for Redis support")
    global _client
    if _client is None:
        _client = redis.from_url(_get_url(), decode_responses=True)
    return _client


def get(key: str, namespace: str = "bs") -> Optional[str]:
    """Get value. Keys are stored as namespace:key."""
    c = get_client()
    return c.get(f"{namespace}:{key}")


def set(key: str, value: Any, namespace: str = "bs", ex_seconds: Optional[int] = None) -> None:
    """Set value. ex_seconds = TTL."""
    c = get_client()
    k = f"{namespace}:{key}"
    if ex_seconds is not None:
        c.setex(k, ex_seconds, str(value) if not isinstance(value, str) else value)
    else:
        c.set(k, str(value) if not isinstance(value, str) else value)


def delete(key: str, namespace: str = "bs") -> None:
    c = get_client()
    c.delete(f"{namespace}:{key}")


# Tardigrade-specific namespaces
TARDIGRADE_NS = "tardigrade"
STARDUST_NS = "stardust"
