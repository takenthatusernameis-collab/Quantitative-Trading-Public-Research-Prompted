# Handoff — Next Agentic Work Session

**Timestamp:** $(date -u +%Y-%m-%dT%H:%M:%SZ)
**Created by:** Kilo (kilo-auto/free)
**Repo:** Quantitative-Trading-Public-Research-Prompted (main)

---

## Initial Task Message

> "Leave a timestamped clear initial task message for the next agentic work session in a durable handoff !"

This task is complete: this file is the durable handoff for the next session.

---

## Context

- Working directory: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
- Research phase complete (E001–E043). Surviving validated strategies in `ledger/RESEARCH_LEDGER.md`.
- Conventions: `SEED=42`, close-to-close primary, verification backs up/restores `experiments/*.json` goldens.
- Git tree clean except `__pycache__/*.pyc` (ignored). Goldens match pinned baseline.

---

## Clear Initial Task (do this first, in order)

### 1) Verify repo state
```bash
git status --short
```
Ignore `__pycache__/*.pyc`. If working tree has verification output (not goldens), restore first: `SEED=42 python3 run_all_verification.py --restore-only`.

### 2) Baseline integrity
```bash
SEED=42 bash scripts/check.sh
```
If golden mismatch or stale `.verify_snapshot/` with no live run: restore then re-run. Do **not** re-pin goldens to silence drift.

### 3) Quick verification (clean baseline)
```bash
SEED=42 python3 run_all_verification.py
```
Must complete fully and restore goldens. **Do not commit** a half-finished run.

### 4) Orient to open work
- Read `AGENTS.md` (Baseline Integrity, Reproducibility).
- Read `ledger/RESEARCH_LEDGER.md` — focus on E049 (optimizer determinism / ill-conditioned tangency QP numeric drift) and E040.
- **No mandated next research task.** Research phase complete. Proceed only if user gives concrete objective.
- Numeric drift in E041/E042 is expected (ill-conditioned QP, 1-ulp). Do **not** re-pin — see ledger.

---

## Key Files

- `AGENTS.md`
- `ledger/RESEARCH_LEDGER.md`
- `run_all_verification.py`
- `scripts/check.sh`
- `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`

---

## Gotchas / Constraints

- Always use `SEED=42`.
- Never leave verification run half-finished (`.verify_snapshot/` guarded by `ACTIVE.json`).
- `check_golden_baseline.py` enforces SHA-256 pins in `ledger/golden_baseline.json`.
- `check_data_coverage.py` enforces cache coverage; verification runs with `QUANT_RESEARCH_OFFLINE=1`.
- Optimizer ill-conditioning causes bounded numeric drift (E041/E042) — do not re-pin.
- CI workflow cannot be created by agents (template in `.github/workflow-templates/verification-gate.yml`); maintainer must create via GitHub UI.

---

## Handoff Notes

- This file is the durable handoff target. Update symlinks to point here: `HANDOFF.md`, `HANDOFF_CURRENT.md`, `HANDOFF_NEXT.md`, `HANDOFF_NEXT_SESSION.md`, `.kilo/handoff.md`, `.kilo/handoff_next_session.md`.
- Previous: `HANDOFF_NEXT_SESSION_2026-10-29T11-27-16Z.md`
- If no new objective, maintain baseline (`check.sh` + quick verification) and report clean, do not invent new research.
