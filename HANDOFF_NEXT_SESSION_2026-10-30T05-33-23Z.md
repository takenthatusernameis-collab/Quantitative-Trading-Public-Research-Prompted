# HANDOFF — Next Agentic Work Session

**Timestamp:** 2026-10-30T05:33:23Z (UTC)
**Branch:** main
**Last commit:** `fb00cb6` — chore(kilo): checkpoint agent session
**Working tree:** clean (tracked changes limited to `__pycache__/*.pyc`, pre-existing/gitignored). `experiments/` goldens match HEAD and the pinned baseline.
**Snapshot:** `.verify_snapshot/` absent — no live verification run, nothing to recover.
**Baseline integrity verified at write time:** `SEED=42 bash scripts/check.sh` → exit 0, ALL CHECKS PASSED (last confirmed 2026-10-30T05:27:05Z).

---

## INITIAL TASK (do first)

1. **Verify baseline integrity before any changes**
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   Confirms: py_compile on core scripts/drivers, `check_goldens_clean.py` (working tree vs HEAD), `check_golden_baseline.py` (artifacts vs pinned SHA-256 in `ledger/golden_baseline.json`), `check_data_coverage.py` (all data inputs cached + pinned), and `tests/test_portfolio_opt.py`. Expect exit 0.

2. **If checks fail**
   - Stale snapshot / goldens differ from HEAD with no live run owning it → recover: `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/` as last resort). Never leave a verification run half-finished.
   - If a tracked artifact under `experiments/` was replaced in HEAD vs the pinned baseline, **do not re-pin by re-running verification**. Restore the correct artifact from the commit whose SHA-256 matches `ledger/golden_baseline.json` (`git checkout <commit> -- experiments/<file>`) and fix the cause. Re-pinning requires `python3 scripts/check_golden_baseline.py --update` and must appear in the diff.

3. **Do not make changes or commit without explicit user direction.** Goldens (`experiments/*.json`) are authoritative; never modify them as a side effect of verification. Do not re-run experiments to "refresh" goldens. Do not re-pin to silence drift.

---

## Current state

- **Research phase complete:** E001–E043. Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- **Canonical artifacts:** `experiments/*.json` are goldens. `run_all_verification.py` backs up/restores them; verification must never overwrite the committed baseline.
- **Data:** Cached parquet in `data/` (gitignored except pinned vintages). `data/vintages.json` pins 2026-10-12; 2026-10-11 committed for specific experiments. Fundamentals pinned in `data/fundamentals/` per `data/fundamentals_vintages.json` (enables offline E029). Cache coverage enforced by `scripts/check_data_coverage.py`. Verification runs offline (`QUANT_RESEARCH_OFFLINE=1`).
- **Optimizer determinism (E049):** `src/portfolio_opt.py` validates on problem constraints, not solver exit status. SLSQP status 8 is build-dependent but feasible optima are accepted; pinned by `tests/test_portfolio_opt.py`. Ill-conditioned tangency QP still causes numeric drift in E041/E042 grids.
- **Known open item:** E041 numeric drift remains (133 diffs) exceeding 1e-4 tolerance in extended verification; do **not** re-pin to silence it. E029 and E030 are offline-reproducible with 0 differences.

## Immediate priorities for next session

- [x] `SEED=42 bash scripts/check.sh` passes — verified at write time.
- [ ] If user request comes in, follow AGENTS.md strictly: use `SEED=42`, respect pre-registration/multiple-testing discipline, never commit unless explicitly asked, never modify goldens via verification.
- [ ] Open item (only if explicitly asked): address ledger E049 — ill-conditioned tangency QP causes 1-ulp drift in E041/E042. Replace with a well-conditioned deterministic solver if directed, then re-run extended verification.

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
- CI workflow cannot be created by automated agents (see AGENTS.md). Template at `.github/workflow-templates/verification-gate.yml`.