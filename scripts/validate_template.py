#!/usr/bin/env python3
import sys
from pathlib import Path

root = Path(__file__).parent.parent
tpl = root / ".github" / "workflow-templates" / "verification-gate.yml"
txt = tpl.read_text()
# basic sanity checks
assert "Verification Gate" in txt
assert "run_all_verification.py" in txt
assert "--full" in txt
print("OK")
sys.exit(0)
