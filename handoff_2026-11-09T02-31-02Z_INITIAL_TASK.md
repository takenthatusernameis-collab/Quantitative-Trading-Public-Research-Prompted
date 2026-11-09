# Durable Handoff — Next Agentic Work Session

**Created:** 2026-11-09T02:40:44Z
**Working tree:** clean (no uncommitted changes)
**Last commits:** `chore(kilo): checkpoint agent session` (×5, latest `31217c01`)

## Repo state

- Research phase complete: experiments E001–E043 finished; surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- Canonical research artifacts live in `experiments/*.json` (committed goldens).
- AGENTS.md defines the verification workflow and golden-baseline guards.

## Next task (initial)

Run the fast convention-robustness check + template validation to confirm the tree is green before any new work:

```bash
SEED=42 bash scripts/check.sh
# or equivalently
make check
```

If `check.sh` passes, the next session is clear to proceed with new experiment work. If it reports a golden mismatch, fix it before committing (see AGENTS.md "Baseline Integrity" — never let a verification run capture output into `experiments/`).

## Key guards to remember

- `experiments/*.json` are committed goldens; `run_all_verification.py` backs them up and restores them — never commit verification output.
- Replacing a golden requires re-pinning via `python3 scripts/check_golden_baseline.py --update`.
- Data inputs must be pinned in `ledger/data_baseline.json` (`scripts/check_data_coverage.py`); runs execute with `QUANT_RESEARCH_OFFLINE=1`.
- Always use `SEED=42`.
