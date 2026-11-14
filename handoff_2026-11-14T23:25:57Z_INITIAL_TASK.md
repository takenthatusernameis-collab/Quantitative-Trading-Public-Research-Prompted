# Durable Handoff — Next Agentic Work Session

**Timestamp (UTC): 2026-11-14T23:25:57Z**
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** `main` — `3b1b549d` ("chore(kilo): checkpoint agent session"); `origin/main...HEAD` = `0 0` (in sync)
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Current State

- **Working tree:** no source/data changes. `git status --short | grep -v __pycache__` is clean; only `__pycache__/*.pyc` build artifacts differ (gitignored build output — do not commit).
- **Verification snapshot:** active run detected (`.verify_snapshot/ACTIVE.json` owned by pid 128924). `experiments/e001.json` modified by this run. `experiments/e042_quick.json` untracked artifact present.
- **Goldens:** `experiments/*.json` mostly match HEAD except `e001.json` (modified by active verification run). Guard suite re-run this session (SEED=42):
  - `SEED=42 bash scripts/check.sh` → **exit 0**, "=== All checks passed ===" (py_compile, JSON artifacts parse, goldens clean vs HEAD, pinned golden baseline, data coverage, `test_portfolio_opt`, convention robustness, template validation, experiment imports).
  - Some test fixture JSONs in `experiments/` fail schema validation by design (they are negative test cases).
  - `data/panel.parquet` fingerprint mismatch vs pinned baseline; file not git-tracked (gitignored). A fresh clone would re-download.
- **Environment:** Python 3.12.3 with `requirements.txt` dependencies installed. If reset, run `pip3 install --break-system-packages -r requirements.txt` before trusting `check.sh`.
- **Delta vs prior durable handoff** (2026-11-14T22:30:02Z, HEAD `9a90bd36`): one checkpoint commit (`9a90bd36..3b1b549d`) + this handoff refresh. Filtered for research content → **0 paths** under `experiments/`, `data/`, `src/`, `scripts/`, `tests/`, `research_state/`. No research substance changed.
- **Research phase:** complete (E001–E051). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`. Durable-handoff refreshes recorded.

---

## INITIAL TASK (do first)

**Confirm baseline integrity, recover active verification run, then await explicit user direction.**

1. **Recover the active verification run first**
   ```bash
   SEED=42 python3 run_all_verification.py --restore-only
   ```
   This restores `experiments/*.json` goldens from the snapshot and cleans up `.verify_snapshot/`.

2. **Confirm repo state after recovery**
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   Expect exit 0. If it fails with `ModuleNotFoundError`, install deps (`pip3 install --break-system-packages -r requirements.txt`) and re-run — do not treat a dependency error as a baseline failure.

3. **If checks fail for a real reason**
   - Goldens differ from HEAD → `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`), or restore from the commit whose SHA-256 matches `ledger/golden_baseline.json`.
   - Active verification snapshot (`.verify_snapshot/ACTIVE.json`) → recover with `--restore-only` before proceeding.

4. **Then idle awaiting explicit user direction.**
   - Do **NOT** make source changes or commits unless explicitly asked.
   - Do **NOT** modify `experiments/*.json` goldens as a side effect of verification.
   - Do **NOT** re-pin baselines without explicit instruction and justification in the diff.
   - Do **NOT** commit `__pycache__/*.pyc` noise.

---

## Key Commands

```bash
# Baseline integrity (required first)
SEED=42 bash scripts/check.sh

# Recovery
SEED=42 python3 run_all_verification.py --restore-only

# Verification
SEED=42 python3 run_all_verification.py              # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended   # (~21 min)
SEED=42 python3 run_all_verification.py --full       # (~15 min)

# Guards
python3 scripts/check_golden_baseline.py
python3 scripts/check_data_coverage.py
python3 scripts/check_goldens_clean.py
```

---

## Known Open Items (read AGENTS.md / ledger before acting)

- **Active verification run:** Must be recovered with `--restore-only` before any new work.
- **Optimizer determinism (E049):** `src/portfolio_opt.py` validates solver answers on constraints, never solver exit status. Tangency QP is ill-conditioned — 1-ulp input changes can move `min_var` by ~1e-05; E041/E042 grid artifacts may drift 29–133 numeric diffs. **Do not re-pin to silence.**
- **E041 drift:** 133 numeric differences (1-ulp QP sensitivity); 3 structural differences already fixed. Open in ledger; do not re-pin.
- **Data coverage:** `data/panel.parquet` fingerprint mismatch and not git-tracked. If needed, commit and re-pin with `python3 scripts/check_data_coverage.py --update`.
- **CI gate:** `.github/workflows/verification-gate.yml` must be created by a maintainer via GitHub UI; template at `.github/workflow-templates/verification-gate.yml`.
- **Always use `SEED=42`.** Never commit verification output or `__pycache__/*.pyc`.

---

## Durable artifact

Primary: repo root `handoff_2026-11-14T23:25:57Z_INITIAL_TASK.md`.
Mirrors: `handoff/`, `HANDOFFS/`, `.handoff/` (both `handoff_`-prefixed and bare-timestamp names), `.kilo/`, `.kilo/handoff/`.
Generic canonical pointers repointed via `python3 scripts/repoint_handoff.py handoff_2026-11-14T23:25:57Z_INITIAL_TASK.md`.

Supersedes `handoff_2026-11-14T22:30:02Z_INITIAL_TASK.md` (ledger E342, HEAD `9a90bd36`).