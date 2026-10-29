# HANDOFF — Next Agentic Work Session

**Created:** 2026-10-29T14-35-35Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Branch:** main (up to date with origin/main, HEAD fb99de3)
**Research phase:** COMPLETE (E001–E049). Surviving validated strategies in `ledger/RESEARCH_LEDGER.md`.

Working tree verified clean at handoff time (only `__pycache__/*.pyc` noise, no `.verify_snapshot/` stale marker, no verification output leaked into `experiments/`).

---

## Clear Initial Task (do this first, in order)

### 1. Verify repo state
```bash
git status --short
```
Ignore `__pycache__/*.pyc` noise. If the working tree holds verification output instead of goldens, restore before doing anything else (see step 2).

### 2. Baseline integrity — must pass before any changes
```bash
SEED=42 bash scripts/check.sh
```
- Golden mismatch or stale `.verify_snapshot/`? Run `SEED=42 python3 run_all_verification.py --restore-only`, then re-run `check.sh`.
- Do **not** re-pin goldens to silence drift. Use `scripts/check_golden_baseline.py --update` only with explicit justification.
- `check_golden_baseline.py` enforces SHA-256 pins in `ledger/golden_baseline.json`.
- `check_data_coverage.py` enforces cache coverage; verification runs with `QUANT_RESEARCH_OFFLINE=1`.

### 3. Quick verification (establish clean baseline)
```bash
SEED=42 python3 run_all_verification.py
```
Must complete fully and restore goldens. If interrupted, run `--restore-only`; **do not commit** a half-finished run.

### 4. Orient to open work
- Read `AGENTS.md` (Baseline Integrity, Reproducibility sections).
- Read `ledger/RESEARCH_LEDGER.md` — focus on E049 (optimizer determinism / ill-conditioned tangency QP numeric drift) and E040 (close-out).
- **No mandated next research task.** Research phase is complete. Proceed only when the user provides a concrete objective.
- Numeric drift in E041/E042 is expected (ill-conditioned QP, 1-ulp sensitivity). Do **not** re-pin to silence it — see the open item in the ledger.

---

## Key Files to Read First
- `AGENTS.md`
- `ledger/RESEARCH_LEDGER.md`
- `run_all_verification.py`
- `scripts/check.sh`
- `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`

---

## Gotchas / Constraints
- Always use `SEED=42`.
- Never leave a verification run half-finished (`.verify_snapshot/` guarded by `ACTIVE.json` owning pid).
- `check_golden_baseline.py` enforces SHA-256 pins in `ledger/golden_baseline.json`.
- `check_data_coverage.py` enforces cache coverage; verification runs with `QUANT_RESEARCH_OFFLINE=1`.
- Optimizer ill-conditioning causes bounded numeric drift (E041/E042) — do not re-pin.
- CI workflow cannot be created by agents (template in `.github/workflow-templates/verification-gate.yml`); a maintainer must create it via the GitHub UI.

---

## Handoff Notes
- This file is the durable handoff target. Symlinks `HANDOFF.md`, `HANDOFF_CURRENT.md`, `HANDOFF_NEXT.md`, `HANDOFF_NEXT_SESSION.md`, and any `.kilo/handoff*` should point here.
- Preceding session handoffs (chronological): `HANDOFF_NEXT_SESSION_2026-10-29T14-32-30Z.md`, `HANDOFF_NEXT_SESSION_2026-10-29T14-31-27Z.md`, `HANDOFF_NEXT_SESSION_2026-10-29T14-29-58Z.md`, plus the `HANDOFF_SESSION_*` and earlier `HANDOFF_NEXT_SESSION_*` series.
- If the user gives no new objective, the correct action is to maintain the baseline (run `check.sh` + quick verification) and report clean, not to invent new research.
