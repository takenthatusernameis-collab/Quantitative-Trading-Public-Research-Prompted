# Initial Task for Next Agentic Work Session
Timestamp (UTC): 2026-11-05T12:51:52Z
HEAD: 8585fe5 (2026-11-05 12:50:37 +0000, `chore(kilo): checkpoint agent session`)
Working tree: clean (no uncommitted changes at handoff creation)

## Baseline Status (observed this session)
- `SEED=42 bash scripts/check.sh` → **exit 1** (environment-limited).
  - **Integrity checks PASSED**: 114 committed JSON artifacts parse OK; all committed golden artifacts match HEAD; 107/107 pinned golden artifacts match `ledger/golden_baseline.json`; 35 pinned data inputs present/tracked/unchanged; `test_portfolio_opt`, `test_json_artifacts`, `test_goldens_clean` suites all OK.
  - **Environment failure (not a repo regression)**: `tests/test_data_coverage.py` reported 3 errors because `pandas` is not installed in this runner environment (`ModuleNotFoundError: No module named 'pandas'`). These tests exercise `src.data` import paths that require the full scientific stack.
  - The `FAIL ...` lines emitted mid-run are **expected negative-case output from the test harness itself** (schema/manifest/golden-recovery scenarios exercised under temp fixtures), not failures of the committed repository state.
- No `.verify_snapshot/` / no interrupted verification run detected.
- Prior stale-task correction remains in effect (E086): cost sensitivity on `large_liquid` is **already complete as E005** (`cost_sweep.py` → `experiments/cost_sensitivity.json`, pinned). Do not re-execute it.

## Immediate Priorities (next session)
1. **Re-establish a green baseline in a fully provisioned environment**
   ```bash
   pip install -r requirements.txt
   SEED=42 bash scripts/check.sh          # expect exit 0
   ```
   If a golden mismatch or stale snapshot is reported, recover first:
   `SEED=42 python3 run_all_verification.py --restore-only`
   (use `git checkout -- experiments/` only if HEAD is verified against `ledger/golden_baseline.json`). **Never commit verification output.**

2. **Confirm open research work**
   - Review `ledger/RESEARCH_LEDGER.md` tail/open items for any genuinely open, pre-registrable task.
   - Research phase is complete (E001–E043). If no open pre-registered item exists, **close the session with a status report** — do not invent new work or move goalposts.

3. **If an open pre-registrable item is identified**
   - Propose before implementation: objective, gates, falsification expectations, sensitivity grid (reported, not gated), data/vintage requirements, and multiple-testing discipline.
   - Any config clearing gates in a sensitivity grid requires a dedicated pre-registered confirmatory run + full placebo before promotion.

## Verification Reference
```bash
make check                  # fast convention + golden checks (~seconds)
make verify                 # convention robustness only
make verify-quick           # SEED=42 python3 run_all_verification.py (~8 min)
make verify-extended        # --extended (~21 min; structural match)
make verify-full            # --full (~15 min; E042 n_sim=50 + 96-config grid)
SEED=42 python3 run_all_verification.py --restore-only
```

## Non-Negotiable Constraints
- **Reproducibility**: `SEED=42` for all stochastic/verification runs.
- **Goldens are canonical**: `experiments/*.json` must not be modified by verification. Never re-pin baselines as a side effect of a run. `git checkout -- experiments/` restores HEAD (which can be wrong if a checkpoint captured verification output) — prefer `--restore-only` or restore SHAs pinned in `ledger/golden_baseline.json`.
- **Data**: Pinned vintages (`data/vintages.json`, `data/fundamentals_vintages.json`); cache coverage enforced by `scripts/check_data_coverage.py`; verification uses `QUANT_RESEARCH_OFFLINE=1`.
- **Pre-registration & discipline**: No post-hoc goalpost moves; sensitivity grids reported, not gated; negative results recorded honestly (REJECTED/PARTIAL) with evidence.
- **Project config**: Put new commands/agents in `.kilo/` (not `.kilocode/` or `.opencode/`).
- **Commits**: Do not commit interrupted verification artifacts or unpinned golden changes. Do not commit/push unless explicitly requested.

## Suggested Next Action
In an environment with `requirements.txt` installed, run `SEED=42 bash scripts/check.sh`. If green and `ledger/RESEARCH_LEDGER.md` shows no open items, report repository closed/verified. Otherwise, draft a pre-registration for the next ledger-approved item before coding.
