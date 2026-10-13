#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/.."

export SEED=42

echo "=== Fast verification checks ==="
python3 verify_convention_robustness.py
python3 scripts/validate_template.py
echo "=== All checks passed ==="
