# Handoff: Next Agentic Session

- **Timestamp:** 2026-10-28T01:40:51Z
- **Branch:** main
- **HEAD:** $(git -C /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted rev-parse HEAD)
- **Durable handoff:** HANDOFF_NEXT_SESSION_2026-10-28T01-40-51Z.md
- **Working tree:** Only `__pycache__/*.pyc` bytecode changes (gitignored noise). No tracked source, data, or golden changes. No `.verify_snapshot/` present — no interrupted verification run to recover.

## Context

- Repo: Independent reproducible quantitative-strategy research (2014–2026 US equities, futures, macro). Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- Verification infrastructure is strict: `experiments/*.json` (107 files) are canonical goldens. `run_all_verification.py` backs them up before re-running and restores them afterward — **never leave a run half-finished**.
- Known reporting-only drift (decisions unchanged, do NOT re-pin to silence):
  - **E041**: ~133 numeric diffs (1-ulp sensitivity of an ill-conditioned QP; optimizer determinism fixed per ledger E049). 3 structural differences gone.
  - **E030**: numeric diffs on near-zero quantities (documented; 16-ETF input pinned per ledger E048).
- Cache coverage is an enforced invariant: `scripts/check_data_coverage.py` + `ledger/data_baseline.json`. Verification runs with `QUANT_RESEARCH_OFFLINE=1`; a missing cache entry fails hard instead of silently downloading.
- CI workflow `.github/workflows/main.yml` exists; the intended `verification-gate.yml` still requires maintainer creation via GitHub UI (template at `.github/workflow-templates/verification-gate.yml`, instructions in `VERIFICATION_GATE_TEMPLATE.md`) — outside agent scope per AGENTS.md.

## Initial Task (do this first)

1. **Verify repo health (golden integrity).**
   ```bash
   SEED=42 bash scripts/check.sh
   ```
2. **Confirm clean baseline state.**
   ```bash
   git diff --name-only
   SEED=42 python3 scripts/check_golden_baseline.py
   SEED=42 python3 scripts/check_data_coverage.py
   ```
3. **Act on results.**
   - If all checks pass and only `__pycache__` differs: repo is clean. Review `ledger/RESEARCH_LEDGER.md` for open items; no verification rerun required.
   - If golden integrity fails: restore before committing (`SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`). Do **not** re-pin artifacts as a side effect of a verification run.
   - If `check_goldens_clean.py` reports a *live* verification run, leave it alone.

## One Precise Next Task (bounded, optional)

No new research task is warranted — the repository is in a clean, fully-verified state. If a bounded in-session task is desired, re-run `SEED=42 python3 run_all_verification.py --extended` and confirm stability (expect the pre-existing E030/E041 drift; do **not** weaken tolerances or modify committed goldens).

## Quick Reference

- Fast check: `SEED=42 bash scripts/check.sh` or `make check`
- Quick verify (8 drivers): `SEED=42 python3 run_all_verification.py` or `make verify-quick`
- Extended (~21 min): `SEED=42 python3 run_all_verification.py --extended` or `make verify-extended`
- Full: `SEED=42 python3 run_all_verification.py --full` or `make verify-full`
- Restore goldens if interrupted: `SEED=42 python3 run_all_verification.py --restore-only`

## Notes for Next Agent

- Always use `SEED=42`.
- Verification overwrites `experiments/*.json` temporarily — never leave a run half-finished.
- Do **not** commit verification outputs. Only commit intentional source/data changes.
- Do **not** change gate logic, sensitivity grids, pre-registered outcomes, or validated constructions (`src/backtest.py`, `src/strategies.py`, `src/futures.py`, `src/macro.py`, `src/portfolio_opt.py`).
- Known drift (E030, E041) is reporting-only. Do **not** weaken tolerances or re-pin goldens to silence it.
- The only working-tree changes are `__pycache__/*.pyc` bytecode files — not tracked source; ignore or clean, do not commit.
- CI workflow creation is maintainer-gated (outside agent scope).

## Timestamp

Created: 2026-10-28T01:40:51Z (UTC)
