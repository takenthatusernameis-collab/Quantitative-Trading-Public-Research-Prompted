# Agentic Session Handoff

**Timestamp (UTC):** 2026-11-15T10:13:13Z
**Branch:** `main`
**Working tree:** clean except `scripts/__pycache__/`, `src/__pycache__/`, `tests/__pycache__/` (compiled bytecode, no source changes)
**Last commit:** `90fbe595 chore(kilo): checkpoint agent session`

## Context

Quantitative-strategy research repo on 2014–2026 US equities, futures, macro. Research phase complete (E001–E043); surviving validated strategies in `ledger/RESEARCH_LEDGER.md`.

Canonical artifacts: `experiments/*.json` (committed goldens). Verification never modifies them; `run_all_verification.py` backs up and restores. Offline mode enforced via `QUANT_RESEARCH_OFFLINE=1` + cache coverage pinned in `ledger/data_baseline.json`.

Key commands:
- `SEED=42 bash scripts/check.sh` — convention robustness + template validation (~seconds, offline)
- `SEED=42 python3 run_all_verification.py` — quick full verification (~8 min)
- `SEED=42 python3 run_all_verification.py --extended` — extended verification (~21 min)
- `SEED=42 python3 run_all_verification.py --full` — full verification (~15 min)

## Open item (ledger)

- E041 (min-var confirmatory): 133 remaining numeric differences are 1-ulp sensitivity of an ill-conditioned QP (`src/portfolio_opt.py`); still exceeds 1e-4 tolerance. Do **not** re-pin to silence. See ledger open item.
- Tangency QP ill-conditioned: 1-ulp input perturbation moves `min_var` answers by ~1e-05.

## Clear initial task for next session

Run the convention-robustness check first, then quick verification:

```
SEED=42 bash scripts/check.sh
SEED=42 python3 run_all_verification.py
```

If any step fails, restore artifacts before committing:
```
SEED=42 python3 run_all_verification.py --restore-only
```

Do not commit verification output. Commit only intentional source changes.
