# Durable Handoff — Quantitative-Trading Research

**Session ended:** 2026-11-16T13:43:23Z
**Branch:** default (git HEAD = fa6aebe5 "chore(kilo): checkpoint agent session")

## Working-tree state

`git status --short` shows only compiled `__pycache__/*.pyc` files modified (build artifacts, not source). No source files are uncommitted. Verify with `git status --short` before starting; clean any stray `.pyc`/`.json` output if present.

## Project conventions (read AGENTS.md fully before acting)

- Experiments under `experiments/*.json` are committed golden artifacts. Verification backs them up and restores them; a half-finished run leaves driver output in the tree — restore with `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`).
- Repo-local snapshot: `.verify_snapshot/ACTIVE.json` holds owning pid; do not start verification while a live run owns it.
- `scripts/check.sh` runs convention checks + goldens clean + golden baseline + tests.
- Cache invariant: every `data.download()` call site must resolve to a tracked cache file pinned in `ledger/data_baseline.json`; unpinned input = live yfinance download = non-reproducible. Run offline with `QUANT_RESEARCH_OFFLINE=1`.
- Seed: always `SEED=42`.

## Immediate next task (initial task message)

**Run the fast convention check and confirm a clean tree:**

```
SEED=42 bash scripts/check.sh
# or: make check
```

Expected outcome: no failures. If it reports golden mismatches, fix them BEFORE committing (do not let a verification run silently replace the baseline).

If clean, proceed to verification:
```
SEED=42 python3 run_all_verification.py --skip-slow   # convention + 8 drivers, fast
SEED=42 python3 run_all_verification.py               # quick full (~8 min)
```

## Key files / commands

- `AGENTS.md` — project commands & conventions (authoritative)
- `scripts/check.sh` — convention-robustness check + template validation
- `run_all_verification.py` --quick / --extended / --full / --skip-slow / --restore-only
- `scripts/check_data_coverage.py --update` — to pin a new data input
- `scripts/check_golden_baseline.py --update` — to re-pin an experiment artifact
- `tests/test_portfolio_opt.py` — pins optimizer determinism rule (first-class step of check.sh)

## Open items from AGENTS.md (ledger)

- E041 (market-neutral portfolio): optimizer determinism fixed; 133 numeric diffs remain (ill-conditioned QP, 1-ulp sensitivity) exceeding 1e-4 tolerance. Do NOT re-pin to silence. Open item in ledger.
- E042 (min-var confirmatory): PARTIAL; `--n-sim 50` confirmatory run.
- E029 / E030 now offline-reproducible (0 diffs) since 2026-10-20.
