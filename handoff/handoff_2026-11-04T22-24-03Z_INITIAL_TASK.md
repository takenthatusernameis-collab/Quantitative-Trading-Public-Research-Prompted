# Durable Handoff — Initial Task Message

**Timestamp:** 2026-11-05T00:23:52Z
**From:** main agent (kilo-auto/free)
**Session:** ses_e56e8d6cdffeBuA8nQL3cfCgUJ

---

## Context

Repository: `Quantitative-Trading-Public-Research-Prompted` — independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data.

- Research phase (E001–E043) is **complete**.
- Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.
- All experiments are pre-registered with falsification expectations and promotion gates.

## Current State

- No active task in progress.
- Board has no peer participants beyond `main` (this session).
- Verification suite (`run_all_verification.py`) backs up `experiments/*.json` goldens before re-running and restores them afterward. **Never leave a verification run half-finished.**
- Baseline integrity is enforced by `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py`.

## Instructions for Next Session

1. **Read the assigned objective** — if none is given, confirm state via `AGENTS.md` and `ledger/RESEARCH_LEDGER.md`.
2. **Reproduce/verify first** — run `SEED=42 bash scripts/check.sh` (fast) before making changes.
3. **Preserve goldens** — any verification re-run must complete or be recovered with `SEED=42 python3 run_all_verification.py --restore-only`.
4. **Follow conventions** — close-to-close is the v1.2.3 primary convention; use `SEED=42`; offline mode `QUANT_RESEARCH_OFFLINE=1` for reproducibility.
5. **Do not commit** unless explicitly asked.

## Useful Commands

```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 run_all_verification.py --extended
SEED=42 python3 run_all_verification.py --restore-only
SEED=42 python3 run_all_verification.py --full
```

## Open Items

- None flagged. New work requires a driver under `experiments/` with a pre-registered JSON block and falsification expectations.