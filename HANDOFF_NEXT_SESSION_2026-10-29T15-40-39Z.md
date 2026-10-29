# HANDOFF — Next Agentic Work Session

**Created:** 2026-10-29T15:40:39Z
**Repo:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Branch:** main, HEAD `15852fc` (chore(kilo): checkpoint agent session), up to date with origin/main
**Research phase:** COMPLETE (E001–E049). Surviving validated strategies in `ledger/RESEARCH_LEDGER.md`.

Working tree verified clean at handoff time (only `__pycache__/*.pyc` noise; no `.verify_snapshot/` stale marker; no verification output leaked into `experiments/`). Baseline integrity (`SEED=42 bash scripts/check.sh`) should be re-confirmed before any changes.

---


## CLEAR INITIAL TASK MESSAGE (Do This First, In Order)

### 1) Verify repository state
```bash
git status --short
```
Ignore `__pycache__/*.pyc` noise. If the working tree holds verification output instead of goldens, restore before doing anything else (see step 2).


### 2) Baseline integrity — MUST pass before any changes
```bash
SEED=42 bash scripts/check.sh
```
- **Golden mismatch or stale `.verify_snapshot/`?** Run `SEED=42 python3 run_all_verification.py --restore-only`, then re-run `scripts/check.sh`.
- **Do NOT re-pin goldens to silence drift.** Only use `python3 scripts/check_golden_baseline.py --update` with explicit, documented justification.
- `scripts/check_golden_baseline.py` enforces SHA-256 pins in `ledger/golden_baseline.json`.
- `scripts/check_data_coverage.py` enforces cache coverage; verification runs with `QUANT_RESEARCH_OFFLINE=1`.


### 3) Establish a clean baseline (quick verification)
```bash
SEED=42 python3 run_all_verification.py
```
Must complete fully and restore goldens. If interrupted at any point, run `SEED=42 python3 run_all_verification.py --restore-only` — **do not commit** a half-finished run.


### 4) Orient to current state
- Read `AGENTS.md` (Baseline Integrity, Reproducibility sections).
- Read `ledger/RESEARCH_LEDGER.md` — focus on **E049** (optimizer determinism / ill-conditioned tangency QP numeric drift) and **E040** (close-out).
- **No mandated next research task.** Research phase is complete. Proceed only if the user provides a concrete objective. If no objective is given, maintain the baseline (steps 1-3) and report a clean status.


---


## Known Pre-Existing Drift (Reporting-Only — Decisions Unchanged)
- **E041 (market-neutral portfolio, REJECTED):** ~133 numeric diffs due to 1-ulp sensitivity of an ill-conditioned tangency QP. Optimizer determinism was fixed per **E049**; the 3 structural differences are gone. **Do not re-pin.**
- **E030:** Numeric diffs on near-zero quantities (documented). **Do not re-pin.**
- **E029/E030 inputs:** Pinned for offline reproducibility; their goldens were deliberately re-pinned at the time. Do not "fix" by re-running and re-pinning.


---


## Key Files To Read First
- `AGENTS.md`
- `ledger/RESEARCH_LEDGER.md`
- `run_all_verification.py`
- `scripts/check.sh`
- `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`
- `src/portfolio_opt.py` (optimizer determinism context, E049)


---


## Gotchas / Constraints
- **Always use `SEED=42`.**
- **Never leave a verification run half-finished.** `.verify_snapshot/` is guarded by `ACTIVE.json` owning the PID.
- `scripts/check_golden_baseline.py` enforces SHA-256 pins in `ledger/golden_baseline.json`.
- `scripts/check_data_coverage.py` enforces cache coverage; verification runs with `QUANT_RESEARCH_OFFLINE=1`.
- Optimizer ill-conditioning causes bounded numeric drift (E041/E042) — **do not re-pin** to silence it.
- CI workflow cannot be created by agents (template in `.github/workflow-templates/verification-gate.yml`); a maintainer must create it via the GitHub UI.
- Do **not** commit verification outputs — only intentional source/data changes.
- Convention: close-to-close is v1.2.3 primary; overnight decomposition reported alongside.


---


## Handoff Notes
- This file is the durable handoff target. Symlinks `HANDOFF.md`, `HANDOFF_CURRENT.md`, `HANDOFF_NEXT.md`, and `HANDOFF_NEXT_SESSION.md` now point to this file.
- If the user gives no new objective, the correct action is to maintain the baseline (run `check.sh` + quick verification) and report clean — **do not invent new research**.
