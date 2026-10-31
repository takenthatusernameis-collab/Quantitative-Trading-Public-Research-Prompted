# Agentic Work Session Handoff

**Timestamp (UTC):** 2026-10-31T01:04:45Z
**Handoff from:** Current agent session
**Repository:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current Project State

- **Research phase:** Complete (E001–E043). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.
- **Canonical artifacts:** `experiments/*.json` are committed goldens. The verification suite backs these up before re-running and restores them afterward — they must never be left modified.
- **Data coverage:** Enforced by `scripts/check_data_coverage.py` against `ledger/data_baseline.json`. Pinned caches exist in `data/` (gitignored except vintages in `data/vintages.json` and fundamentals in `data/fundamentals_vintages.json`).
- **Known open items:** E041 numeric drift due to an ill-conditioned QP / solver sensitivity (documented in the ledger). Optimizer determinism rules are enforced by `tests/test_portfolio_opt.py`. Do **not** re-pin artifacts to silence this drift.
- **Environment:** Python 3 research repo; dependencies in `requirements.txt` (optional `cvxpy`/`cvxopt`, falls back to `scipy.optimize`).

## Initial Task For Next Session

Start here in order:

1. **Verify clean baseline state**
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   This runs py_compile, data coverage, golden-clean checks, golden-baseline fingerprint check, convention-robustness, and portfolio-opt tests. If it reports a golden mismatch or stale snapshot, restore before proceeding:
   ```bash
   SEED=42 python3 run_all_verification.py --restore-only
   ```
   or `git checkout -- experiments/` (use the pinned commit if HEAD already captured a run).

2. **Review research state and priorities**
   - Read `ledger/RESEARCH_LEDGER.md` for open items, gates, and promotion candidates.
   - Check `git status` and recent commits to understand what’s uncommitted.
   - Review `AGENTS.md` for verification commands and constraints.

3. **Run appropriate verification based on findings**
   - **Quick sanity:** `SEED=42 make verify-quick` (~8 min) — re-runs the 8-driver quick block and validates.
   - **Extended (if checking driver drift):** `SEED=42 make verify-extended` (~21 min).
   - **Full (if needed):** `SEED=42 make verify-full` (~15 min) — includes E042 n_sim=50 and the 96-config sensitivity grid.

## Important Constraints

- **Always use `SEED=42`** for reproducibility.
- **Never commit verification outputs.** If interrupted, restore goldens before committing.
- **Follow pre-registration discipline.** Goalposts are not moved post-hoc; multiple-testing is reported, not gated.
- **No CI workflow changes.** The GitHub Actions workflow cannot be created by automated agents (controller restores it; repo token lacks permissions). Use local `make` targets instead.

**Next agent: Start with step 1 above.**
