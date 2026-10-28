# HANDOFF — Timestamped initial task for next agentic session

**Timestamp (UTC):** 2026-10-28T20-16-16Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Branch:** main
**Working tree:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Research phase:** Complete (E001–E043). Surviving validated strategies are in `ledger/RESEARCH_LEDGER.md`.

## INITIAL TASK (START HERE)

Do **not** re-run full verification blindly. Treat golden integrity as the first gate.

1. **Check golden/state cleanliness**
   ```bash
   git status --short
   SEED=42 python3 scripts/check_goldens_clean.py
   SEED=42 python3 scripts/check_golden_baseline.py
   SEED=42 python3 scripts/check_data_coverage.py
   ```

2. **If anything is dirty/stale or a snapshot is pending**
   - Follow `AGENTS.md` "Baseline Integrity". If `check_goldens_clean.py` reports a stale snapshot from a killed run, recover with:
     ```bash
     SEED=42 python3 run_all_verification.py --restore-only
     ```
   - If `check_golden_baseline.py` fails, **do not re-pin** as a side effect of a verification run. Only re-pin with `python3 scripts/check_golden_baseline.py --update` if explicitly correcting the pinned baseline with justification. The committed golden is authoritative.
   - If `check_data_coverage.py` fails, add/commit the missing tracked cache file and re-pin via `python3 scripts/check_data_coverage.py --update`. Never rely on ad-hoc live downloads during verification (`QUANT_RESEARCH_OFFLINE=1` is enforced by the suite).

3. **Run the fast convention gate**
   ```bash
   SEED=42 bash scripts/check.sh
   # or: make check
   ```
   This runs py_compile + convention robustness + template validation + the golden/data guards.

4. **Assess state and report**
   Read `ledger/RESEARCH_LEDGER.md` (focus on open items). Pay particular attention to **E049** (optimizer determinism / tangency QP ill-conditioning). Note that `src/portfolio_opt.py` must validate on constraints (not solver status) — enforced by `tests/test_portfolio_opt.py` which `scripts/check.sh` runs.

## CURRENT KNOWN CONSTRAINTS

- **Never leave a verification run half-finished.** `run_all_verification.py` backs up `experiments/` to `.verify_snapshot/` (gitignored) with `ACTIVE.json`. Killing it mid-run is recoverable via `--restore-only`, but avoid interrupting.
- **Do not commit verification output.** If `experiments/` differs from HEAD due to an interrupted run, restore before committing.
- **E041/E042 numeric drift is expected.** Ill-conditioned tangency QP gives 1-ulp sensitivity; extended verification may report drift (E041 ~133 numeric diffs) despite identical gates/decisions. Do **not** re-pin to silence this.
- **E029/E030 offline-reproducible.** Fundamentals pinned in `data/fundamentals/`, E030 16-ETF panel committed. Data coverage is enforced.
- **Verification modes:** `verify-quick` (~8m), `verify-extended` (~21m), `verify-full` (~15m). Use `--skip-slow` or `--restore-only` as appropriate.
- **CI workflow cannot be created by agents.** Template at `.github/workflow-templates/verification-gate.yml`.

## FILES TO READ FIRST

- `AGENTS.md` — commands, guards, recovery, reproducibility
- `ledger/RESEARCH_LEDGER.md` — decisions, gates, open items (E049, etc.)
- `ledger/golden_baseline.json` — pinned SHAs
- `ledger/data_baseline.json` — pinned data SHAs
- `scripts/check.sh`, `run_all_verification.py` — verification entrypoints
- `tests/test_portfolio_opt.py` — optimizer determinism contract

## SUGGESTED NEXT ACTION (IF CLEAN)

If all guards pass and `scripts/check.sh` is green, summarize:
- Golden/data integrity: OK
- Stale snapshots: none
- Open ledger items + recommendation for next concrete step (do **not** expand scope beyond repo state; this is research-complete repo)

## Suggested first command
```bash
git status --short && echo "---" && SEED=42 bash scripts/check.sh
```
