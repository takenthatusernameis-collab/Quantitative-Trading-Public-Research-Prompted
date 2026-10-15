.PHONY: check verify verify-quick verify-extended verify-full

check:
	SEED=42 bash scripts/check.sh

verify:
	SEED=42 python3 verify_convention_robustness.py

verify-quick:
	SEED=42 python3 run_all_verification.py

verify-extended:
	SEED=42 python3 run_all_verification.py --extended

verify-full:
	SEED=42 python3 run_all_verification.py --full
