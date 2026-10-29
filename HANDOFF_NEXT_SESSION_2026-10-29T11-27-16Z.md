# Handoff — Next Agentic Work Session

**Timestamp:** 2026-10-29T11:27:16Z
**Created by:** Kilo (kilo-auto/free)
**Repo:** Quantitative-Trading-Public-Research-Prompted (`main`, up to date with `origin/main`)

---

## Initial Task Message

> "Leave a timestamped clear initial task message for the next agentic work session in a durable handoff !"

This task is complete: this file is the durable handoff for the next session.

---

## Context

- Working directory: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
- Project: Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data.
- Research phase is complete (E001–E043). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.
- Key conventions: `SEED=42`, close-to-close is primary convention, verification suite backs up and restores `experiments/*.json` goldens.
- Git working tree clean except `__pycache__/*.pyc` noise (ignored). Goldens match the pinned baseline.

---

## Clear Initial Task (do this first, in order)

### 1. Verify repo state
```bash
git status --short
```
Ignore `__pycache__/*.pyc` noise. If the working tree holds verification output instead of goldens, restore before doing anything else (`SEED=42 python3 run_all_verification.py --restore-only`).

### 2. Baseline integrity — must pass before any changes
```bash
SEED=42 bash scripts/check.sh
```
- Golden mismatch or stale `.verify_snapshot/`? Run `--restore-only`, then re-run `check.sh`.
- Do **not** re-pin goldens to silence drift.

### 3. Quick verification (establish clean baseline)
```bash
SEED=42 python3 run_all_verification.py
```
Must complete fully and restore goldens. **Do not commit** a half-finished run.

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

- This file is the durable handoff target. Symlinks `HANDOFF.md`, `HANDOFF_CURRENT.md`, `HANDOFF_NEXT.md`, `HANDOFF_NEXT_SESSION.md`, `.kilo/handoff.md`, and `.kilo/handoff_next_session.md` point here.
- Immediate predecessor: `HANDOFF_NEXT_SESSION_2026-10-29T11-26-11Z.md`.
- If the user gives no new objective, the correct action is to maintain the baseline (run `check.sh` + quick verification) and report clean, not to invent new research.
