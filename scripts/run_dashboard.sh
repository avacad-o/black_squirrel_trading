#!/usr/bin/env bash
# Run the private dashboard. From repo root: ./scripts/run_dashboard.sh
set -e
cd "$(dirname "$0")/.."
export DASHBOARD_PASSWORD="${DASHBOARD_PASSWORD:-squirrel}"
export SECRET_KEY="${SECRET_KEY:-change-me}"
echo "Dashboard at http://127.0.0.1:5000 — password: \$DASHBOARD_PASSWORD"
exec python3 -m flask --app dashboard.app run --host 0.0.0.0 --port 5000
