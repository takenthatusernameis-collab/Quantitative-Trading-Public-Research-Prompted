# Handoff — Next Agentic Session

**Timestamp:** 2026-10-31T08:09:35Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** see `git log -1 --oneline`
**Working tree state:** inspect with `git status --short`

## Context
- Research phase complete (E001–E043). Surviving validated strategies are in `ledger/RESEARCH_LEDGER.md`.
- `experiments/*.json` are canonical goldens. The verification suite backs up/restores them; **never leave a verification run half-finished**.
- Baseline integrity guards are enforced: `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`. Data coverage is enforced (unpinned inputs fail offline).
- Key known open items (from AGENTS.md / ledger): E041 optimizer-drift remains (ill-conditioned QP) — do **not** re-pin to silence; E049 fixed solver gating but numeric drift persists. E029/E030 made offline-reproducible with pinned data.
- Verification commands: `make check` (fast), `make verify-quick` (~8m), `make verify-extended` (~21m), `make verify-full` (~15m). Always use `SEED=42`.

## Immediate Task (clear starting point)
1. **Verify baseline integrity first** (must be clean before any changes):
   ```bash
   SEED=42 make check
   ```
   If this fails, follow recovery: `SEED=42 python3 run_all_verification.py --restore-only` or restore specific files from `HEAD`/pinned commit. Do not proceed until clean.

2. **Read the ledger and open items**:
   - `ledger/RESEARCH_LEDGER.md` — understand E041/E049 status and promotion gates.
   - `ledger/golden_baseline.json` and `ledger/data_baseline.json` — know what’s pinned.
   - `tests/test_portfolio_opt.py` — documents the solver-gating rule (must hold).

3. **Decide next concrete action** (pick one, don’t expand scope):
   - If baseline is clean and you need to investigate E041 drift further: reproduce with extended comparison and inspect `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json` (gitignored) without modifying goldens.
   - If adding/fixing data: commit the file and re-pin via `python3 scripts/check_data_coverage.py --update` (only if necessary and justified).
   - If changing code affecting artifacts: run targeted verification for affected drivers first; never re-pin goldens as a side effect of a verification run.

## Constraints
- Do **not** commit verification output. If interrupted, restore goldens before committing.
- Never re-pin `experiments/*.json` to silence numeric drift unless there is an explicit, justified reason recorded in the ledger.
- Use `SEED=42` for all runs. Run offline where possible (`QUANT_RESEARCH_OFFLINE=1` is used by verification).
- Follow pre-registration/multiple-testing discipline; goalposts are never moved post-hoc.
- Do not create GitHub workflows (controller restores them; token lacks `workflows` permission).

## Quick Commands
```bash
# Integrity
SEED=42 make check

# Inspect state
git status --short && git log -1 --oneline
python3 scripts/check_golden_baseline.py
python3 scripts/check_data_coverage.py

# Recovery if needed
SEED=42 python3 run_all_verification.py --restore-only
```

## Files to read first
- `AGENTS.md` (full)
- `ledger/RESEARCH_LEDGER.md`
- `run_all_verification.py` (understand backup/restore/snapshot ownership)
- `scripts/check.sh` (integrity steps)
- `src/portfolio_opt.py` + `tests/test_portfolio_opt.py` (if touching optimizer)
