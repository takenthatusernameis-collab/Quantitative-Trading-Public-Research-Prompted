# HANDOFF — Next Agentic Work Session

**Created:** 2026-10-29T17:00:57Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Branch:** main, HEAD `2bc8552` (chore(kilo): checkpoint agent session), working tree clean except tracked `__pycache__/*.pyc` noise (15 files, 0 insertions)
**Research phase:** COMPLETE (E001–E049). Surviving validated strategies in `ledger/RESEARCH_LEDGER.md`.

Working tree verified clean at handoff time: no `.verify_snapshot/` stale marker, no verification output leaked into `experiments/`, no uncommitted source/data changes. This session performed **no code changes** — baseline was inspected and found intact.

---

## CLEAR INITIAL TASK MESSAGE (Do This First, In Order)

### 1) Verify repository state
```bash
git status --short
git log --oneline -3
```
Ignore `__pycache__/*.pyc` noise. If the working tree holds verification output instead of goldens, restore before anything else (step 2).

### 2) Baseline integrity — MUST pass before any changes
```bash
SEED=42 bash scripts/check.sh
```
- Golden mismatch or stale `.verify_snapshot/`? Run `SEED=42 python3 run_all_verification.py --restore-only`, then re-run `scripts/check.sh`.
- Do NOT re-pin goldens to silence drift. Only use `python3 scripts/check_golden_baseline.py --update` with explicit, documented justification.

### 3) Establish a clean baseline (quick verification)
```bash
SEED=42 python3 run_all_verification.py
```
Must complete fully and restore goldens. If interrupted, run `SEED=42 python3 run_all_verification.py --restore-only` — do not commit a half-finished run.

### 4) Orient to current state
- Read `AGENTS.md` (Baseline Integrity, Reproducibility sections).
- Read `ledger/RESEARCH_LEDGER.md` — focus on E049 (optimizer determinism / ill-conditioned tangency QP numeric drift) and E040 (close-out).
- **No mandated next research task.** Research phase is complete. Proceed only if the user provides a concrete objective. If no objective is given, maintain the baseline (steps 1–3) and report a clean status — do not invent new research.

---

## Known Pre-Existing Drift (Reporting-Only — Decisions Unchanged)
- **E041 (market-neutral portfolio, REJECTED):** ~133 numeric diffs due to 1-ulp sensitivity of an ill-conditioned tangency QP. Optimizer determinism fixed per E049; structural differences gone. Do not re-pin.
- **E030:** Numeric diffs on near-zero quantities (documented). Do not re-pin.
- **E042 (min-variance, PARTIAL 4/5):** G2 placebo-significance gate fails (placebo z 1.60 < 3.0); not promoted. Recorded as PARTIAL.

## Gotchas / Constraints
- Always use `SEED=42`.
- Never leave a verification run half-finished (`.verify_snapshot/` guarded by `ACTIVE.json` owning the PID).
- Do not commit verification outputs — only intentional source/data changes.
- CI workflow cannot be created by agents; template at `.github/workflow-templates/verification-gate.yml` (maintainer creates via GitHub UI).
- `check_golden_baseline.py` enforces SHA-256 pins in `ledger/golden_baseline.json`.
- `check_data_coverage.py` enforces cache coverage; verification runs with `QUANT_RESEARCH_OFFLINE=1`.

## Key References
- `AGENTS.md` — commands, conventions, baseline integrity rules
- `ledger/RESEARCH_LEDGER.md` — experiment history and disposition
- `ledger/golden_baseline.json` — pinned golden fingerprints
- `ledger/data_baseline.json` — pinned data cache fingerprints
- `scripts/check.sh`, `run_all_verification.py`

## Handoff Notes
- This file is the durable handoff target. Symlinks `HANDOFF.md`, `HANDOFF_CURRENT.md`, `HANDOFF_NEXT.md`, `HANDOFF_NEXT_SESSION.md`, and any `.kilo/handoff*` should point here.
- Immediate predecessor: `HANDOFF_NEXT_SESSION_2026-10-29T16-59-17Z.md`.
- If the user gives no new objective, the correct action is to maintain the baseline (run `check.sh` + quick verification) and report clean, not to invent new research.

(End of file)
