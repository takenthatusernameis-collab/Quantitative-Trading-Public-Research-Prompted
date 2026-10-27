# HANDOFF_NEXT_SESSION_2026-10-27T23-47-15Z

## Initial Task (clear)
**Do not re-run the full verification suite to "refresh" goldens.** Treat `experiments/*.json` as the committed authoritative baseline and keep the ledger's disposition intact. Your first job is to establish a clean, known-good baseline state and then execute the *next* concrete action (below). If anything looks like it would overwrite goldens, stop and restore first.

## Context (current state)
- **Phase**: Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- **Goldens**: `experiments/*.json` are canonical. Verification overwrites them during runs and must restore them. A backup lives in `.verify_snapshot/` with `ACTIVE.json`.
- **Verification guards**: `scripts/check_goldens_clean.py` (working tree vs HEAD) and `scripts/check_golden_baseline.py` (vs `ledger/golden_baseline.json`) are enforced in `scripts/check.sh`. Never re-pin goldens as a side effect of verification.
- **Known drift/caveats** (important): E029 offline-reproducible (fundamentals pinned in `data/fundamentals/`), E030 offline-reproducible (16-ETF panel committed). E041 has optimizer-ill-conditioning drift (133 numeric diffs) — do **not** re-pin. E042 lead/tangency can be environment-sensitive due to QP conditioning.
- **Cache coverage enforced**: `scripts/check_data_coverage.py` requires every `data.download()` cache file to exist, be git-tracked, and match `ledger/data_baseline.json`. Missing/pinned inputs only via `--update` with intent.
- **Optimizers**: SLSQP status 8 ("Positive directional derivative for linesearch") is feasible/optimal at constrained optimum in some builds; validation is on constraints, not exit status (pinned by `tests/test_portfolio_opt.py`).

## Suggested next actions (concrete)
1. **Verify baseline integrity first** (read-only/guarded):
   ```bash
   SEED=42 python3 scripts/check_goldens_clean.py
   SEED=42 python3 scripts/check_golden_baseline.py
   SEED=42 python3 scripts/check_data_coverage.py
   ```
   If `check_goldens_clean.py` reports a *live* verification, leave it alone. If it reports a stale snapshot or golden mismatch vs HEAD, **restore before proceeding**: `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/` only if HEAD is known-good).

2. **Run fast convention check**:
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   (runs py_compile, guards, convention-robustness checks, etc.)

3. **Pick one focused task** (do not blanket re-verify). Good candidates depending on goal:
   - If extending analysis: work from existing `experiments/*.json` and `ledger/RESEARCH_LEDGER.md` (no regeneration).
   - If modifying code that affects portfolio optimization: run `python3 -m pytest tests/test_portfolio_opt.py -v` and be mindful of ill-conditioning (do not chase 1e-5 numeric drift).
   - If touching data/loading: run `scripts/check_data_coverage.py` after changes and only update pins with explicit rationale.
   - If reproducing a specific experiment: use its driver (e.g. `experiments/run_e042.py`) with care, knowing verification will restore goldens.

## Key files to read
- `AGENTS.md` — commands, guards, drift notes, cache rules
- `ledger/RESEARCH_LEDGER.md` — decisions (REJECTED/PARTIAL/VALIDATED), gates
- `ledger/golden_baseline.json`, `ledger/data_baseline.json`
- `scripts/check.sh`, `run_all_verification.py`, `verify_convention_robustness.py`
- `.verify_snapshot/README` (if exists) for recovery details

## Guardrails
- **Never** commit verification output or overwrite canonical goldens as side effect.
- **Never** re-pin goldens to silence known numeric drift (E041/E042 conditioning).
- **Never** add unpinned data downloads; commit cache files and update `ledger/data_baseline.json` via `--update` with justification.
- **Always** use `SEED=42`.
- **Offline safety**: verification uses `QUANT_RESEARCH_OFFLINE=1` for drivers; respect that.

## Timestamp
Created: 2026-10-27T23:47:15Z (UTC)
