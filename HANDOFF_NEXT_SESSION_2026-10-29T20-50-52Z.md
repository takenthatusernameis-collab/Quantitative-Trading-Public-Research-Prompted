# Handoff (timestamped)

- Created: 2026-10-29T20:50:30Z
- Branch: main
- HEAD: 34e0b1d (chore(kilo): checkpoint agent session) by kilo-autonomous at 2026-10-29 20:46:42 +0000
- Working tree: goldens restored clean to committed baseline; stale snapshot recovered.

## Repo state (summary)
- Research phase complete (E001–E043). Surviving validated strategies in `ledger/RESEARCH_LEDGER.md`.
- Canonical artifacts: `experiments/*.json` (goldens). Verification may overwrite temporarily; snapshot lives in `.verify_snapshot/` (gitignored). Guards: `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`.
- Data: cached parquet in `data/` (gitignored except pinned vintages). Fundamentals pinned for E029. Cache coverage enforced.
- Optimizer determinism note (E049): tangency QP ill-conditioned; SLSQP status 8 acceptable if feasible/optimal (validated on constraints). Some grid artifacts still drift numerically; do not re-pin to silence.

## Clear initial task for next session
1. **Sanity check**: Run `SEED=42 bash scripts/check.sh` from repo root. Ensure no golden mismatch and all fast checks pass. If snapshot issues reappear, use `run_all_verification.py --restore-only`.
2. **Pick next action** (suggested):
   - If you need confidence: run `SEED=42 python3 run_all_verification.py --skip-slow` or `--quick`.
   - If modifying code affecting portfolio optimization/data/loading: pay attention to E041/E042 numerical stability and cache coverage (update pins via scripts if adding data).
   - If changing experiments/artifacts: never re-pin goldens as a side effect of verification; use `python3 scripts/check_golden_baseline.py --update` only with explicit justification and record in ledger.
3. **Constraints**: Follow conventions in AGENTS.md (pre-registration, no post-hoc goalpost moves, don't commit verification output mid-run). Use `SEED=42`. Keep changes minimal and verify with relevant checks/tests.

## Pointers
- Ledger: `ledger/RESEARCH_LEDGER.md`
- Verification entrypoint: `run_all_verification.py`
- Guards: `scripts/check_*.py`
- Data coverage: `scripts/check_data_coverage.py` / `ledger/data_baseline.json`
- Golden baseline: `scripts/check_golden_baseline.py` / `ledger/golden_baseline.json`
