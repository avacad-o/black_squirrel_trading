#!/usr/bin/env bash
# Connect this scaffold to https://github.com/avacad-o/black_squirrel_trading and push.
# Run from repo root: ./scripts/push_to_github.sh

set -e
cd "$(dirname "$0")/.."

if ! command -v git &>/dev/null; then
  echo "Install Git / Xcode Command Line Tools first: xcode-select --install"
  exit 1
fi

if [[ ! -d .git ]]; then
  git init
  git remote add origin https://github.com/avacad-o/black_squirrel_trading.git
fi

# If remote already has commits (e.g. README), pull first
if git ls-remote --exit-code origin main 2>/dev/null; then
  git fetch origin
  git branch -M main 2>/dev/null || true
  git pull origin main --allow-unrelated-histories --no-edit || true
fi

git add .
git status
echo "---"
echo "Review above. Then run:"
echo "  git commit -m 'Add TPS scaffold (Tardigrade + Stardust + shared)'"
echo "  git push -u origin main"
echo "Or run the next two lines to commit and push now:"
read -p "Commit and push? [y/N] " -n 1 -r
echo
if [[ $REPLY =~ ^[yY]$ ]]; then
  git commit -m "Add TPS scaffold (Tardigrade + Stardust + shared)"
  git push -u origin main
  echo "Done. See https://github.com/avacad-o/black_squirrel_trading"
fi
