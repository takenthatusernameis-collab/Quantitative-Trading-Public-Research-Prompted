# Handoff (timestamped)

- Created: 2026-10-29T20:46:50Z
- Branch: main
- HEAD: 34e0b1d (chore(kilo): checkpoint agent session) by kilo-autonomous at 2026-10-29 20:46:42 +0000
- Working tree: had stale .pyc artifacts from previous runs; goldens were restored after detecting stale snapshot (pid 39093) via `run_all_verification.py --restore-only`.

## Repo state (summary)
- Research phase complete (E001–E043). Surviving validated strategies in `ledger/RESEARCH_LEDGER.md`.
- Canonical artifacts: `experiments/*.json` (goldens). Verification may overwrite temporarily; snapshot lives in `.verify_snapshot/` (gitignored). Guards: `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`.
- Data: cached parquet in `data/` (gitignored except pinned vintages). `data/vintages.json` pins 2026-10-12; 2026-10-11 committed for specific experiments. Fundamentals pinned in `data/fundamentals/` for E029 offline reproducibility. `scripts/check_data_coverage.py` enforces cache coverage.
- Optimizer determinism note (E049): tangency QP ill-conditioned; SLSQP status 8 acceptable if feasible/optimal (validated on constraints). Some grid artifacts still drift numerically; do not re-pin to silence.

## Verification status (current)
- Goldens restored clean to committed baseline (snapshot recovered).
- Quick local sanity: `SEED=42 bash scripts/check.sh` runs fast convention-robustness + template validation. Full suite: `make verify-quick` (~8 min), `make verify-extended` (~21 min), `make verify-full` (~15 min).
- Extended: E029/E030 now reproducible offline (0 diffs). E041 still shows numeric drift (133) with structural diffs resolved; tracked as open in ledger (do not re-pin).
- CI workflow template at `.github/workflow-templates/verification-gate.yml`; actual workflow cannot be created by agents (controller restores/cleans `.github/workflows/`).

## Clear initial task for next session
1. **Sanity check**: Run `SEED=42 bash scripts/check.sh` from repo root. Ensure no golden mismatch and all fast checks pass. If snapshot issues reappear, use `run_all_verification.py --restore-only`.
2. **Pick next action** (suggested):
   - If you need confidence: run `SEED=42 python3 run_all_verification.py --skip-slow` (convention-only) or `--quick`.
   - If modifying code that affects portfolio optimization/data/loading: pay attention to E041/E042 numerical stability and cache coverage (update pins via the scripts if adding data).
   - If changing experiments/artifacts: **never** re-pin goldens as a side effect of verification; use `python3 scripts/check_golden_baseline.py --update` only with explicit justification and record in ledger.
3. **Constraints**: Follow conventions in AGENTS.md (pre-registration, no post-hoc goalpost moves, don’t commit verification output mid-run). Use `SEED=42`. Keep changes minimal and verify with relevant checks/tests.

## Pointers
- Ledger: `ledger/RESEARCH_LEDGER.md`
- Verification entrypoint: `run_all_verification.py`
- Guards: `scripts/check_*.py`
- Data coverage: `scripts/check_data_coverage.py` / `ledger/data_baseline.json`
- Golden baseline: `scripts/check_golden_baseline.py` / `ledger/golden_baseline.json`
