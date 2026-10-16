#!/bin/bash
set -euo pipefail
cd "$(dirname "$0")/.."

export SEED=42

echo "=== Fast verification checks ==="
python3 scripts/check_json_artifacts.py
python3 verify_convention_robustness.py
python3 scripts/validate_template.py
python3 scripts/check_experiment_imports.py
echo "=== All checks passed ==="
