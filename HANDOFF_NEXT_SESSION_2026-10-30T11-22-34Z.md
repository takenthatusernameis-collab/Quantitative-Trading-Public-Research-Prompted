# HANDOFF — Next Agentic Work Session

**Timestamp:** 2026-10-30T11:22:34Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Working tree:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**HEAD:** 08166c8 chore(kilo): checkpoint agent session
**Working tree:** uncommitted `__pycache__` .pyc modifications only (no source changes)

---

## INITIAL TASK (do first)

1. **Recover any stale verification snapshot** (blocking, do this before anything else)
   ```bash
   SEED=42 python3 run_all_verification.py --restore-only
   ```
   Fallback: `git checkout -- experiments/`. Never leave a verification run half-finished; the suite overwrites `experiments/*.json` temporarily and restores them afterwards.

2. **Verify baseline integrity**
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   Expect exit 0: py_compile, goldens clean vs HEAD, pinned baseline match (`check_golden_baseline.py`), data coverage (`check_data_coverage.py`), portfolio_opt tests.

3. **If any check fails**
   - Goldens differ from HEAD after restore → restore from the commit whose SHA-256 matches `ledger/golden_baseline.json` via `git checkout <commit> -- experiments/<file>`.
   - Never re-pin to silence drift; re-pinning requires `python3 scripts/check_golden_baseline.py --update` and must appear in the diff.
   - If `.verify_snapshot/ACTIVE.json` reports a live pid, wait for that run to finish or confirm it is dead before starting a new one.

4. **Do not make changes or commit without explicit user direction.** Goldens are authoritative; never modify them as a side effect of verification.

---

## Current state

- **Research phase complete:** E001–E043. Surviving validated strategies in `ledger/RESEARCH_LEDGER.md`.
- **Known open item:** E041 numeric drift (133 numeric diffs) exceeds 1e-4 tolerance in extended verification; structural diffs are gone and gates/decision unchanged (REJECTED 3/5). Do **not** re-pin. E029 and E030 offline-reproducible with 0 differences.
- **Optimizer determinism (E049):** `src/portfolio_opt.py` validates on the problem's constraints, not solver exit status; pinned by `tests/test_portfolio_opt.py`.
- **Data coverage enforced:** every `data.download()` input must be tracked and pinned in `ledger/data_baseline.json`; verification runs with `QUANT_RESEARCH_OFFLINE=1`.

## Immediate priorities for next session

1. Recover stale snapshot, then run `SEED=42 bash scripts/check.sh` (must exit 0).
2. Read `ledger/RESEARCH_LEDGER.md` for any remaining open items; act only on the highest-priority concrete task.
3. If integrity passes and verification is clean, stop and report status — no code changes required unless explicitly directed.

## Quick reference

- Check all conventions: `SEED=42 make check`
- Quick verify: `SEED=42 make verify-quick` (~8 min)
- Extended verify: `SEED=42 make verify-extended` (~21 min)
- Full verify: `SEED=42 make verify-full` (~15 min)
- Recover goldens: `SEED=42 python3 run_all_verification.py --restore-only`
- Convention robustness only: `SEED=42 make verify`

## Constraints & reminders

- Always use `SEED=42`.
- Pre-registration required; sensitivity grids are "reported, not gated"; confirmatory runs need a dedicated pre-registered run with a full placebo before promotion.
- Negative results recorded honestly (REJECTED/PARTIAL).
- Keep responses concise; document deviations in commit messages only if explicitly asked to commit.