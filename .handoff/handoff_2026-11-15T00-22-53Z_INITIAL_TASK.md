# Durable Handoff — Next Agentic Work Session

**Timestamp (UTC): 2026-11-15T00:22:53Z**
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** `main` — `5d4b794b` ("chore(kilo): checkpoint agent session", committed 2026-11-14 23:38:15 +0000); `origin/main...HEAD` = `0 0` (in sync)
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Current State

- **Working tree:** no source/data changes. `git status --short | grep -v __pycache__` is clean; only `__pycache__/*.pyc` build artifacts differ (gitignored build output — do not commit).
- **Verification snapshot:** none active (`.verify_snapshot/` and `.verify_reports/` absent). No interrupted verification run.
- **Goldens:** `experiments/*.json` match HEAD (107 tracked `experiments/*.json`; 114 committed JSON artifacts total). Guard suite re-run this session (SEED=42):
  - `SEED=42 bash scripts/check.sh` → **exit 0**, "=== All checks passed ===" (py_compile, JSON artifacts parse, goldens clean vs HEAD, pinned golden baseline, data coverage, `test_portfolio_opt`, convention robustness, template validation, experiment imports).
  - All committed JSON artifacts parse; committed goldens match HEAD; pinned golden/data baselines match.
- **Environment:** Python 3.12.3 with `requirements.txt` dependencies installed. If reset, run `pip3 install --break-system-packages -r requirements.txt` before trusting `check.sh`.
- **Delta vs prior durable handoff** (E344, artifact `handoff_2026-11-14T23-38-06Z_INITIAL_TASK.md`, HEAD `7517bf8d`; HEAD advanced `7517bf8d` → `5d4b794b`): `git diff --name-only 7517bf8d..5d4b794b` → **1 path**, the prior E344 handoff artifact itself. Filtered for research content → **0 paths** under `experiments/`, `data/`, `src/`, `scripts/`, `tests/`, `research_state/`. No research substance changed.
- **Ledger gap (flagged, not fabricated):** the ledger ends at **E343**. The prior refresh self-labeled **E344** (artifact `handoff_2026-11-14T23-38-06Z_INITIAL_TASK.md`) but its ledger record was never persisted — `grep E344 ledger/RESEARCH_LEDGER.md` → 0 matches, and `git diff 7517bf8d..5d4b794b -- ledger/` is empty. This refresh is recorded as **E345**; the E344 gap is noted here rather than reconstructed.
- **Research phase:** complete (E001–E051). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`. Durable-handoff refreshes recorded through E343 (plus the unrecorded E344 artifact; this refresh = E345).

---

## INITIAL TASK (do first)

**Confirm baseline integrity, then await explicit user direction.**

1. **Confirm repo state**
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   Expect exit 0 ("=== All checks passed ==="). If it fails with `ModuleNotFoundError`, install deps (`pip3 install --break-system-packages -r requirements.txt`) and re-run — do not treat a dependency error as a baseline failure.

2. **If checks fail for a real reason**
   - Goldens differ from HEAD → `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`), or restore from the commit whose SHA-256 matches `ledger/golden_baseline.json`.
   - Active verification snapshot (`.verify_snapshot/ACTIVE.json`) → recover with `--restore-only` before proceeding.

3. **Then idle awaiting explicit user direction.**
   - Do **NOT** make source changes or commits unless explicitly asked.
   - Do **NOT** modify `experiments/*.json` goldens as a side effect of verification.
   - Do **NOT** re-pin baselines without explicit instruction and justification in the diff.
   - Do **NOT** commit `__pycache__/*.pyc` noise.

---

## Key Commands

```bash
# Baseline integrity (required first)
SEED=42 bash scripts/check.sh

# Verification
SEED=42 python3 run_all_verification.py              # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended   # (~21 min)
SEED=42 python3 run_all_verification.py --full       # (~15 min)

# Recovery / guards
SEED=42 python3 run_all_verification.py --restore-only
python3 scripts/check_golden_baseline.py
python3 scripts/check_data_coverage.py
python3 scripts/check_goldens_clean.py
```

---

## Known Open Items (read AGENTS.md / ledger before acting)

- **Optimizer determinism (E049):** `src/portfolio_opt.py` validates solver answers on constraints, never solver exit status. Tangency QP is ill-conditioned — 1-ulp input changes can move `min_var` by ~1e-05; E041/E042 grid artifacts may drift 29–133 numeric diffs. **Do not re-pin to silence.**
- **E041 drift:** 133 numeric differences (1-ulp QP sensitivity); 3 structural differences already fixed. Open in ledger; do not re-pin.
- **Ledger E344 gap:** see "Current State" above — the E344 handoff artifact exists but has no ledger record.
- **CI gate:** `.github/workflows/verification-gate.yml` must be created by a maintainer via GitHub UI; template at `.github/workflow-templates/verification-gate.yml`.
- **Always use `SEED=42`.** Never commit verification output or `__pycache__/*.pyc`.

---

## Durable artifact

Primary: repo root `handoff_2026-11-15T00-22-53Z_INITIAL_TASK.md`.
Mirrors: `handoff/`, `HANDOFFS/`, `.handoff/` (both `handoff_`-prefixed and bare-timestamp names), `.kilo/`, `.kilo/handoff/`.
Generic canonical pointers repointed via `python3 scripts/repoint_handoff.py handoff_2026-11-15T00-22-53Z_INITIAL_TASK.md`.

Supersedes `handoff_2026-11-14T23-38-06Z_INITIAL_TASK.md` (self-labeled E344, HEAD `7517bf8d`).