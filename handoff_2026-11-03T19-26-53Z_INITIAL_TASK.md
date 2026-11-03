# INITIAL TASK - Handoff for Next Agent Session

**Timestamp (UTC): 2026-11-03T19:26:53Z**
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** main — `7e90fad` "chore(kilo): checkpoint agent session"
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

---

## Goal

Continue quantitative strategy research per `AGENTS.md`. Research phase is complete (E001–E043); surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`. **There is currently NO open task in the queue — this session was a handoff-only turn.** The prior handoff `handoff_2026-11-03T19-26-24Z_INITIAL_TASK.md` is superseded by this one.

## Current State (verified at handoff time)

- Working tree CLEAN (`git status --short` empty); no `experiments/` diff; goldens match HEAD.
- `.verify_snapshot/` ABSENT — no live verification run, nothing to recover.
- `experiments/` holds 107 committed golden JSONs, protected by `ledger/golden_baseline.json`.
- Prior handoffs `handoff_2026-11-03T19-20-36Z_INITIAL_TASK.md` and `handoff_2026-11-03T19-26-24Z_INITIAL_TASK.md` superseded.

## Immediate Priorities (in order)

1. Confirm repo still clean; if `.verify_snapshot/ACTIVE.json` exists, a run was interrupted — run `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`) before anything else.
2. Understand current research status — read `ledger/RESEARCH_LEDGER.md` and `AGENTS.md`.
3. Follow verification discipline strictly:
   - Always `SEED=42`.
   - Never re-pin goldens as a side effect of running the suite.
   - Never leave a verification run half-finished; restore `experiments/` if interrupted.
   - New `data.download()` input requires a committed cache file + `ledger/data_baseline.json` re-pin via `python3 scripts/check_data_coverage.py --update`.
4. **Wait for explicit user task/instructions before taking action.**

## Quick Commands

```bash
ls -la .verify_snapshot/ 2>&1 | head
SEED=42 bash scripts/check.sh
SEED=42 python3 run_all_verification.py --restore-only
SEED=42 python3 run_all_verification.py --full   # ~15 min full verification
```

## Known Invariants / Caveats

- E029, E030 offline-reproducible since 2026-10-20 (data pinned in `data/fundamentals/` and committed panel).
- E041 has remaining numeric drift (1-ulp sensitivity of ill-conditioned QP, 133 diffs) — DO NOT re-pin.
- E042 lead artifact likewise drifts — DO NOT re-pin.
- Optimizer (`src/portfolio_opt.py`) validates on the problem's constraints, never on solver exit status; pinned by `tests/test_portfolio_opt.py`.
- Close-to-close is the v1.2.3 primary convention; overnight decomposition reported alongside.
- Dependencies: `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance); cvxpy/cvxopt optional.
- Repro caveat (documented in `HANDOFF_REPRO_CAVEAT.md`): E041/E042 sensitivity grids are not byte-exact in this sandbox; no gate/decision affected.

## Handoff Message

Repository is clean and checkpointed at `7e90fad`. Pick up from understanding the ledger and current state. Follow all baseline integrity rules strictly. Wait for explicit user instructions before taking any action.

---

*This file is the durable initial-task handoff for the next agentic work session. Update the timestamp and symlinks (`handoff_current.md`, `handoff_next.md`, `NEXT_HANDOFF.md`, `NEXT_SESSION_HANDOFF.md`) when superseded.*