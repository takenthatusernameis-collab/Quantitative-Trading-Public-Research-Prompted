# INITIAL TASK - Handoff for Next Agent Session

**Timestamp (UTC): 2026-11-04T02-07-36Z**
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** main — 7b5e86a90add297ba6e365c6941f55265fc4a6b3
**Origin/HEAD:** origin/main — 5a76acb978c4868134d947b7c268311d4e17618f
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Working Tree:** 16 modified tracked files (all `**/__pycache__/*.pyc`)

## ⚠ Live verification snapshot pending recovery

`.verify_snapshot/ACTIVE.json` exists (timestamped 2026-11-04T01:07) — a prior verification run was interrupted and owns the snapshot. Per AGENTS.md baseline integrity:

- The suite **refuses to start** while another live run owns the snapshot.
- `scripts/check_goldens_clean.py` reports a live run (not a failure) and flags a stale snapshot as pending.
- **Recovery (do this before any verification):** `SEED=42 python3 run_all_verification.py --restore-only`  (or `git checkout -- experiments/`).

Working tree currently shows no `experiments/*.json` modifications — only `__pycache__` — so goldens likely still match HEAD, but recover first to clear the ACTIVE marker.

## Initial Task

Research phase complete (E001–E043); surviving strategies documented in `ledger/RESEARCH_LEDGER.md`.

**Action required:** Wait for explicit user instructions before any research action. Do not re-run verification, modify experiments, or change baselines without explicit direction. If asked to verify, recover the snapshot first (see above).

## First Steps (verify state)

```bash
git status --short && git rev-parse HEAD origin/main
ls -la .verify_snapshot/ 2>&1 | head
SEED=42 python3 run_all_verification.py --restore-only   # only if a live/stale snapshot is pending
SEED=42 bash scripts/check.sh
```

## Verification Commands (if explicitly asked to reproduce)

```bash
SEED=42 python3 run_all_verification.py            # quick (~8 min, 8 drivers)
SEED=42 python3 run_all_verification.py --extended # (~21 min, +18 committed drivers)
SEED=42 python3 run_all_verification.py --full     # (~15 min, E042 n_sim=50 + 96-config grid)
SEED=42 python3 run_all_verification.py --restore-only  # recover goldens after an interrupted run
```

## Key Constraints (from AGENTS.md)

- `experiments/*.json` are committed goldens — verification backs them up and restores them; never commit verification output or leave a run half-finished.
- Golden baseline enforced by `scripts/check_golden_baseline.py` vs `ledger/golden_baseline.json`; data coverage by `scripts/check_data_coverage.py` vs `ledger/data_baseline.json`.
- Optimizer: validate on problem constraints, not solver exit status (see `tests/test_portfolio_opt.py`, ledger E049).
- Always use `SEED=42`. Close-to-close is the v1.2.3 primary convention.
- CI workflow cannot be created by automated agents (see AGENTS.md). Use local `make check/verify/*`.

## Handoff provenance

Fresh timestamped handoff created for next agentic session.
Durable copies written to: `handoff/`, `.kilo/handoff/`, and root symlink targets updated.

Handoff written by agent at 2026-11-04T02-07-36Z.
