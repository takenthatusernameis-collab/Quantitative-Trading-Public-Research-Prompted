# Agentic Handoff — Initial Task

**Created:** 2026-11-12T13:06:54Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Working dir:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Current state

- Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- Canonical research artifacts: `experiments/*.json` (committed goldens). Do not replace with driver output.
- Baseline integrity guards enforced by `scripts/check.sh`: `check_goldens_clean.py`, `check_golden_baseline.py`, `check_data_coverage.py`, optimizer determinism tests, etc. (see `AGENTS.md`).
- No pending verification run; `.verify_snapshot/` has no `ACTIVE.json`.
- `git status`: ` M src/__pycache__/cache_keys.cpython-312.pyc` (build artifact; not part of canonical baseline). Working tree otherwise clean on `main` (`53191374 chore(kilo): checkpoint agent session`).

## Initial task for next session

1. **Baseline check (fast, offline):**
   ```bash
   SEED=42 bash scripts/check.sh
   # or: make check
   ```
   If it reports golden drift, recover with `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/` (only if HEAD is the pinned baseline; see AGENTS.md).

2. **If asked to run/extend research:**
   - Pre-register before execution (gates, falsification, sensitivity grid; `pre_registered` block in output, ledger entry format).
   - Verify handoff premises against recorded `experiments/*.json` before relying on them.
   - New data inputs: commit and re-pin via `python3 scripts/check_data_coverage.py --update`. Golden re-pin only when intentionally replacing baseline via `python3 scripts/check_golden_baseline.py --update` (never as side effect of verification).
   - After any driver/verification run, restore goldens: `SEED=42 python3 run_all_verification.py --restore-only`.

3. **Verification levels (if needed):**
   - Quick (~8m): `SEED=42 python3 run_all_verification.py` / `make verify-quick`
   - Extended (~21m): `--extended`
   - Full (~15m): `--full`

## Do NOT

- Create `.github/workflows/verification-gate.yml` (template only: `.github/workflow-templates/verification-gate.yml`; controller/token constraints).
- Commit verification/driver output to `experiments/`.
- Commit secrets/keys.

## References

- `AGENTS.md` — commands, reproducibility, baseline/integrity rules.
- `ledger/RESEARCH_LEDGER.md` — E001–E043 records and dispositions.
- `ledger/PRIORITIZATION.md` — ranking criteria and procedure.
