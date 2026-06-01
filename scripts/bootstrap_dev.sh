#!/usr/bin/env bash
# Bootstrap development environment
set -euo pipefail

uv sync

echo ""
echo "MCUflow-Edge development environment ready."
echo "Run 'uv run pytest tests/' to verify."
