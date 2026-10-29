# HANDOFF — Next Agentic Work Session

**Created:** 2026-10-29T12-24-18Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Branch:** `main`
**Research phase:** COMPLETE (E001–E049). Surviving validated strategies in `ledger/RESEARCH_LEDGER.md`.

---

## Clear Initial Task (do this first, in order)

### 1. Verify repo state
```bash
git status --short
```
Ignore `__pycache__/*.pyc` noise. If the working tree holds verification output instead of committed goldens, restore before doing anything else (see step 2):
```bash
SEED=42 python3 run_all_verification.py --restore-only
# or
git checkout -- experiments/
```

### 2. Baseline integrity — must pass before any changes
```bash
SEED=42 bash scripts/check.sh
```
- Golden mismatch or stale `.verify_snapshot/`? Restore with `--restore-only`, then re-run `check.sh`.
- Do **not** re-pin goldens to silence drift. Use `scripts/check_golden_baseline.py --update` only with explicit justification and a ledger entry.
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
- CI workflow cannot be created by agents (template in `.github/workflow-templates/verification-gate.yml`); a maintainer must create it via the GitHub UI.
- If the user gives no new objective, the correct action is to maintain the baseline (run `check.sh` + quick verification) and report clean, not to invent new research.

---

## Handoff Notes
- This file is the durable handoff target. Symlinks `HANDOFF.md`, `HANDOFF_CURRENT.md`, `HANDOFF_NEXT.md`, `HANDOFF_NEXT_SESSION.md` point here.
- Immediate predecessor: `HANDOFF_NEXT_SESSION_2026-10-29T11-38-30Z.md`; plus the `HANDOFF_SESSION_*` and earlier `HANDOFF_NEXT_SESSION_*` series.
