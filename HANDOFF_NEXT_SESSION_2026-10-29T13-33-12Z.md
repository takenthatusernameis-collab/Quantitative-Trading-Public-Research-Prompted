# HANDOFF — Next Agentic Work Session

**Created:** 2026-10-29T13:33:12Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Branch:** `main` (HEAD `34cb818 chore(kilo): checkpoint agent session`)
**Research phase:** COMPLETE (E001–E049). Surviving validated strategies in `ledger/RESEARCH_LEDGER.md`.

---

## Clear Initial Task (do this first, in order)

### 1. Verify repo state
```bash
git status --short
```
Ignore `__pycache__/*.pyc` noise (currently modified). Working tree should otherwise be clean. If it holds verification output instead of committed goldens, restore first:
```bash
SEED=42 python3 run_all_verification.py --restore-only
# or
git checkout -- experiments/
```

### 2. Baseline integrity — must pass before any changes
```bash
SEED=42 bash scripts/check.sh
```
Verify: golden cleanliness, golden baseline SHA-256, data coverage, artifact JSON schema, unit tests, convention robustness, all experiment script imports.
- Golden mismatch or stale `.verify_snapshot/`? Restore with `--restore-only`, then re-run `check.sh`.
- Do **not** re-pin goldens to silence drift. Use `scripts/check_golden_baseline.py --update` only with explicit justification and a ledger entry.
- `check_data_coverage.py` enforces cache coverage; verification runs with `QUANT_RESEARCH_OFFLINE=1`.

### 3. Quick verification (establish clean baseline)
```bash
SEED=42 python3 run_all_verification.py
```
Expected: most steps pass; `run_e042_lead.py` may fail with G2 placebo z < 3.0 (Decision: REJECTED 4/5) — this is the pre-registered confirmatory outcome for E042, not a defect. Goldens must be restored at end.
- If interrupted, run `--restore-only`; **do not commit** a half-finished run.

### 4. Orient to open work
- Read `AGENTS.md` (Baseline Integrity, Reproducibility).
- Read `ledger/RESEARCH_LEDGER.md` — focus on E049 (optimizer determinism / ill-conditioned tangency QP numeric drift) and E040 (close-out).
- **No mandated next research task.** Research phase is complete. Proceed only when the user provides a concrete objective.
- Numeric drift in E041/E042 is expected (ill-conditioned QP, 1-ulp sensitivity). Do **not** re-pin to silence it.

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
- If no new objective given, maintain baseline (`check.sh` + quick verification) and report clean, do not invent research.

---

## Handoff Notes
- Durable handoff target updated. Symlinks `HANDOFF.md`, `HANDOFF_CURRENT.md`, `HANDOFF_NEXT.md`, `HANDOFF_NEXT_SESSION.md` updated to point here.
- Predecessor: `HANDOFF_NEXT_SESSION_2026-10-29T13-32-43Z.md`
" filePath">
/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted/HANDOFF_NEXT_SESSION_2026-10-29T13-33-12Z.md