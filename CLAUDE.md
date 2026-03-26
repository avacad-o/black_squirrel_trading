# CLAUDE.md
## Black Squirrel Trading — Claude Code Instructions

This file tells Claude Code exactly how to build this project. Read it fully before writing any code.

---

## WHO YOU ARE

You are the lead engineer building Black Squirrel Trading, a private algorithmic trading platform. You write clean, production-ready Python. You never skip error handling. You never hardcode secrets. You always use the packages specified. You build one file at a time, test it, then move to the next.

---

## WHAT YOU ARE BUILDING

Two completely independent Python systems that share infrastructure but never share strategy or data.

### TARDIGRADE
Automated micro-scalping engine for MCL (Micro WTI Crude Oil futures). Trades one instrument only. Reads price, volume, and time. No news, no fundamentals, no external signals. Executes through Tradovate API. Runs 24/7 on Hetzner server.

### STARDUST
Macro stock research and ideation engine. Monitors 4 stocks across 4 thesis types (REMNANT, STASIS, SMOLDER, ROGUE). Ingests broad data from 6 sources, scores each stock using 4 weighted models, outputs probability-weighted trade ideas and push notifications. Does not execute trades. User decides when to act.

---

## PROJECT STRUCTURE

Build exactly this structure. Do not add files not listed here without asking first.

```
black-squirrel/
│
├── CLAUDE.md                         ← this file
├── BLACK_SQUIRREL_SPEC.md            ← full product spec, reference for all decisions
├── .env.example                      ← template showing all required env vars, no values
├── requirements.txt                  ← all Python dependencies
├── docker-compose.yml                ← TimescaleDB, Redis, Grafana, Loki
│
├── tardigrade/
│   ├── __init__.py
│   ├── main.py                       ← entry point, starts all bracket loops
│   ├── data/
│   │   ├── __init__.py
│   │   └── databento_feed.py         ← MCL tick data stream from Databento
│   ├── strategy/
│   │   ├── __init__.py
│   │   ├── candles.py                ← builds OHLCV candles from tick data
│   │   ├── indicators.py             ← Bollinger Bands, EMA, RSI using pandas-ta
│   │   ├── timeframes.py             ← evaluates all 7 timeframes, returns signal per TF
│   │   ├── confluence.py             ← applies weights, returns 0-100 score + direction
│   │   └── calendar.py               ← market calendar, EIA dates, session flags
│   ├── execution/
│   │   ├── __init__.py
│   │   ├── tradovate.py              ← Tradovate REST API client (auth, orders, positions)
│   │   ├── orders.py                 ← place, modify, cancel orders
│   │   └── brackets.py               ← time bracket enforcement, cutoff logic
│   ├── risk/
│   │   ├── __init__.py
│   │   ├── sizing.py                 ← contract count by account tier
│   │   ├── streaks.py                ← win/loss streak tracking and halt rules
│   │   └── limits.py                 ← daily target, max drawdown, cycle halt logic
│   └── logging/
│       ├── __init__.py
│       └── trade_logger.py           ← logs every trade to TimescaleDB with full context
│
├── stardust/
│   ├── __init__.py
│   ├── main.py                       ← entry point, starts all scheduled scraping jobs
│   ├── ingestion/
│   │   ├── __init__.py
│   │   ├── polygon.py                ← Polygon.io client: price, volume, news, options
│   │   ├── edgar.py                  ← SEC EDGAR: 10-K, 10-Q, 8-K, insider transactions, 13F
│   │   ├── fmp.py                    ← Financial Modeling Prep: earnings, analysts, ownership
│   │   ├── unusual_whales.py         ← Unusual Whales: options flow, institutional signals
│   │   └── reddit.py                 ← Reddit (praw): sentiment, post velocity
│   ├── nlp/
│   │   ├── __init__.py
│   │   └── synthesizer.py            ← Anthropic API: summarizes filings, generates thesis
│   ├── scoring/
│   │   ├── __init__.py
│   │   ├── models.py                 ← 4 weighted scoring variants (A, B, C, D)
│   │   ├── composite.py              ← blended score + individual model outputs
│   │   └── events.py                 ← external event weight adjustments
│   ├── signals/
│   │   ├── __init__.py
│   │   ├── threshold.py              ← signal activation: NOT IN SIGHT / IN SIGHT / ACTIVATED
│   │   ├── scenarios.py              ← best/base/worst case generator
│   │   └── alerts.py                 ← push notification triggers on status change
│   └── tracking/
│       ├── __init__.py
│       └── history.py                ← signal history, misfire logging, track record
│
├── shared/
│   ├── __init__.py
│   ├── config.py                     ← loads all env vars via Doppler or .env
│   ├── db/
│   │   ├── __init__.py
│   │   ├── timescale.py              ← TimescaleDB connection pool
│   │   └── migrations/
│   │       ├── 001_tardigrade_trades.sql
│   │       ├── 002_tardigrade_candles.sql
│   │       ├── 003_stardust_signals.sql
│   │       └── 004_stardust_scores.sql
│   ├── cache/
│   │   ├── __init__.py
│   │   └── redis_client.py           ← Redis connection, get/set helpers
│   └── calendar/
│       ├── __init__.py
│       └── market_events.py          ← EIA dates, Fed dates, market hours
│
└── dashboard/
    ├── tardigrade/
    │   └── grafana_dashboard.json    ← Grafana dashboard config for Tardigrade
    └── stardust/
        └── grafana_dashboard.json    ← Grafana dashboard config for Stardust
```

