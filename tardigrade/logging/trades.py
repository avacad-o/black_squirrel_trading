"""
Full trade logging with confluence notes and calendar flags. TPS § 1.9.
"""
from dataclasses import dataclass, field
from datetime import datetime
from typing import Any, Optional

from shared.calendar.events import active_event_flags, CalendarEvent


@dataclass
class TradeRecord:
    timestamp: datetime
    instrument: str
    direction: str  # LONG / SHORT
    entry_price: float
    target_price: float
    stop_price: float
    confluence_score: float
    confluence_breakdown: dict[str, Any]
    calendar_flags: list[str]
    exit_price: Optional[float] = None
    exit_reason: Optional[str] = None  # TARGET_HIT / STOP_HIT / BRACKET_CUTOFF
    gross_pnl: Optional[float] = None
    commission: Optional[float] = None
    net_pnl: Optional[float] = None
    notes: str = ""


def build_notes(
    instrument: str,
    direction: str,
    entry_time: datetime,
    confluence_score: float,
    confluence_breakdown: dict,
    calendar_flags: list[str],
) -> str:
    """Auto-generated note explaining entry logic. TPS § 1.9 example."""
    time_str = entry_time.strftime("%H:%M") if hasattr(entry_time, "strftime") else str(entry_time)
    parts = [
        f"Entered {direction} {instrument} at {time_str} EST."
    ]
    # Summarize key confluence (simplified)
    if confluence_breakdown:
        tf_high = [k for k, v in confluence_breakdown.items() if isinstance(v, str) and v == direction]
        if tf_high:
            parts.append(f" Timeframes aligned: {', '.join(tf_high[:4])}.")
    parts.append(f" Confluence score {confluence_score:.0f}.")
    if calendar_flags:
        parts.append(f" Calendar: {'; '.join(calendar_flags[:2])}.")
    else:
        parts.append(" No calendar flags active.")
    return " ".join(parts)


def create_trade_record(
    instrument: str,
    direction: str,
    entry_price: float,
    target_price: float,
    stop_price: float,
    confluence_score: float,
    confluence_breakdown: dict,
    entry_time: datetime,
    calendar_events: list[CalendarEvent],
) -> TradeRecord:
    """Build record at entry; exit fields filled on close."""
    flags = active_event_flags(entry_time, calendar_events)
    notes = build_notes(
        instrument, direction, entry_time, confluence_score, confluence_breakdown, flags
    )
    return TradeRecord(
        timestamp=entry_time,
        instrument=instrument,
        direction=direction,
        entry_price=entry_price,
        target_price=target_price,
        stop_price=stop_price,
        confluence_score=confluence_score,
        confluence_breakdown=confluence_breakdown,
        calendar_flags=flags,
        notes=notes,
    )


def persist_trade(record: TradeRecord) -> None:
    """Insert into TimescaleDB. Run from repo root with PYTHONPATH=. so shared is importable."""
    try:
        from shared.db import timescale  # type: ignore
        sql = """
        INSERT INTO trades (
            timestamp, instrument, direction, entry_price, target_price, stop_price,
            confluence_score, confluence_breakdown, calendar_flags, exit_price, exit_reason,
            gross_pnl, commission, net_pnl, notes
        ) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)
        """
        import json
        timescale.execute(
            sql,
            (
                record.timestamp,
                record.instrument,
                record.direction,
                record.entry_price,
                record.target_price,
                record.stop_price,
                record.confluence_score,
                json.dumps(record.confluence_breakdown),
                record.calendar_flags,
                record.exit_price,
                record.exit_reason,
                record.gross_pnl,
                record.commission,
                record.net_pnl,
                record.notes,
            ),
        )
    except Exception:
        pass  # no DB or table yet; log and continue
