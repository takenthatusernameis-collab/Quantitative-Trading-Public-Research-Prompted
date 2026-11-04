# Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-04T11:52:53Z
**Branch:** main
**HEAD:** 7c4de3b (chore(kilo): checkpoint agent session)
**Working tree:** Only `__pycache__/*.pyc` modified (gitignored in effect; safe).

## Project state
- Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- Canonical experiment artifacts live in `experiments/*.json`. Verification suite backs up/restores them; never commit verification output.
- Baseline integrity guards are enforced: `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py` (pinned in `ledger/golden_baseline.json`), `scripts/check_data_coverage.py` (pinned in `ledger/data_baseline.json`). See AGENTS.md "Baseline Integrity".
- Offline reproducibility: data caches in `data/` (some vintages committed), E029 fundamentals pinned in `data/fundamentals/` with `data/fundamentals_vintages.json`, `QUANT_RESEARCH_OFFLINE=1` used by verification.
- Optimizer determinism (E049): `src/portfolio_opt.py` validates on constraints (not solver exit status); tangency QP ill-conditioned causes small numeric drift in E041/E042 grids (accepted in extended reporting only).

## Quick verification (safe, read-only style for checks)
```bash
SEED=42 bash scripts/check.sh                # fast checks + guards
SEED=42 python3 verify_convention_robustness.py  # convention robustness (no writes)
SEED=42 python3 run_all_verification.py --skip-slow  # skip slow batch/regression
```
Full suite: `SEED=42 python3 run_all_verification.py` (~15 min). Extended: `--extended` (~21 min). If interrupted, recover: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`.

## Suggested initial task for next session
**Task:** Audit and harden baseline integrity (golden/data coverage) against accidental re-pin
- **Goal:** Ensure no verification run can silently replace canonical goldens; verify guards are active and document the recovery procedure.
- **Steps:**
  1. Run `SEED=42 bash scripts/check.sh` and confirm all guards pass (goldens clean vs HEAD, golden baseline matches pinned hashes, data coverage OK, JSON artifacts OK).
  2. Review `scripts/check_golden_baseline.py` and `scripts/check_goldens_clean.py` behavior (active snapshot detection). Confirm `.verify_snapshot/ACTIVE.json` handling is correct.
  3. Inspect recent history around golden re-pins (commits noted in AGENTS.md) and ensure `ledger/golden_baseline.json`/`ledger/data_baseline.json` are only updated intentionally via `--update` flags.
  4. Add/verify a short note in `AGENTS.md` or `docs/` if needed, but do not change canonical artifacts.
- **Acceptance:** `scripts/check.sh` passes cleanly; no tracked `experiments/*.json` changed by the session; handoff notes updated if any guard adjustments made.

## Notes / gotchas
- Do not run full verification to "refresh" goldens. If goldens appear changed, restore first.
- E041/E042 numeric drift is expected due to ill-conditioned QP; do not re-pin to silence.
- CI workflow cannot be created by agents (controller restores `.github/workflows/`).
