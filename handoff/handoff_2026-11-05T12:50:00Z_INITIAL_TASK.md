# Initial Task for Next Agentic Work Session
Timestamp (UTC): 2026-11-05T12:50:00Z
HEAD: e912164e96fd0afb070569f8351ba71f5205d6a4 (2026-11-05 12:49:33 +0000, "chore(kilo): checkpoint agent session")

## Repository State
- **Research phase**: Complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- **Baseline**: 138 tracked `experiments/*.json` goldens match HEAD; no `.verify_snapshot/` present (no interrupted verification run).
- **Working tree**: Clean at time of handoff creation.
- **Prior handoffs**: State adopted from recent handoffs (e.g., `handoff/handoff_2026-11-05T12-49-07Z_INITIAL_TASK.md`). The stale-task correction from E086 remains in effect: cost sensitivity on `large_liquid` is **already complete as E005** (`cost_sweep.py` → `experiments/cost_sensitivity.json`, pinned in `ledger/golden_baseline.json`). Do not re-execute it.

## Immediate Priorities (before any changes)
1. **Baseline integrity check**
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   If it reports a golden mismatch or stale snapshot pending, recover first:
   `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/` only if HEAD is known-good and matches `ledger/golden_baseline.json`). **Never commit verification output.**

2. **Confirm open work**
   - Review `ledger/RESEARCH_LEDGER.md` (tail / open items) for any genuinely open, pre-registrable task.
   - If no open items remain, report repository closed and do not invent new work.

## Verification Commands (reference)
```bash
make check                  # fast: convention + golden checks (~seconds)
make verify                 # convention robustness only
make verify-quick           # SEED=42 python3 run_all_verification.py (~8 min)
make verify-extended        # --extended (~21 min)
make verify-full            # --full (~15 min, E042 n_sim=50 + grid)
SEED=42 python3 run_all_verification.py --restore-only  # recover interrupted run
```

## Conventions / Constraints (must follow)
- **Reproducibility**: Always `SEED=42` for stochastic/verification runs.
- **Pre-registration**: Any new experiment requires pre-registered gates, falsification expectations, and sensitivity grid before execution. Do not move goalposts post-hoc.
- **Multiple-testing discipline**: Sensitivity grids are reported, not gated; a config clearing gates in a grid needs a dedicated pre-registered confirmatory run + full placebo before promotion.
- **Goldens**: `experiments/*.json` are canonical. Never re-pin as a side effect of verification. `git checkout -- experiments/` restores HEAD (which may be bad if a checkpoint captured verification output) — prefer `--restore-only` or restore the SHA pinned in `ledger/golden_baseline.json`.
- **Data**: Pinned vintages in `data/vintages.json` / `data/fundamentals_vintages.json`. Verification runs with `QUANT_RESEARCH_OFFLINE=1`; cache coverage enforced by `scripts/check_data_coverage.py`.
- **Project config**: Use `.kilo/` for commands/agents (not `.kilocode/` or `.opencode/`).
- **Commits**: Do not commit interrupted verification artifacts or unpinned golden changes.

## Suggested Next Action
Run `SEED=42 bash scripts/check.sh`. If clean and ledger shows no open items, the session can close with a status report. If an open, pre-registrable item exists, propose it (objective, gates, falsification, data) before implementation.
