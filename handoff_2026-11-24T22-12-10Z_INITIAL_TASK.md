# Durable Handoff — Kilo Agent Session

**Created:** 2026-11-24T23:01:40Z
**Session:** New session — 2026-11-24T23:01:37.955Z
**Working tree:** clean (`git status --short` empty)
**Recent commits:** `701e5154 chore(kilo): checkpoint agent session` (and prior checkpoints)

## Repository context

Quantitative trading research repo (2014–2026 US equities / futures / macro). Research phase complete (E001–E043); surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

Key conventions (from `AGENTS.md`):
- `experiments/*.json` are canonical research artifacts — never modify directly; verification suite backs them up and restores them.
- `SEED=42` required for all runs.
- `run_all_verification.py` supports `--skip-slow`, `--restore-only`, `--extended`, `--full`.
- `scripts/check.sh` = convention-robustness check + template validation (offline, seconds).
- `scripts/check_golden_baseline.py` — compares experiments/ against `ledger/golden_baseline.json` SHA-256 fingerprints.
- `scripts/check_data_coverage.py` — requires every `data.download()` cache file tracked and pinned in `ledger/data_baseline.json`; runs offline via `QUANT_RESEARCH_OFFLINE=1`.
- `python3 -m py_compile` on changed files (no separate linter).
- CI verification-gate workflow cannot be created by automated agents (template at `.github/workflow-templates/verification-gate.yml`; maintainer must create via GitHub UI).

## Clear initial task for next session

Run the fast convention check to confirm the tree is in a clean, reproducible state:

```bash
SEED=42 bash scripts/check.sh
# or: make check
```

If `check.sh` passes, report the result. If it reports a golden/data mismatch or any failure, do **not** commit verification output — restore via `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`) and surface the failure.

**Definition of done:** `scripts/check.sh` exits 0 with no golden/data mismatches, and no stray driver output remains under `experiments/`.

## Notes

- Board (`board_read`/`board_post`) is shared with peer participants; this session row is `self: true`. No peer messages pending.
- No in-progress task beyond this handoff itself was specified in the current request.