---

## ENVIRONMENT VARIABLES

Never hardcode any of these. Always load from environment via `shared/config.py`.

```
# Tardigrade
TRADOVATE_API_KEY
TRADOVATE_API_SECRET
TRADOVATE_ACCOUNT_ID
TRADOVATE_ENV                # "sim" or "live" — default to "sim"

DATABENTO_API_KEY

# Stardust
POLYGON_API_KEY
FMP_API_KEY
UNUSUAL_WHALES_API_KEY
REDDIT_CLIENT_ID
REDDIT_CLIENT_SECRET
REDDIT_USER_AGENT
ANTHROPIC_API_KEY

# Shared infrastructure
TIMESCALE_URL                # postgresql://user:pass@localhost:5432/black_squirrel
REDIS_URL                    # redis://localhost:6379
REDIS_PASSWORD

# Dashboard
GRAFANA_ADMIN_PASSWORD
```

---

## REQUIRED PACKAGES

Use exactly these packages. Do not substitute without asking.

```
# Data & Analysis
databento
pandas
numpy
pandas-ta

# Broker
requests                     # Tradovate REST API via HTTP

# Stardust data sources
polygon-api-client
praw
anthropic

# Infrastructure
psycopg2-binary
redis
apscheduler
schedule
python-dotenv

# Utilities
loguru                       # logging
httpx                        # async HTTP where needed
```

---

## CODING STANDARDS

Follow these exactly. Do not deviate.

### Error handling
- Every external API call wrapped in try/except
- Log the error with full context using loguru
- Never let an unhandled exception kill the main process
- Tardigrade: on any execution error, cancel all open orders and wait for next bracket
- Stardust: on any ingestion error, skip that source and continue with remaining sources

### Logging
- Use loguru for all logging, not print statements
- Log format: `{time} | {level} | {module} | {message}`
- Every trade entry and exit logged at INFO level
- Every API error logged at ERROR level with full traceback
- Every calendar flag logged at WARNING level

### Secrets
- Load all secrets in `shared/config.py` using `os.environ.get()`
- Raise a clear error at startup if any required secret is missing
- Never log secret values

### Database
- All TimescaleDB writes use parameterized queries, never string formatting
- All tables use hypertables (TimescaleDB time-series optimization)
- Connection pool managed in `shared/db/timescale.py`, imported everywhere

### Testing
- After building each file, write a simple `if __name__ == "__main__"` test block
- Test with real API calls where possible (Tradovate sim, Databento free tier)
- Never mock external APIs in the test blocks — test against real endpoints

---

## BUILD ORDER

Build in exactly this sequence. Complete and test each step before moving to the next. Do not skip ahead.

### PHASE 1 — Foundation
1. `shared/config.py` — env var loader with validation
2. `shared/db/timescale.py` — database connection pool
3. `shared/cache/redis_client.py` — Redis client
4. `shared/db/migrations/` — all 4 SQL migration files
5. `docker-compose.yml` — TimescaleDB, Redis, Grafana, Loki
6. `requirements.txt` — all dependencies
7. `.env.example` — all required vars with placeholder values

### PHASE 2 — Tardigrade Core
8. `shared/calendar/market_events.py` — EIA dates, Fed dates, session times
9. `tardigrade/data/databento_feed.py` — MCL tick stream
10. `tardigrade/strategy/candles.py` — build OHLCV candles from ticks
11. `tardigrade/strategy/indicators.py` — Bollinger, EMA, RSI
12. `tardigrade/strategy/timeframes.py` — signal per timeframe
13. `tardigrade/strategy/confluence.py` — weighted score 0-100
14. `tardigrade/strategy/calendar.py` — calendar flag injection

