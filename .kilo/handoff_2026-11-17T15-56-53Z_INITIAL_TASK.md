# Durable Handoff — Initial Task Message (next agentic work session)

**Created:** 2026-11-17T15:56:53Z
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Working directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## 1. Snapshot of state at handoff

- **HEAD:** `4ee50465` ("chore(kilo): checkpoint agent session") on `main`.
- **Sync:** `git rev-parse origin/main` == HEAD; `git rev-list --left-right --count origin/main...HEAD` → `0	0` (in sync).
- **Working tree:** only the 15 tracked `__pycache__/*.pyc` build artifacts under `scripts/`, `src/`, `tests/` are modified (gitignored bytecode; all guards ignore them). No source, driver, artifact, data, test, or ledger changes are uncommitted. No `.verify_snapshot/` or `.verify_reports/` present → no interrupted verification run to recover. `git status --short -- experiments/ data/ src/ scripts/ tests/ research_state/` is clean (excluding bytecode).
- **Research status:** repository is **closed**. Research phase E001–E051 complete; `experiments/*.json` are committed golden artifacts (107 pinned). Durable-handoff bookkeeping entries continue in the ledger (last: E462 at 2026-11-17T15:52:51Z; this refresh is the next entry, E463).
- **Prior handoff superseded:** `handoff_2026-11-17T15-55-27Z_INITIAL_TASK.md` (last fully mirrored + repointed handoff; HEAD `bd2d97b4`), read and retained for history.
- **Delta vs prior complete handoff (`handoff_2026-11-17T15-55-27Z_INITIAL_TASK.md`, HEAD `bd2d97b4` → live `4ee50465`):** checkpoint/handoff bookkeeping only — one `chore(kilo): checkpoint agent session` commit (`4ee50465`) recording this handoff refresh. No changes to `experiments/`, `data/`, `src/`, `scripts/`, `tests/`, or `research_state/` sources. Prior research state adopted unchanged.

## 2. Verification performed this session (2026-11-17T15:56Z)

- Working-tree / integrity inspection: HEAD `4ee50465`, in sync with `origin/main`; only `__pycache__/*.pyc` modified; `experiments/`, `data/`, `src/`, `scripts/`, `tests/`, `research_state/` clean; no `.verify_snapshot/` / `.verify_reports/` present (no interrupted run to recover).
- `scripts/check.sh` was **not** re-run this session to avoid unnecessary churn; the immediately preceding session (E462) recorded `SEED=42 bash scripts/check.sh` → `=== All checks passed ===` (exit 0) and `python3 scripts/check_golden_baseline.py` → `ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT` at HEAD `bd2d97b4`. The delta to `4ee50465` is checkpoint/bookkeeping only (no source/artifact change), so that result still holds. Run `SEED=42 bash scripts/check.sh` yourself to reconfirm.

## 3. Initial task for the next session

**No new research is requested. The research phase is closed.** If a new research direction is authorized, it must follow `ledger/PRIORITIZATION.md` (v1.2.7) and the AGENTS.md pre-registration rules. Otherwise the default task is:

1. Confirm state: `git status --short`, `git rev-parse HEAD`, `git rev-list --left-right --count origin/main...HEAD`. Expect only `__pycache__/*.pyc` modifications and a clean tree.
2. `SEED=42 bash scripts/check.sh` (or `make check`) — fast offline check, seconds. Fix any golden mismatch BEFORE committing.
3. If deeper verification is warranted: `SEED=42 python3 run_all_verification.py` (quick, ~8 min) or `--extended` / `--full`. Never leave a run half-finished; recover with `SEED=42 python3 run_all_verification.py --restore-only`.
4. Record any substantive outcome as the next ledger entry (E464+) with live HEAD, UTC timestamp, delta, and constraints honored.
5. Do **NOT** commit unless explicitly directed.

## 4. Standing constraints / gates (read before acting)

- **Canonical artifacts:** `experiments/*.json` are committed goldens. The verification suite overwrites then restores them. Never leave a run half-finished.
- **Recovery:** `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`. If HEAD already carries a captured run, restore the pinned artifact per `ledger/golden_baseline.json` (`git checkout <commit> -- experiments/<file>`; re-pin only deliberately via `python3 scripts/check_golden_baseline.py --update`, which shows the replacement in the diff).
- **Golden guards:** `scripts/check_goldens_clean.py` (working tree vs HEAD) and `scripts/check_golden_baseline.py` (SHA-256 vs pinned baseline) are first-class steps of `scripts/check.sh` and the suite. Never re-pin as a side effect of a verification run.
- **Data coverage:** every `data.download()` call site must resolve to a git-tracked, SHA-256-pinned cache file per `ledger/data_baseline.json` (`scripts/check_data_coverage.py`; update with `--update` only when intentionally adding a pinned input). The suite re-runs drivers with `QUANT_RESEARCH_OFFLINE=1`.
- **Seed / conventions:** always `SEED=42`. Close-to-close is the v1.2.3 primary convention; overnight decomposition reported alongside.
- **Known benign drift (do NOT re-pin to silence):** the tangency QP (`src/portfolio_opt.py` `max_sharpe` / `min_var`) remains ill-conditioned; a 1-ulp input perturbation moves the E041/E042 grid artifacts by ~1e-05, so `--extended` still reports E041 (and sometimes E042 grid) drifting by 29–133 numeric differences. This is a documented research-engineering decision (ledger E049 *Open item* + E050), not a defect to re-pin away. Optimizer determinism rule: judge a solver answer on the **problem's constraints**, never the solver's exit status (pinned by `tests/test_portfolio_opt.py`).
- **Durable handoff mechanism:** write `handoff_<UTC>_INITIAL_TASK.md` at the repo root, mirror it to `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/`, then run `python3 scripts/repoint_handoff.py handoff_<UTC>_INITIAL_TASK.md` to repoint the generic canonical symlinks (timestamped/historical aliases are intentionally left untouched).

## 5. Quick commands

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended / full verification
SEED=42 python3 run_all_verification.py --extended
SEED=42 python3 run_all_verification.py --full

# Recover golden artifacts after an interrupted verification run
SEED=42 python3 run_all_verification.py --restore-only
```
