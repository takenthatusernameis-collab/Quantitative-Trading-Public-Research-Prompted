# Initial Task — Next Agentic Work Session

**Timestamp (UTC):** 2026-11-16T11:37:52Z
**Project:** Quantitative-Trading-Public-Research-Prompted
**Status:** Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Baseline / integrity (do first)

1. **Check working tree:** `git status --short` — expect only incidental `__pycache__/*.pyc` modifications; do not commit them. There must be no tracked `experiments/` diffs and no pending `.verify_snapshot/`.
2. **Fast gate:** `SEED=42 bash scripts/check.sh` (or `make check`). Fix any golden/baseline mismatch **before** committing; never re-pin baselines as a side effect of verification.
3. **Recovery if needed:** `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`). If `HEAD` already carries a captured run, restore pinned artifacts per `ledger/golden_baseline.json`.

## Known state / open items

- `experiments/*.json` are canonical golden artifacts; verification overwrites and restores them — never leave a run half-finished.
- E041 optimizer determinism was addressed (E049): extended drift reduced (354→133 numeric diffs, 3 structural diffs removed) but remaining 1-ulp/ill-conditioned QP sensitivity still exceeds tolerance in extended checks. **Do not re-pin E041/E042 grid artifacts** to silence drift (see ledger open item / E049).
- E029/E030 inputs are pinned and offline-reproducible (E045/E048). Cache coverage enforced by `scripts/check_data_coverage.py` + `QUANT_RESEARCH_OFFLINE=1` in verification.
- CI workflow template: `.github/workflow-templates/verification-gate.yml` (maintainer must create via GitHub UI).

## Suggested verification commands

```bash
SEED=42 bash scripts/check.sh          # fast, offline
SEED=42 python3 run_all_verification.py            # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended # ~21 min
SEED=42 python3 run_all_verification.py --full     # ~15 min
```

## Next-session guidance

- Start by running `scripts/check.sh` and reviewing `ledger/RESEARCH_LEDGER.md` for current decisions/open items.
- Treat pre-registration, promotion gates, and negative-result recording as binding project conventions.
- If you run any verification driver, ensure artifacts are restored/clean before ending the session and leaving a new timestamped handoff.
