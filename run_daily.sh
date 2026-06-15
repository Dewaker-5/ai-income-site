#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"
set -a; source .env; set +a
source venv/bin/activate

echo "=== Agent 3: Publishing articles ==="
python agent3_publisher.py

echo ""
echo "=== Agent 4: Fetching traffic data ==="
python agent4_tracker.py

echo ""
echo "All agents completed."
