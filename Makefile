.PHONY: check verify verify-full

check:
	SEED=42 bash scripts/check.sh

verify:
	SEED=42 python3 verify_convention_robustness.py

verify-full:
	SEED=42 python3 run_all_verification.py --full