### PHASE 3 — Tardigrade Execution
15. `tardigrade/execution/tradovate.py` — REST API client
16. `tardigrade/execution/orders.py` — place/cancel/modify
17. `tardigrade/execution/brackets.py` — time bracket enforcement
18. `tardigrade/risk/sizing.py` — contract count by account size
19. `tardigrade/risk/streaks.py` — win/loss streak rules
20. `tardigrade/risk/limits.py` — daily target, drawdown, halt
21. `tardigrade/logging/trade_logger.py` — full trade log to TimescaleDB
22. `tardigrade/main.py` — wire everything together, start bracket loops

### PHASE 4 — Stardust Ingestion
23. `stardust/ingestion/polygon.py` — price, volume, news, options
24. `stardust/ingestion/edgar.py` — filings, insider transactions, 13F
25. `stardust/ingestion/fmp.py` — earnings, analysts, ownership
26. `stardust/ingestion/unusual_whales.py` — options flow
27. `stardust/ingestion/reddit.py` — sentiment scraper

### PHASE 5 — Stardust Intelligence
28. `stardust/nlp/synthesizer.py` — Anthropic API synthesis with prompt caching
29. `stardust/scoring/models.py` — 4 weighted model variants
30. `stardust/scoring/composite.py` — blended score
31. `stardust/scoring/events.py` — event weight adjustments
32. `stardust/signals/threshold.py` — status transition logic
33. `stardust/signals/scenarios.py` — best/base/worst
34. `stardust/signals/alerts.py` — push notifications
35. `stardust/tracking/history.py` — signal history and misfires
36. `stardust/main.py` — wire everything, start scheduled jobs

### PHASE 6 — Dashboard
37. `dashboard/tardigrade/grafana_dashboard.json`
38. `dashboard/stardust/grafana_dashboard.json`

---

## TARDIGRADE LOGIC REFERENCE

### Time Brackets (EST)
- Pre-Market: 07:00–09:15 | cutoff 09:12
- Open: 09:45–10:30 | cutoff 10:27
- Close: 15:00–16:00 | cutoff 15:57
- London: 02:00–04:00 | cutoff 03:57

### Confluence Weights
- 1 Day: 20%
- 4 Hour: 18%
- 1 Hour: 15%
- 30 Min: 13%
- 15 Min: 12%
- 5 Min: 12%
- 3 Min: 10%

### Score Thresholds
- >= 65: execute
- < 65: skip, wait for next candle

### Signals Per Timeframe
- Bollinger Band position (above mid / below mid / outside upper / outside lower)
- Consecutive candle count (greens or reds)
- Volume vs 20-period average
- Price vs 20 EMA and 50 EMA
- RSI zone (oversold < 35 / neutral 35–65 / overbought > 65)

### Position Sizing
- $500–$999: 1 contract
- $1,000–$2,499: 1–2 contracts
- $2,500–$4,999: 2–3 contracts
- $5,000–$9,999: 3–5 contracts
- $10,000+: 5–10 contracts

### Risk Rules
- 3 consecutive losses → pause until next bracket
- 3 consecutive wins → continue until first loss, then stop
- Daily target hit → stop all trading
- $500 drawdown in cycle → stop, full review
- 3 losing cycles → halt program

### Trade Target
- Primary: 0.15% per trade
- Win/risk ratio: 1:1.3
- MCL round-trip commission: ~$1.70

---

## STARDUST LOGIC REFERENCE

### Four Quadrants
- REMNANT: battered recovery, medium risk, 4–12 weeks
- STASIS: sleeper, low-medium risk, 6–20 weeks
- SMOLDER: slow burner, low risk, 4–10 weeks
- ROGUE: wild card, high risk, 8–20 weeks

### Stock Base Criteria
- Market cap $500M–$10B
- Volume 500K+ shares/day
- NYSE or NASDAQ only
- Price > $5.00
- Not S&P 500 member

### Scoring Model Weights
```
Signal              | Model A | Model B | Model C | Model D
Insider Activity    |   20%   |   15%   |   10%   |   25%
Institutional Flow  |   18%   |   20%   |   15%   |   20%
Options Flow        |   15%   |   20%   |   10%   |   15%
Technical Score     |   15%   |   10%   |   25%   |   10%
Fundamental Score   |   12%   |   15%   |   20%   |   10%
Sentiment Score     |   10%   |   10%   |   10%   |   10%
Analyst Revisions   |   10%   |   10%   |   10%   |   10%
```

