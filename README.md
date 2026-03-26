# Black Squirrel Trading

**Confidential | Not financial advice**

Two independent systems on one server, one dashboard. No shared strategy. No cross-talk.

- **TARDIGRADE** — Micro Futures Execution Engine (automated scalping; Tradovate + Databento)
- **STARDUST** — Macro Stock Signal Engine (research/ideation; signals only, does not trade)

**Build instructions for Claude / Cursor:** read **`CLAUDE.md`** in this repo (copied from your `Downloads/CLAUDE.md`). It defines structure, env vars, packages, build order, and constraints.

Add **`BLACK_SQUIRREL_SPEC.md`** at the repo root with your full product spec if you want it versioned here (see `CLAUDE.md` § project structure).

## Repo

**[avacad-o/black_squirrel_trading](https://github.com/avacad-o/black_squirrel_trading)** (public)

To push this scaffold to the repo (from your machine, with Git installed):

```bash
cd black_squirrel_trading
git init
git remote add origin https://github.com/avacad-o/black_squirrel_trading.git
git fetch origin && git pull origin main --allow-unrelated-histories  # repo has initial README
git add . && git commit -m "Add TPS scaffold" && git push -u origin main
```

Or run `./scripts/push_to_github.sh` from the project root.

## Private web dashboard

A password-protected web UI runs from the same repo:

```bash
export DASHBOARD_PASSWORD=your-password
export SECRET_KEY=your-secret-key
./scripts/run_dashboard.sh
```

Open http://localhost:5000, log in, then use **Tardigrade** (brackets, risk, trades) and **Stardust** (4 quadrants, scores). For production, run behind HTTPS (e.g. nginx + Let’s Encrypt) on your Hetzner server. See `dashboard/README.md`.

## Project structure

```
black_squirrel_trading/
├── tardigrade/     # Execution engine
├── stardust/       # Signal engine
├── shared/         # Config, DB, cache, calendar
└── dashboard/      # Web dashboard (Flask) + Grafana configs
```

## Build sequence

Follow the 20-step build sequence in the TPS. Do not skip steps.

## Environment

Secrets via Doppler. See `docs/TPS.md` § 3.5 for required env vars.

## License

Confidential.
