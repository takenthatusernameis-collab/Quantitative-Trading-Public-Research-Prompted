# HANDOFF — Timestamped initial task for next agentic session

Timestamp (UTC): 2026-10-28T07:29:59Z
Repo: Quantitative-Trading-Public-Research-Prompted
Branch: main
HEAD: 1ebed83083958d29fbf63add38d359fa6798f8c8
Working tree: modified (__pycache__ only; no tracked source changes)
Verify snapshot: none active (.verify_snapshot/ACTIVE.json absent)

## Current state summary
- Research phase complete (E001–E043). Surviving validated strategies documented in ledger/RESEARCH_LEDGER.md.
- Verification guards in place: check_goldens_clean.py, check_golden_baseline.py, check_data_coverage.py; optimizer determinism constraint pinned by tests/test_portfolio_opt.py.
- Data caches: pinned vintages in data/vintages.json (2026-10-12) and committed 2026-10-11 vintage; E029 fundamentals pinned in data/fundamentals/ per data/fundamentals_vintages.json.
- Verification: run_all_verification.py supports --quick/--extended/--full/--skip-slow/--restore-only. Backups in .verify_snapshot/ (gitignored) with ACTIVE.json marker.
- Modified files now are only __pycache__ artifacts (no tracked source changes).

## Immediate priorities (start here)
1. **Baseline hygiene** — Ensure working tree clean of uncommitted tracked changes before running verification. If any tracked files change, follow AGENTS.md baseline integrity rules (do not re-pin goldens as side effect of verification).
2. **Run verification** — Decide scope:
   - Fast: SEED=42 bash scripts/check.sh (convention-robustness + template validation)
   - Quick: SEED=42 python3 run_all_verification.py (~8 min)
   - Extended: SEED=42 python3 run_all_verification.py --extended (~21 min) — note E041 still has numeric drift (133 diffs) per optimizer ill-conditioning; do not re-pin.
   - Full: SEED=42 python3 run_all_verification.py --full only if needed.
3. **If verification interrupted** — Recovery: SEED=42 python3 run_all_verification.py --restore-only (or git checkout -- experiments/). Check .verify_snapshot/ACTIVE.json.
4. **Data coverage** — If adding new data inputs, commit files and re-pin with `python3 scripts/check_data_coverage.py --update` (never rely on live yfinance in offline verification).

## Known open items (from AGENTS.md)
- E041 numeric drift (133 differences) remains due to 1-ulp QP sensitivity (ill-conditioned tangency). Structural differences resolved; gates/decisions unchanged. Do not silence by re-pinning — open item in ledger.
- CI workflow cannot be created by agents (controller restores .github/workflows/; repo token lacks workflows push). Template at .github/workflow-templates/verification-gate.yml.

## Suggested first command for next session
```bash
SEED=42 bash scripts/check.sh
```
If it passes, consider `SEED=42 python3 run_all_verification.py --quick`. Do not commit verification output; restore goldens if left modified.

## Notes
- Always use SEED=42.
- Close-to-close is primary convention v1.2.3; overnight decomposition reported.
- Pre-registration and multiple-testing discipline apply.