### Signal Status States
- ANALYZING: system running, no threshold crossed
- NOT IN SIGHT: score below threshold (red)
- IN SIGHT: score approaching threshold (yellow)
- ACTIVATED: score crossed threshold (green)

### External Event Weights
- Fed rate decision: ±15%
- CPI / Jobs: ±10%
- Earnings: ±20%
- Election / policy: ±15%
- Geopolitical shock: ±25%
- Industry regulation: ±12%

### Anthropic API Usage
- Enable prompt caching on all document analysis calls
- System prompt: "You are a financial research analyst. Output structured JSON only."
- Always request JSON output, parse with try/except
- Max tokens: 1000 per call
- Use claude-sonnet-4-5 model

---

## DATABASE SCHEMA REFERENCE

### tardigrade_trades
```sql
CREATE TABLE tardigrade_trades (
    time            TIMESTAMPTZ NOT NULL,
    instrument      TEXT NOT NULL,
    direction       TEXT NOT NULL,
    contracts       INT NOT NULL,
    entry_price     NUMERIC NOT NULL,
    exit_price      NUMERIC,
    target_price    NUMERIC NOT NULL,
    stop_price      NUMERIC NOT NULL,
    confluence_score NUMERIC NOT NULL,
    timeframe_scores JSONB,
    calendar_flags  JSONB,
    exit_reason     TEXT,
    gross_pnl       NUMERIC,
    commission      NUMERIC,
    net_pnl         NUMERIC,
    bracket         TEXT NOT NULL,
    notes           TEXT
);
SELECT create_hypertable('tardigrade_trades', 'time');
```

### tardigrade_candles
```sql
CREATE TABLE tardigrade_candles (
    time        TIMESTAMPTZ NOT NULL,
    timeframe   TEXT NOT NULL,
    open        NUMERIC NOT NULL,
    high        NUMERIC NOT NULL,
    low         NUMERIC NOT NULL,
    close       NUMERIC NOT NULL,
    volume      NUMERIC NOT NULL
);
SELECT create_hypertable('tardigrade_candles', 'time');
```

### stardust_signals
```sql
CREATE TABLE stardust_signals (
    time            TIMESTAMPTZ NOT NULL,
    ticker          TEXT NOT NULL,
    quadrant        TEXT NOT NULL,
    composite_score NUMERIC NOT NULL,
    model_a_score   NUMERIC,
    model_b_score   NUMERIC,
    model_c_score   NUMERIC,
    model_d_score   NUMERIC,
    status          TEXT NOT NULL,
    target_return   NUMERIC,
    target_weeks    INT,
    thesis          TEXT,
    scenarios       JSONB,
    risk_factors    JSONB,
    actual_return   NUMERIC,
    misfire         BOOLEAN DEFAULT FALSE,
    notes           TEXT
);
SELECT create_hypertable('stardust_signals', 'time');
```

### stardust_scores
```sql
CREATE TABLE stardust_scores (
    time                TIMESTAMPTZ NOT NULL,
    ticker              TEXT NOT NULL,
    insider_score       NUMERIC,
    institutional_score NUMERIC,
    options_score       NUMERIC,
    technical_score     NUMERIC,
    fundamental_score   NUMERIC,
    sentiment_score     NUMERIC,
    analyst_score       NUMERIC,
    raw_data            JSONB
);
SELECT create_hypertable('stardust_scores', 'time');
```

---

## HARD CONSTRAINTS

These rules are non-negotiable. Never violate them.

### Tardigrade
- TRADOVATE_ENV must default to "sim" — never default to "live"
- Never hold a position across bracket boundaries
- Never enter with less than 3 minutes left in bracket
- Never trade more than one position simultaneously
- Never override the 3-loss halt rule
- Never skip commission in P&L calculations
- Always log the confluence score breakdown with every trade

### Stardust
- Never output a buy or sell recommendation — output probability scores and signals only
- Never activate a signal with less than 2 weeks of data
- Never skip a source error silently — always log it
- Never delete signal history — misfires stay in the record
- Always run misfire post-mortem when actual_return < 0 on an ACTIVATED signal

---

## HOW TO START

When Claude Code opens this project, the first message should be:

"I have read CLAUDE.md. I understand I am building Black Squirrel Trading — two independent systems, Tardigrade and Stardust. I will follow the build order in CLAUDE.md exactly, starting with Phase 1. Ready to begin with shared/config.py?"

Then wait for confirmation before writing any code.

---

*Black Squirrel Trading | v1.1 | Confidential | Not financial advice*
