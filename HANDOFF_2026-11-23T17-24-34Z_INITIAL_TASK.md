# Agentic Work Session Handoff — 2026-11-23T17:24:34Z

**Timestamp**: 2026-11-23T17:24:34Z
**HEAD**: `8eb64d65b4ca5660a8b6953bde68ec14143c16aa` on `main` (== `origin/main`)
**Project**: Quantitative-Trading-Public-Research-Prompted
**Research phase**: COMPLETE (E001–E043). Surviving validated strategies in `ledger/RESEARCH_LEDGER.md`.

---

## Initial task for next session

Run the full verification suite (the actual open item), not another handoff refresh.

```bash
pip install -r requirements.txt
SEED=42 python3 run_all_verification.py --extended   # ~21 min
```

Report drift precisely (`.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json`). Do NOT re-pin to silence. Confirm `git status` clean afterward (use `--restore-only` if it dies).

Then address E049/E050 QP drift if present, and propose (do NOT execute) the handoff-cleanup plan. Do not invent post-hoc experiments.

## Critical invariants

1. Baseline integrity: never leave a verification run half-finished; recover with `--restore-only`.
2. Cache coverage: every `data.download()` must have a committed, SHA-256-pinned cache file.
3. Convention: close-to-close is v1.2.3 primary; overnight reported alongside.
4. Seed: always `SEED=42`.
5. Optimizer determinism: validate on problem constraints, never solver exit status.
6. Do NOT re-pin E041/E042 goldens to silence tolerance violations.

## Quick reference

```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 run_all_verification.py --extended
SEED=42 python3 run_all_verification.py --restore-only
```

*Handoff. If you are about to write another handoff without doing step 1 above, stop — that is the degenerate loop.*
