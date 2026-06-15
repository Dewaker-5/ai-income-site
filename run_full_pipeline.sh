#!/usr/bin/env bash
set -e

cd "$(dirname "$0")"
set -a; source .env; set +a
source venv/bin/activate

echo "=== Agent 1: Researching keywords ==="
python agent1_researcher.py

echo ""
echo "=== Agent 2: Writing articles ==="
python agent2_writer.py

echo ""
echo "=== Agent 3: Publishing articles ==="
python agent3_publisher.py

echo ""
echo "=== Agent 4: Fetching traffic data ==="
python agent4_tracker.py

echo ""
echo "Full pipeline completed."
