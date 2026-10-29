# Handoff: Next Agentic Session
- **Timestamp:** 20261029T061652Z
- **Branch:** main
- **HEAD:** 379eba9
- **Durable handoff:** HANDOFF_NEXT_SESSION_20261029T061652Z.md
- **Working tree:** Tracked changes present (15 file(s))

## Context
- Repo: Independent reproducible quantitative-strategy research (2014–2026 US equities/futures/macro). Research phase complete (E001–E043). Surviving strategies documented in `ledger/RESEARCH_LEDGER.md`.
- Verification strict: `experiments/*.json` are canonical goldens. Never re-pin as side effect of verification. E030 and E041 exhibit pre-existing numeric drift (reporting-only) — do not re-pin or weaken tolerances.
- Guards enforced: `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py` (pins `ledger/golden_baseline.json`), `scripts/check_data_coverage.py` (pins `ledger/data_baseline.json`). Cache coverage and golden integrity are required.
- Optimizer determinism: `src/portfolio_opt.py` validates on problem constraints (not solver exit status). Ill-conditioned tangency QP remains; see ledger E049.

## Initial Task (do this first)
1. **Verify repo health (golden integrity).**
   ```bash
   SEED=42 bash scripts/check.sh
   ```
2. **Confirm baseline state.**
   ```bash
   git diff --name-only
   python3 scripts/check_golden_baseline.py
   python3 scripts/check_data_coverage.py
   ```
3. **Decide next action.**
   - If checks pass and working tree clean of tracked changes: no verification rerun needed. Review `ledger/RESEARCH_LEDGER.md` for open items.
   - If checks fail on goldens: restore before committing (`SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`). Do not re-pin artifacts as a side effect. If a commit already replaced baselines, restore from the commit pinned in `ledger/golden_baseline.json` instead.
   - If data coverage fails: commit missing inputs and re-pin with `python3 scripts/check_data_coverage.py --update` only with review.

## One Precise Next Task (bounded, optional)
Review `ledger/RESEARCH_LEDGER.md` for any open items. Only act on explicitly open, bounded items. Do not re-run full verification unless there is a concrete reason (e.g. to investigate a regression). If you do rerun, never leave it half-finished and never commit verification outputs.

## Quick Reference
- Fast check: `SEED=42 bash scripts/check.sh` or `make check`
- Quick verify: `SEED=42 python3 run_all_verification.py` or `make verify-quick`
- Extended: `SEED=42 python3 run_all_verification.py --extended` or `make verify-extended` (expect pre-existing E030/E041 drift)
- Full: `SEED=42 python3 run_all_verification.py --full` or `make verify-full`
- Restore goldens: `SEED=42 python3 run_all_verification.py --restore-only`

## Notes for Next Agent
- Always use `SEED=42`.
- Verification overwrites `experiments/*.json` temporarily — never leave a run half-finished.
- Do not commit verification outputs. Only commit intentional source/data changes.
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or validated constructions.
- Golden/data pins require explicit `--update` and review; never silent re-pins.
