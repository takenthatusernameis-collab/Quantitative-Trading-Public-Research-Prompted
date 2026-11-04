# Handoff (2026-11-04T11:53:44Z)

## Repo state
- Branch: main
- Recent commits: f6b6c58, 6f8f6d1, 4e7b929
- Working tree: clean (no uncommitted changes)
- Research phase: complete (E001–E043). Surviving strategies documented in ledger/RESEARCH_LEDGER.md

## Baselines (do not overwrite)
- Golden artifacts: experiments/*.json (pinned). Verification backs up/restores; never leave verification half-finished.
- Baseline hashes: ledger/golden_baseline.json, ledger/data_baseline.json
- Data caches: data/ (gitignored except pinned vintages). E029 fundamentals pinned in data/fundamentals/ per data/fundamentals_vintages.json.

## Known open items (from AGENTS.md)
- E041 numeric drift: optimizer determinism fixed (validator uses problem constraints), but tangency QP is ill-conditioned → ~133 numeric diffs remain in extended verification. Do NOT re-pin to silence; see ledger E049 open item.
- E030/E029: now reproducible offline with pinned inputs; goldens re-pinned deliberately.
- Cache coverage enforced by scripts/check_data_coverage.py (offline mode in verification).

## Clear initial task for next session
1. **Verify baseline integrity first** (fast):
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   This runs goldens-clean, golden-baseline, data-coverage, convention-robustness, and tests.

2. **Run extended verification to see current drift state**:
   ```bash
   SEED=42 python3 run_all_verification.py --extended
   ```
   Review `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json` (gitignored). Pay special attention to E041 (numeric vs structural diffs) and confirm counts match expectations.

3. **Address E041 open item per ledger**: Determine whether the remaining 133 numeric diffs are acceptable as 1-ulp sensitivity or require a different approach (do not re-pin). Document decision in ledger/RESEARCH_LEDGER.md with evidence from the extended report.

## Quick repro commands
- Quick: `SEED=42 python3 run_all_verification.py`
- Full: `SEED=42 python3 run_all_verification.py --full`
- Recover if interrupted: `SEED=42 python3 run_all_verification.py --restore-only`

## Notes
- Always use SEED=42. Verification overwrites experiments/ temporarily; recovery is automatic at startup or via --restore-only.
- If golden-baseline check fails, do not re-pin as side effect of verification — follow AGENTS.md guidance.
