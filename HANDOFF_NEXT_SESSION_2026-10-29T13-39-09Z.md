# HANDOFF — Next Agentic Work Session

**Created:** 2026-10-29T13:39:09Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Branch:** `main` (HEAD `6223dd9aca7e23edf646069c49c2a5d141106ff7` @ 2026-10-29 13:39:01 +0000, "chore(kilo): checkpoint agent session")
**Research phase:** COMPLETE (E001–E049). Surviving validated strategies in `ledger/RESEARCH_LEDGER.md`.

## Current working-tree state (verified at handoff time)
- `git status --short` shows **only** `__pycache__/*.pyc` modifications (build noise, gitignored-ish but tracked from a prior run). No source, experiment, or ledger changes.
- `.verify_snapshot/` does **not** exist — no live or stale verification snapshot. Baseline is at rest.
- All canonical artifacts under `experiments/` match HEAD. Nothing to restore.

## Clear Initial Task (do this first, in order)

### 1. Baseline integrity — must pass before any changes
```bash
SEED=42 bash scripts/check.sh
```
Checks: golden cleanliness, golden baseline SHA-256 (`ledger/golden_baseline.json`), data coverage (`ledger/data_baseline.json`), artifact JSON schema, unit tests, convention robustness, all experiment script imports.
- On golden mismatch: restore with `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`), then re-run `check.sh`.
- Do **not** re-pin goldens to silence drift. Use `scripts/check_golden_baseline.py --update` only with explicit justification and a ledger entry.

### 2. Quick verification (establish clean baseline, ~8 min)
```bash
SEED=42 python3 run_all_verification.py
```
Expected: most steps pass. `run_e042_lead.py` may fail with G2 placebo z < 3.0 (Decision: REJECTED 4/5) — this is the pre-registered confirmatory outcome for E042, not a defect. Goldens must be restored at end (`--restore-only`).
- Never leave a verification run half-finished (`.verify_snapshot/` guarded by `ACTIVE.json` owning pid). A killed run is recoverable via `--restore-only`.

### 3. Orient to open work
- Read `AGENTS.md` (Baseline Integrity, Reproducibility sections).
- Read `ledger/RESEARCH_LEDGER.md` — focus on E049 (optimizer determinism / ill-conditioned tangency QP numeric drift) and E040 (close-out).
- **No mandated next research task.** Research phase is complete. Proceed only when the user provides a concrete objective.
- Numeric drift in E041/E042 is expected (ill-conditioned QP, 1-ulp sensitivity). Do **not** re-pin to silence it.

## Key Files to Read First
- `AGENTS.md`
- `ledger/RESEARCH_LEDGER.md`
- `run_all_verification.py`
- `scripts/check.sh`
- `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`

## Gotchas / Constraints
- Always use `SEED=42`.
- Never leave a verification run half-finished (`.verify_snapshot/` guarded by `ACTIVE.json` owning pid).
- `check_golden_baseline.py` enforces SHA-256 pins in `ledger/golden_baseline.json`.
- `check_data_coverage.py` enforces cache coverage; verification runs with `QUANT_RESEARCH_OFFLINE=1`.
- Optimizer ill-conditioning causes bounded numeric drift (E041/E042) — do not re-pin.
- CI workflow cannot be created by agents (template in `.github/workflow-templates/verification-gate.yml`); a maintainer must create it via the GitHub UI.
- If no new objective given, maintain baseline (`check.sh` + quick verification) and report clean, do not invent research.

## Handoff Notes
- Durable handoff target updated. Symlinks `HANDOFF.md`, `HANDOFF_CURRENT.md`, `HANDOFF_NEXT.md`, `HANDOFF_NEXT_SESSION.md` (root) and `.kilo/HANDOFF.md`, `.kilo/HANDOFF_NEXT_SESSION.md`, `.kilo/handoff.md`, `.kilo/handoff_next.md`, `.kilo/handoff_next_session.md` point here.
- Predecessor: `HANDOFF_NEXT_SESSION_2026-10-29T13-38-32Z.md`