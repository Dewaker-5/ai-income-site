#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"
set -a; source .env; set +a
source venv/bin/activate

echo "=== Agent 5: Sending weekly Telegram report ==="
python agent5_reporter.py

echo "Weekly report sent."
