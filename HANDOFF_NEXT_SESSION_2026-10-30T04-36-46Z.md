# HANDOFF — Next Agentic Work Session

**Timestamp:** 2026-10-30T04:36:46Z (UTC)
**Branch:** main
**Last commit:** 2b6ae54 chore(kilo): checkpoint agent session
**Working tree:** clean of tracked changes (only `__pycache__/*.pyc`, gitignored — 13 modified pyc files, no source/data changes)
**Snapshot:** `.verify_snapshot/` empty — no live verification run, nothing to recover
**Research phase:** complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

---

## INITIAL TASK (do first)

### 1. Verify baseline integrity before making any changes
```bash
SEED=42 bash scripts/check.sh
```
This runs: `py_compile` on core scripts/drivers, `scripts/check_goldens_clean.py` (working tree vs HEAD), `scripts/check_golden_baseline.py` (artifacts vs pinned SHA-256 in `ledger/golden_baseline.json`), `scripts/check_data_coverage.py` (all data inputs cached + pinned), and `tests/test_portfolio_opt.py`.
**Confirm ALL CHECKS PASSED (exit 0).**

### 2. If checks fail due to a stale/in-progress verification
- If `scripts/check_goldens_clean.py` reports a stale snapshot or goldens differ from HEAD (and no live run owns it): recover with `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/` as a last resort). Never leave a verification run half-finished.
- If a tracked artifact under `experiments/` was replaced in HEAD vs the pinned baseline, **do not re-pin by re-running verification**. Restore the correct artifact from the commit that matches `ledger/golden_baseline.json` (e.g. `git checkout <commit> -- experiments/<file>`) and fix the cause. Re-pinning requires `python3 scripts/check_golden_baseline.py --update` and should be intentional.

### 3. Open item (only if explicitly asked)
Address ledger **E049** — ill-conditioned tangency QP causes 1-ulp drift in E041/E042 grid artifacts. Do **not** re-pin artifacts to silence drift; replace the SLSQP solve with a well-conditioned deterministic solver if directed, then re-run extended verification to confirm drift resolved.

---

## Current state

- **Research phase complete:** E001–E043. Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.
- **Canonical artifacts:** `experiments/*.json` are goldens. `run_all_verification.py` backs up/restores them; verification must never overwrite the committed baseline.
- **Data:** Cached parquet in `data/` (gitignored except pinned vintages). `data/vintages.json` pins 2026-10-12; 2026-10-11 is committed for specific experiments. Fundamentals pinned in `data/fundamentals/` per `data/fundamentals_vintages.json` (enables offline E029). Cache coverage is enforced by `scripts/check_data_coverage.py`; verification runs offline (`QUANT_RESEARCH_OFFLINE=1`).
- **Optimizer determinism (E049):** `src/portfolio_opt.py` validates on problem constraints (not solver exit status). SLSQP status 8 is build-dependent but feasible optimums are accepted; pinned by `tests/test_portfolio_opt.py`. The tangency QP itself remains ill-conditioned: a 1-ulp input perturbation still moves the `min_var` answers by ~1e-05, so E041/E042 grid artifacts still drift by 29-133 differences. Do **not** re-pin them to silence that.
- **Known pre-existing drift (reporting-only, decisions unchanged):**
  - **E041**: ~133 numeric diffs (1-ulp sensitivity of ill-conditioned QP). 3 structural differences gone. Do **not** re-pin.
  - **E030**: numeric diffs on near-zero quantities (documented). Do **not** re-pin.
  - **E029/E030 inputs**: pinned for offline reproducibility; goldens deliberately re-pinned. Do not "fix" by re-running.

---

## Immediate priorities for next session

- [ ] Run `SEED=42 bash scripts/check.sh` and confirm all gates pass.
- [ ] If clean, review `ledger/RESEARCH_LEDGER.md` for any open items/gates before starting new work.
- [ ] If user request comes in, follow AGENTS.md strictly: use `SEED=42`, respect pre-registration/multiple-testing discipline, never commit unless explicitly asked, and never modify goldens via verification.

---

## Quick reference commands

```bash
# Fast checks
SEED=42 bash scripts/check.sh
SEED=42 make check

# Verification
SEED=42 python3 run_all_verification.py --skip-slow  # convention + quick gates
SEED=42 python3 run_all_verification.py --quick       # 8 drivers + batch/validate + E042 n_sim=2
SEED=42 python3 run_all_verification.py --extended    # +18 drivers (reports drift in .verify_reports/)
SEED=42 python3 run_all_verification.py --full        # +E042 n_sim=50 + 96-config grid

# Recovery
SEED=42 python3 run_all_verification.py --restore-only

# Guards
SEED=42 python3 scripts/check_goldens_clean.py
SEED=42 python3 scripts/check_golden_baseline.py
SEED=42 python3 scripts/check_data_coverage.py
```

## Files to read first
- `AGENTS.md` (full project commands/conventions)
- `ledger/RESEARCH_LEDGER.md`
- `ledger/golden_baseline.json`
- `ledger/data_baseline.json`
- `scripts/check.sh`
- `run_all_verification.py`

## Notes
- Always use `SEED=42`.
- Do not commit verification output. If interrupted, restore goldens before committing.
- Sensitivity grids are reported, not gated. Confirmatory runs require pre-registration + full placebo.
- CI workflow cannot be created by automated agents (see AGENTS.md). Template at `.github/workflow-templates/verification-gate.yml`, instructions in `VERIFICATION_GATE_TEMPLATE.md`.