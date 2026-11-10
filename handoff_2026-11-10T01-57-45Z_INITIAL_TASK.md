# INITIAL TASK (Handoff) — 2026-11-10T01:57:45Z

## Objective
Continue from a clean, verified state. The research phase is complete (E001–E043); surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`. Treat committed artifacts under `experiments/` as canonical unless there is an explicit, pre-registered reason to re-pin (see baseline integrity rules).

## Current State
- Branch: `main` (recent commits: checkpoint agent sessions)
- Repo is a reproducible quantitative research repo (US equities/futures/macro, 2014–2026)
- Canonical artifacts: `experiments/*.json`, pinned baselines in `ledger/golden_baseline.json` and `ledger/data_baseline.json`
- Cached data: `data/` (gitignored except pinned vintages in `data/vintages.json`, fundamentals in `data/fundamentals/` per `data/fundamentals_vintages.json`)
- Verification suite exists (`run_all_verification.py`, `scripts/check.sh`, `make verify-*`)

## Immediate Priorities (in order)
1. **Establish a clean baseline**
   - Run `SEED=42 bash scripts/check.sh` (fast: convention-robustness + template validation). If it reports golden mismatches or a stale snapshot, do **not** commit — restore first (`SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/` per AGENTS.md guidance).
2. **Verify reproducibility as needed**
   - Quick: `SEED=42 python3 run_all_verification.py` (~8 min).
   - Extended/Full only if investigating drift or validating changes.
3. **Respect baseline integrity**
   - Never let verification overwrite canonical goldens unattended. `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py` are enforced; re-pinning requires `--update` and must be deliberate/documented.
   - `scripts/check_data_coverage.py` enforces cached inputs match `ledger/data_baseline.json` (offline-capable verification).
4. **Follow project conventions**
   - Pre-registration, multiple-testing discipline (grids reported not gated), negative results recorded honestly.
   - Close-to-close primary; overnight decomposition reported.
   - Determinism notes (optimizer status 8; ill-conditioned QP can cause small numeric drift) — do not silence by re-pinning without justification.

## Known Open/Watch Items (from ledger/AGENTS)
- E041 numeric drift persists under extended checks (optimizer sensitivity) — do not re-pin to hide it.
- Some drivers historically showed floating-point drift; extended comparison accepts bounded numeric drift, fails on structural changes.
- Data coverage is enforced; unpinned inputs require committing + re-pinning.

## Suggested First Action
Run: `SEED=42 bash scripts/check.sh` and report status. If clean, summarize state from `ledger/RESEARCH_LEDGER.md` (surviving strategies/gates) before making changes.

## Notes for Next Agent
- Read `AGENTS.md` for full verification/reproducibility rules before running long suites.
- If interrupted mid-verification, recover with `--restore-only` before committing.
- Do not commit verification outputs; only commit intentional, justified changes with updated docs/ledgers if baselines change.
