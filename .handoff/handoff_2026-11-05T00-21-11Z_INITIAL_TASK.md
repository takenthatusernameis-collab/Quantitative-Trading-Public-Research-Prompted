# INITIAL TASK FOR NEXT AGENTIC SESSION

**Timestamp:** 2026-11-05T00:21:11Z
**Repo:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Branch:** (check `git branch -a` on start)
**Handoff Type:** Durable handoff (leave this for next agent)

## Mission
Continue work from the verified research baseline. Research phase is complete (E001–E043); surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`. Treat committed artifacts as authoritative.

## Read First (in order)
1. `AGENTS.md` - Commands, conventions, golden baseline guards, verification flows
2. `ledger/RESEARCH_LEDGER.md` - Surviving strategies, rejected/partial, open items (pay special attention to E049/open drift items)
3. `ledger/golden_baseline.json` and `ledger/data_baseline.json` - Pinned fingerprints (do **not** re-pin casually)
4. Most recent handoff: `.handoff/handoff_2026-11-05T00-20-27Z_INITIAL_TASK.md`

## Current State (known)
- **Verification guards enforced:** `.verify_snapshot/` with `ACTIVE.json`, `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`. A live run is reported, not failed.
- **Extended/quick/full verification** available via `run_all_verification.py` / `make verify-*`. Drivers re-run under `QUANT_RESEARCH_OFFLINE=1` in suite context.
- **Optimizer determinism (E049):** `src/portfolio_opt.py` validates on constraints (not solver exit status). Ill-conditioned QP can produce small numeric drift (1-ulp); do **not** re-pin artifacts to silence drift.
- **Data coverage:** all `data.download()` sites must have committed/pinned cache files matching `ledger/data_baseline.json`. Missing entries fail hard in verification.
- **Convention:** close-to-close primary (overnight decomposition reported). Fundamentals for E029 pinned in `data/fundamentals/` per `data/fundamentals_vintages.json`.

## Immediate Actions (on session start)
- [ ] `git status --short && git log --oneline -5`
- [ ] `SEED=42 bash scripts/check.sh` (fast convention-robustness + guards). If it reports golden/data mismatch and no active verification, follow AGENTS.md recovery (do **not** commit a captured run).
- [ ] If `.verify_snapshot/ACTIVE.json` exists from a crashed run: `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/` with care per AGENTS.md)
- [ ] Review open items in `ledger/RESEARCH_LEDGER.md` before making changes

## Safe Working Rules
- **Never leave verification half-finished.** Always restore goldens if interrupted.
- **Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` as a side effect of running verification.** Only re-pin if you intentionally changed a canonical artifact with justification and you update the ledger/fingerprints explicitly.
- **Do not overwrite `experiments/*.json` by running the full suite and committing.** The suite backs up/restores; committing captured outputs is the historical mistake to avoid.
- **Pre-register changes.** Follow pre-registration, multiple-testing discipline ("reported not gated"), and document negative results.
- **Offline when verifying.** Driver runs in verification use offline mode; adding new inputs requires committing cache and re-pinning data baseline.

## Suggested Tasks (pick one if unassigned)
- Investigate/resolve open ledger items (esp. E049 numeric drift policy) without re-pinning artifacts
- Strengthen guards/tests if touching optimizer/data loading/verification
- Document or clean up stale handoffs if requested
- Only run extended/full verification if you need to reproduce a specific drift report

## Verification Quick Reference
```bash
SEED=42 bash scripts/check.sh                # ~seconds
SEED=42 python3 run_all_verification.py      # quick ~8min
SEED=42 python3 run_all_verification.py --extended  # ~21min
SEED=42 python3 run_all_verification.py --full      # ~15min
SEED=42 python3 run_all_verification.py --restore-only
```

## Notes
- Symlinks `handoff_next_session*.md` in repo root may point to older handoffs; prefer files in `.handoff/` by timestamp.
- If you create a new handoff, write to `.handoff/` with ISO-like UTC timestamp and consider updating `handoff_next_session.md` symlink to point to it.
