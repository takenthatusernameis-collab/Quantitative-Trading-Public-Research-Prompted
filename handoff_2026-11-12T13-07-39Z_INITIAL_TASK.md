# Agentic Handoff — Initial Task

**Created:** 2026-11-12T13:07:39Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**HEAD:** `53191374a65959733b4afc7ac39a135d7e9f4fb8` (2026-11-12 13:01:45 +0000, `chore(kilo): checkpoint agent session`, `main` = `origin/main`)

## Current state

- Research phase complete (E001–E043). Surviving validated strategies: `ledger/RESEARCH_LEDGER.md`.
- Canonical artifacts: `experiments/` (138 tracked: 107 golden JSONs + 31 drivers). Goldens/data pinned per `ledger/golden_baseline.json` and `ledger/data_baseline.json`.
- Baseline integrity guards (`scripts/check.sh`): `check_goldens_clean.py`, `check_golden_baseline.py`, `check_data_coverage.py`, optimizer determinism tests, etc. (see `AGENTS.md`).
- No interrupted verification (`.verify_snapshot/` absent).
- `git status`: ` M src/__pycache__/cache_keys.cpython-312.pyc` only (bytecode timestamp drift; not canonical). No other working-tree changes.

## Initial task for next session

1. **Fast baseline check (offline):**
   ```bash
   SEED=42 bash scripts/check.sh
   # or: make check
   ```
   If golden drift is reported, recover before any commit: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/` only when HEAD is the pinned baseline (see `AGENTS.md`).

2. **If asked to run/extend research:**
   - Pre-register before execution (gates, falsification, sensitivity grid; `pre_registered` block; ledger entry).
   - Verify premises against recorded `experiments/*.json`.
   - New data inputs: commit and re-pin with `python3 scripts/check_data_coverage.py --update`. Re-pin goldens only intentionally via `python3 scripts/check_golden_baseline.py --update` (never as a side effect of verification).
   - After any driver/verification run, restore goldens: `SEED=42 python3 run_all_verification.py --restore-only`.

3. **Verification levels (if requested):**
   - Quick (~8m): `SEED=42 python3 run_all_verification.py` / `make verify-quick`
   - Extended (~21m): `--extended`
   - Full (~15m): `--full`

## Do NOT

- Create `.github/workflows/verification-gate.yml` (use template `.github/workflow-templates/verification-gate.yml` only).
- Commit verification/driver output to `experiments/` or secrets/keys.
- Commit `src/__pycache__` artifacts or move gateposts post-hoc.

## References

- `AGENTS.md` — commands, reproducibility, baseline/integrity rules.
- `ledger/RESEARCH_LEDGER.md` — E001–E169 records/dispositions.
- `ledger/PRIORITIZATION.md` — ranking criteria and procedure.
