# Handoff — Next Agentic Session (2026-10-28T00:45:22Z)

## Repo state
- Branch: main
- HEAD: e72e763
- Working tree: see git status below
- Verification: Research phase complete (E001–E043). Surviving validated strategies in ledger/RESEARCH_LEDGER.md.

## Git status (short)
 M scripts/__pycache__/check_data_coverage.cpython-312.pyc
 M scripts/__pycache__/check_golden_baseline.cpython-312.pyc
 M scripts/__pycache__/check_goldens_clean.cpython-312.pyc
 M scripts/__pycache__/check_json_artifacts.cpython-312.pyc
 M scripts/__pycache__/diff_golden.cpython-312.pyc
 M src/__pycache__/cache_keys.cpython-312.pyc
 M src/__pycache__/data.cpython-312.pyc
 M src/__pycache__/offline.cpython-312.pyc
 M src/__pycache__/portfolio_opt.cpython-312.pyc
 M tests/__pycache__/test_data_coverage.cpython-312.pyc
 M tests/__pycache__/test_drift_report.cpython-312.pyc
 M tests/__pycache__/test_golden_baseline.cpython-312.pyc
 M tests/__pycache__/test_goldens_guard.cpython-312.pyc
 M tests/__pycache__/test_json_guard.cpython-312.pyc
 M tests/__pycache__/test_portfolio_opt.cpython-312.pyc
?? HANDOFF_NEXT_SESSION_2026-10-28T00:45:22Z.md

## Recent commits
e72e763 chore(kilo): checkpoint agent session
9cb265c chore(kilo): checkpoint agent session
1f70e9f chore(kilo): checkpoint agent session
55412e8 chore(kilo): checkpoint agent session
e4f549d chore(kilo): checkpoint agent session

## Active constraints / must-know
- Seeds: always SEED=42 for verification/repro runs.
- Baselines: experiments/*.json are canonical. Verification overwrites/backups them (local .verify_snapshot/). Never leave a verification run half-finished; use run_all_verification.py --restore-only or git checkout -- experiments/ if needed.
- Guards: scripts/check_goldens_clean.py (working tree vs HEAD) and scripts/check_golden_baseline.py (artifacts vs ledger/golden_baseline.json SHA-256) are first-class in check.sh. Re-pin only with explicit script (python3 scripts/check_golden_baseline.py --update) when legitimately replacing a golden.
- Data coverage: scripts/check_data_coverage.py enforces cached inputs exist/tracked/match ledger/data_baseline.json. Run with QUANT_RESEARCH_OFFLINE=1 in verification.
- Optimizer: src/portfolio_opt.py validates on constraints (not solver exit status). Tangency QP remains ill-conditioned (small numeric drift possible). Don't silence by re-pinning.
- Drivers: verify-quick (8), verify-extended (+18), verify-full (E042 n_sim=50 + grid). Extended drift report in .verify_reports/VERIFICATION_EXTENDED_SUMMARY.json (gitignored).
- CI: verification-gate workflow cannot be auto-created (controller restores .github/workflows/); template at .github/workflow-templates/verification-gate.yml.

## Quick verification
- Fast check: SEED=42 bash scripts/check.sh  (or make check)
- Quick verify: SEED=42 python3 run_all_verification.py  (or make verify-quick)
- Extended: SEED=42 python3 run_all_verification.py --extended  (or make verify-extended)
- Full: SEED=42 python3 run_all_verification.py --full  (or make verify-full)
- Convention robustness: SEED=42 python3 verify_convention_robustness.py  (or make verify)

## Immediate tasks for next session
1. Check working tree cleanliness / untracked artifacts (.pyc files modified). Decide whether to clean (__pycache__) or leave; they are gitignored? Check .gitignore.
2. If verification was interrupted previously, ensure no stale .verify_snapshot/ACTIVE.json remains and goldens match HEAD/baseline. Run scripts/check_goldens_clean.py and scripts/check_golden_baseline.py.
3. Run a quick sanity check (check.sh) to confirm guards pass.
4. Review ledger/RESEARCH_LEDGER.md for any open items (E041 numeric drift noted; cache coverage enforced).
5. If changes needed, follow project conventions (pre-registration, no golden replacement without re-pinning, offline where applicable).

## Notes
- Cache: data/ gitignored except pinned vintages (2026-10-11 committed, 2026-10-12 pinned in data/vintages.json). Fundamentals pinned separately.
- Do not commit verification outputs; restore goldens if interrupted.
- Commits are checkpoint commits (chore(kilo): checkpoint agent session).
