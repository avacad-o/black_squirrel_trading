"""
Black Squirrel Trading — private web dashboard.

Run from repo root: python -m flask --app dashboard.app run --host 0.0.0.0 --port 5000
Set DASHBOARD_PASSWORD and SECRET_KEY in env. Use HTTPS in production.
"""
import os
import sys
from pathlib import Path

# Ensure repo root is on path so tardigrade, stardust, shared import
_root = Path(__file__).resolve().parent.parent
if str(_root) not in sys.path:
    sys.path.insert(0, str(_root))
from datetime import datetime
from functools import wraps

from flask import Flask, redirect, render_template, request, session, url_for

app = Flask(__name__, static_folder="static", template_folder="templates")
app.secret_key = os.environ.get("SECRET_KEY", "change-me-in-production")
app.config["SESSION_COOKIE_HTTPONLY"] = True
app.config["SESSION_COOKIE_SAMESITE"] = "Lax"

DASHBOARD_PASSWORD = os.environ.get("DASHBOARD_PASSWORD", "squirrel")


def login_required(f):
    @wraps(f)
    def wrapped(*args, **kwargs):
        if not session.get("logged_in"):
            return redirect(url_for("login"))
        return f(*args, **kwargs)
    return wrapped


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        if request.form.get("password") == DASHBOARD_PASSWORD:
            session["logged_in"] = True
            return redirect(url_for("index"))
    return render_template("login.html")


@app.route("/logout")
def logout():
    session.pop("logged_in", None)
    return redirect(url_for("login"))


@app.route("/")
@login_required
def index():
    return render_template("index.html")


@app.route("/tardigrade")
@login_required
def tardigrade():
    from tardigrade.execution.brackets import (
        get_current_bracket,
        can_enter_new_trade,
        minutes_remaining,
        BRACKETS,
    )
    from tardigrade.risk.streaks import streak_action, StreakAction
    from tardigrade.risk.limits import DAILY_TARGET

    # Use EST-like time for display (naive; in production use zoneinfo)
    now = datetime.utcnow()
    # Approximate EST = UTC - 5 (no DST here for simplicity)
    from datetime import timedelta
    est = now - timedelta(hours=5)

    bracket = get_current_bracket(est)
    can_enter = can_enter_new_trade(est)
    mins_left = minutes_remaining(est)

    # Mock streak for demo; in production read from Redis/DB
    streak = streak_action([])

    return render_template(
        "tardigrade.html",
        now_est=est.strftime("%H:%M:%S"),
        bracket_name=bracket.name.value if bracket else "—",
        can_enter=can_enter,
        minutes_remaining=mins_left,
        streak_action=streak.value,
        daily_target=DAILY_TARGET,
        brackets=[(b.name.value, b.start, b.end) for b in BRACKETS],
        recent_trades=[],  # from DB when available
    )


@app.route("/stardust")
@login_required
def stardust():
    from stardust.scoring.composite import composite_score
    from stardust.signals.threshold import status_from_score, SignalStatus

    # Mock 4 quadrants; in production load from DB/Redis
    quadrants = [
        {"name": "REMNANT", "subtitle": "Battered Recovery", "ticker": "—", "score": 0, "status": SignalStatus.ANALYZING_DATA},
        {"name": "STASIS", "subtitle": "Sleeper", "ticker": "—", "score": 0, "status": SignalStatus.ANALYZING_DATA},
        {"name": "SMOLDER", "subtitle": "Slow Burner", "ticker": "—", "score": 0, "status": SignalStatus.ANALYZING_DATA},
        {"name": "ROGUE", "subtitle": "Wild Card", "ticker": "—", "score": 0, "status": SignalStatus.ANALYZING_DATA},
    ]
    # Demo: one quadrant with mock score
    sigs = {n: 68.0 for n in ["insider", "institutional", "options", "technical", "fundamental", "sentiment", "analyst"]}
    blended, per_model = composite_score(sigs)
    quadrants[0]["ticker"] = "EXAMPLE"
    quadrants[0]["score"] = int(blended)
    quadrants[0]["status"] = status_from_score(blended)

    return render_template(
        "stardust.html",
        quadrants=quadrants,
        signal_text=None,  # last generated signal block when available
    )


@app.route("/api/refresh-stardust", methods=["POST"])
@login_required
def refresh_stardust():
    # Placeholder: trigger Stardust rescan (queue job or run in background)
    return {"ok": True, "message": "Refresh queued"}


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=os.environ.get("FLASK_DEBUG", "0") == "1")
