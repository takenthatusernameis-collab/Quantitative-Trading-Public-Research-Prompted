# Agentic Work Session Handoff

**Timestamp**: 2026-11-17T04:14:29Z
**Project**: Quantitative-Trading-Public-Research-Prompted
**Workspace**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Status
- Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- All experiments pre-registered with falsification expectations and promotion gates.

## Verification Commands (from AGENTS.md)
```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh      # or: make check

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py            # or: make verify-quick

# Extended verification (~21 min; 18 more committed drivers, structural match)
SEED=42 python3 run_all_verification.py --extended # or: make verify-extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full     # or: make verify-full

# Convention robustness only (reads JSONs, no writes)
SEED=42 python3 verify_convention_robustness.py     # or: make verify

# Skip slow batch/regression steps (convention only)
SEED=42 python3 run_all_verification.py --skip-slow

# Recover golden artifacts after an interrupted verification run
SEED=42 python3 run_all_verification.py --restore-only
```

## Key Notes for Next Session
- Golden files in `experiments/*.json` are canonical research artifacts.
- Verification suite backs them up before re-running and restores afterward.
- **Never leave a verification run half-finished** — use `--restore-only` to recover if interrupted.
- Seed is always `SEED=42` for reproducibility.
- Data cached in `data/` (gitignored except pinned vintages). Cache coverage is an enforced invariant.
- Baseline integrity: `scripts/check_goldens_clean.py` + `scripts/check_golden_baseline.py` fail on any tracked artifact drift. Re-pin only with `python3 scripts/check_golden_baseline.py --update`, never as a side effect of verification.

## Open Items (from ledger)
- E041 drift: 133 numeric differences remain (1-ulp sensitivity of ill-conditioned QP) — do not re-pin.
- E030: Reproduces with 0 differences since 2026-10-20 (16-ETF panel committed).
- E029: Fully offline-reproducible since 2026-10-20 (fundamentals pinned in `data/fundamentals/`).
- E042 tangency QP remains ill-conditioned; do not re-pin to silence drift.

## Clear Initial Task for Next Session
**Refresh the durable handoff for the next agentic work session.**
1. Capture the live git state (`date -u`, `git rev-parse HEAD`, `git status --short --branch`, origin sync).
2. Delta the working tree against the prior durable handoff; note any changes to `experiments/`, `data/`, `src/`, `scripts/`, `tests/`, or `research_state/`.
3. Write a fresh timestamped `handoff_<ISO>_INITIAL_TASK.md` at the repo root (mirror to `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/`).
4. Run `python3 scripts/repoint_handoff.py handoff_<ISO>_INITIAL_TASK.md` to repoint generic canonical pointers.
5. Do not commit unless explicitly directed. Honor SEED=42; do not change gates, pre-registration, falsification, sensitivity, or validated constructions; do not re-pin goldens; do not commit verification output or `__pycache__`.

## Next Steps
- Read `ledger/RESEARCH_LEDGER.md` for current experiment dispositions and the most recent durable-handoff entry.
- If a new research task is assigned, follow the pre-registration + falsification + promotion-gate discipline documented in AGENTS.md.