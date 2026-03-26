"""
Signal activation logic. TPS § 2.11.

States: ANALYZING_DATA | TARGET_NOT_IN_SIGHT | TARGET_ACTION_IN_SIGHT | TARGET_ACTION_ACTIVATED.
"""
from enum import Enum
from typing import Optional


class SignalStatus(str, Enum):
    ANALYZING_DATA = "ANALYZING_DATA"
    TARGET_NOT_IN_SIGHT = "TARGET_NOT_IN_SIGHT"
    TARGET_ACTION_IN_SIGHT = "TARGET_ACTION_IN_SIGHT"
    TARGET_ACTION_ACTIVATED = "TARGET_ACTION_ACTIVATED"


def status_from_score(
    composite_score: float,
    activation_threshold: float = 70.0,
    in_sight_threshold: float = 60.0,
) -> SignalStatus:
    """
    activation_threshold: score >= this => TARGET_ACTION_ACTIVATED (green).
    in_sight_threshold: score >= this => TARGET_ACTION_IN_SIGHT (yellow).
    Below in_sight => TARGET_NOT_IN_SIGHT (red).
    """
    if composite_score >= activation_threshold:
        return SignalStatus.TARGET_ACTION_ACTIVATED
    if composite_score >= in_sight_threshold:
        return SignalStatus.TARGET_ACTION_IN_SIGHT
    if composite_score >= 0:
        return SignalStatus.TARGET_NOT_IN_SIGHT
    return SignalStatus.ANALYZING_DATA
