# HANDOFF — Next Agentic Work Session

**Created:** 2026-10-29T13:14:08Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Branch:** `main` (HEAD `eb7f1bd2f52e65d3ff20c03414d35a26d2e1a09f`, 2026-10-29 13:03:12 +0000)
**Research phase:** COMPLETE (E001–E049). Surviving validated strategies in `ledger/RESEARCH_LEDGER.md`.

---

## Clear Initial Task (do this first, in order)

### 1. Verify repo state
```bash
git status --short
```
Ignore `__pycache__/*.pyc` noise. Working tree is clean (no verification output).
If it ever holds verification output instead of committed goldens, restore first:
```bash
SEED=42 python3 run_all_verification.py --restore-only
# or
git checkout -- experiments/
```

### 2. Baseline integrity — must pass before any changes
```bash
SEED=42 bash scripts/check.sh
```
**Verified 2026-10-29T13:03Z: ALL CHECKS PASSED** (golden cleanliness, golden baseline SHA-256, data coverage, artifact JSON schema, unit tests, convention robustness, all experiment script imports).
- Golden mismatch or stale `.verify_snapshot/`? Restore with `--restore-only`, then re-run `check.sh`.
- Do **not** re-pin goldens to silence drift. Use `scripts/check_golden_baseline.py --update` only with explicit justification and a ledger entry.
- `check_data_coverage.py` enforces cache coverage; verification runs with `QUANT_RESEARCH_OFFLINE=1`.

### 3. Quick verification (establish clean baseline)
```bash
SEED=42 python3 run_all_verification.py
```
**Verified 2026-10-29T13:03Z: 11 of 12 steps PASS; `run_e042_lead.py` FAILS (known open finding).** Goldens restored at end.
- `run_e042_lead.py` exit 1: G2 placebo z = 1.32 (gate ≥ 3.0) → **Decision: REJECTED (4/5 gates)**, consistent with E042 closure. FE2 (OOS var-reduction vs 1/N) also fails. This is the pre-registered confirmatory run for the E042 min-var market-neutral grid; it is *supposed* to fail — do not treat as a repo defect.
- If interrupted, run `--restore-only`; **do not commit** a half-finished run.

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
- Immediate predecessor: `HANDOFF_NEXT_SESSION_2026-10-29T13-03-20Z.md` (HEAD `eb7f1bd`).
- Prior session handoffs: `HANDOFF_NEXT_SESSION_2026-10-29T12-30-00Z.md`, `HANDOFF_NEXT_SESSION_2026-10-29T12-26-43Z.md`, `HANDOFF_NEXT_SESSION_2026-10-29T12-24-18Z.md`.
