# Durable Handoff — Next Agentic Work Session

**Created:** 2026-11-28T02:55:54Z
**Session:** previous agentic session complete, no uncommitted source changes
  (only `src/__pycache__/cache_keys.cpython-312.pyc` modified — ignore / delete)
**Last commit:** `1bd679b7 chore(kilo): checkpoint agent session`

## Repo state

Working tree is clean apart from a stray `.pyc`. No experiment artifacts under
`experiments/` have been overwritten by a verification run.

## Recommended initial task for next session

Run the fast convention-robustness check end-to-end and confirm it passes
cleanly (offline, seconds):

```bash
SEED=42 bash scripts/check.sh
# or
make check
```

If it passes, proceed to quick verification:

```bash
SEED=42 python3 run_all_verification.py
# or
make verify-quick
```

## Key conventions to respect

- `experiments/*.json` are canonical research artifacts — never commit
  verification output; restore goldens with `--restore-only` if a run is
  interrupted.
- Re-pinning a golden requires `python3 scripts/check_golden_baseline.py
  --update` and must be recorded in `ledger/RESEARCH_LEDGER.md`.
- Data inputs: `scripts/check_data_coverage.py` requires every
  `data.download()` cache file to be git-tracked and SHA-256 pinned in
  `ledger/data_baseline.json`; runs execute with `QUANT_RESEARCH_OFFLINE=1`.
- Always run with `SEED=42`.
- Research phase complete (E001–E043); surviving strategies documented in
  `ledger/RESEARCH_LEDGER.md`.

## Notes / open questions

None recorded. No blockers.
