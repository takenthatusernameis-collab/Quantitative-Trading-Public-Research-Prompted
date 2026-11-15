# HANDOFF — Initial Task Message

**Timestamp:** 2026-11-15T17:19:37Z
**Session:** ses_e1fc752dbffexd4ZTm2uj8e8XO (main agent, state: busy)
**Working directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

---

## Repository Context

This is an independent reproducible quantitative-strategy research repository covering 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. **Research phase E001–E043 is complete.** Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Current State

- Working tree is clean except for a stale untracked pyc: `src/__pycache__/cache_keys.cpython-312.pyc` (safe to ignore).
- Recent commits are all `chore(kilo): checkpoint agent session` checkpoints.
- The verification suite (`run_all_verification.py`) backs up `experiments/*.json` goldens to `.verify_snapshot/` before re-running and restores them afterward — the baseline is never modified by verification.
- Board is empty; no pending peer tasks.

## Standing Conventions & Invariants

1. **Baseline integrity**: Never commit verification output. If a run is interrupted, restore with `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`). A live run is signaled by `.verify_snapshot/ACTIVE.json`; the suite refuses to start while one exists.
2. **Golden guard**: `ledger/golden_baseline.json` pins SHA-256 fingerprints of tracked `experiments/` artifacts. Replacing an artifact requires re-pinning via `python3 scripts/check_golden_baseline.py --update` — never as a side effect of running verification.
3. **Data coverage**: `scripts/check_data_coverage.py` enforces that every `data.download()` call site resolves to a git-tracked, SHA-pinned cache file. Verification runs with `QUANT_RESEARCH_OFFLINE=1`, so a missing entry fails hard.
4. **Reproducibility**: Always use `SEED=42`. Offline mode is enforced during verification. yfinance is not bit-reproducible; any unpinned input is a live download.
5. **Convention**: Close-to-close is the v1.2.3 primary convention; overnight decomposition is reported alongside for every strategy.
6. **Multiple-testing discipline**: Sensitivity grids are "reported, not gated." A config that clears gates in the grid requires a dedicated pre-registered confirmatory run with a full placebo before promotion.
7. **Negative results**: Recorded honestly (REJECTED / PARTIAL) with evidence.
8. **Optimizer determinism** (ledger E049): `src/portfolio_opt.py` validates a solver answer on the problem's constraints, never on the solver's exit status. SLSQP can report status 8 ("Positive directional derivative for linesearch") at a constrained optimum while returning a feasible, optimal point; gating on it made the tangency portfolio environment-dependent. The rule is pinned by `tests/test_portfolio_opt.py`.

## Key Files

- `ledger/RESEARCH_LEDGER.md` — authoritative strategy record (E001–E043+)
- `ledger/golden_baseline.json` — pinned SHA-256 fingerprints for `experiments/`
- `ledger/data_baseline.json` — data cache coverage pins
- `AGENTS.md` — full project commands, conventions, and CI/automation notes
- `scripts/check.sh` — fast convention-robustness check + template validation
- `run_all_verification.py` — verification suite (quick / extended / full modes)

## Quick Commands

```bash
SEED=42 bash scripts/check.sh            # fast check
SEED=42 python3 run_all_verification.py --skip-slow   # convention only
SEED=42 python3 run_all_verification.py --restore-only # recover goldens
SEED=42 python3 run_all_verification.py --full        # full verification
```

## Notes for Next Session

- If asked about Kilo capabilities, consult https://kilo.ai/docs via WebFetch.
- Do not create the CI workflow file (`.github/workflows/verification-gate.yml`) — it requires maintainer action via GitHub UI; a copyable template exists at `.github/workflow-templates/verification-gate.yml`.
- Do not re-pin E041/E042/E030/E029 goldens to silence floating-point drift unless instructed — see the open items in the ledger.