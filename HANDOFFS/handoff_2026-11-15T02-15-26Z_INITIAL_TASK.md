# Durable Handoff — Next Agentic Work Session

**Timestamp (UTC):** 2026-11-15T02:15:26Z
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** `main` — `d79f6a20` ("chore(kilo): checkpoint agent session", 2026-11-15 02:14:32Z); `origin/main...HEAD` = `0 0` (in sync)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

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

## Current State

- **Working tree:** no research/source/data changes. `git status --short | grep -v __pycache__` is clean; only tracked `__pycache__/*.pyc` build artifacts differ (gitignored output — do not commit).
- **Verification snapshot:** none active (`.verify_snapshot/` / `.verify_reports/` absent at handoff time). No interrupted verification run.
- **Goldens/data baselines:** canonical research artifacts remain committed under `experiments/` and pinned via `ledger/golden_baseline.json` / `ledger/data_baseline.json`.
- **Delta vs prior durable handoff** (`handoff_2026-11-15T02-09-57Z_INITIAL_TASK.md`, HEAD `20496ac5`): checkpoint commit(s) advanced HEAD `20496ac5` → `d79f6a20`; filtered for research content → **0 paths** under `experiments/`, `data/`, `src/`, `scripts/`, `tests/`, `research_state/`. Only handoff/ledger pointer housekeeping changed. No research substance changed.
- **Research phase:** complete (E001–E051). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`. Durable-handoff refresh recorded here (supersedes E066 artifact `handoff_2026-11-15T02-09-57Z_INITIAL_TASK.md`).

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

- **Optimizer determinism (E049/E050):** `src/portfolio_opt.py` validates solver answers on problem constraints, not solver exit status (SLSQP status 8 can be build-dependent at a feasible optimum; rule pinned by `tests/test_portfolio_opt.py`). Tangency QP remains ill-conditioned (1-ulp sensitivity can move E041/E042 `min_var` results ~1e-5; E041 still shows 133 numeric diffs). **Do not re-pin E041/E042 artifacts to silence drift.**
- **CI gate:** `.github/workflows/verification-gate.yml` must be created by a maintainer via GitHub UI; template at `.github/workflow-templates/verification-gate.yml`.
- **Always use `SEED=42`.** Never commit verification output or `__pycache__/*.pyc`.

---

## Durable artifact & mirrors

Primary: `handoff_2026-11-15T02-15-26Z_INITIAL_TASK.md` (repo root).
Mirrors created in `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/` and generic canonical pointers repointed via `python3 scripts/repoint_handoff.py handoff_2026-11-15T02-15-26Z_INITIAL_TASK.md`.

Supersedes: `handoff_2026-11-15T02-09-57Z_INITIAL_TASK.md`.
