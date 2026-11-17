# Durable Handoff — Next Agentic Work Session

**Timestamp (UTC):** 2026-11-17T04:23:27Z
**Handoff ID:** E436 (durable handoff refresh)
**HEAD:** `08b6bc3b5b65d359a38257fa00bd9716ba18fcca` "chore(kilo): checkpoint agent session"
**Branch:** `main` (`origin/main` == HEAD; `git rev-list --left-right --count origin/main...HEAD` → `0 0`, in sync)
**Working tree:** clean (`## main...origin/main`); `.verify_snapshot/` and `.verify_reports/` absent (no interrupted verification run)

---

## INITIAL TASK MESSAGE (for the next agentic work session)

> **Timestamped initial task — 2026-11-17T04:23:27Z.**
>
> This is a fresh durable handoff. **No new research task is assigned.** The
> repository is in a CLOSED / research-complete state.
>
> On session start, do the following **before any work**:
>
> 1. Read this file and `AGENTS.md` in full.
> 2. Check the shared board (`board_read`) for any pending task assignment from
>    the coordinator. If a task is posted, follow it within the guardrails below.
> 3. If **no** task is posted, the only valid action is **conformance
>    re-verification** (no new strategy research):
>    a. `SEED=42 bash scripts/check.sh` — confirm the golden baseline is still clean.
>    b. Confirm `git diff --stat HEAD -- experiments/` is empty (canonical baseline untouched).
>    c. If clean, the repository is verified-closed; report closure.
> 4. Refresh this handoff only when asked: capture live `date -u` / HEAD / sync
>    state, write a new timestamped `handoff_<ISO>Z_INITIAL_TASK.md`, mirror it to
>    `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/`, then run
>    `python3 scripts/repoint_handoff.py <new-file>`.
> 5. **Do not commit** unless the user explicitly directs you to.

---

## Repository State: CLOSED / BASELINE EXPECTED CLEAN

- **Research phase complete** (E001–E043 core; ledger recorded through E435).
- **Golden artifacts:** canonical fingerprints pinned in `ledger/golden_baseline.json`
  (verify with `scripts/check.sh` / `scripts/check_golden_baseline.py`).
- **Convention robustness:** policy v1.2.3 (primary = close-to-close); overnight
  reported alongside for every strategy.
- **No live verification run expected:** `.verify_snapshot/` should be absent.
- **Baseline integrity:** `git diff --stat HEAD -- experiments/` should be empty
  before any commit.

## Surviving Validated Strategies (from E040 close-out)

| Strategy | OOS Sharpe (c2c) | OOS Sharpe (overnight) | Beta vs SPY | Key Property |
|---|---|---|---|---|
| TSM Pure (Equity Flagship) | 1.739 | 2.157 | -0.119 (c2c) / -0.065 (ovn) | Cost-robust, equity-β-bearing |
| Dollar-Neutral Low-Beta Sort | 1.053 | 1.287 | +1.02 (c2c) / -0.035 (ovn) | Market-neutral under overnight only |
| Futures TSM 18m (de-seamed) | 0.805 | balanced | -0.010 | Cross-asset trend, positive bear Sharpe |
| Futures Carry (Roll Yield) | 0.523 | balanced | +0.014 | Best bear-market Sharpe in repo (+0.91) |
| Macro Momentum (Brooks 2017) | 0.006 | 0.428 | -0.011 | Genuine crisis alpha (COVID +2.01, 2022 +1.87) |
| Low-Vol Flagship (unlevered) | 1.728 | not reported | +1.084 | Strongest equity-c2c edge, β-bearing |

## All Other Experiments: REJECTED or DATA-INFEASIBLE

34 experiments (E021–E039, E041–E043) are rejected with honest negatives or are
data-infeasible. Key closure results:
- **E041** (max-sharpe market-neutral blend): REJECTED 3/5 (G3 |β|≤0.1 fails, G2 placebo z fails).
- **E042** (min-variance confirmatory): PARTIAL 4/5 (G1/G3/G4/G5 pass; G2 placebo z 1.73 < 3.0 fails).
- **E042b** (sensitivity-grid lead): REJECTED 4/5 (G2 placebo z 1.96 < 3.0 fails).
- **E049/E050**: exact KKT enumeration closes the tangency-QP open item; E041/E042 grid artifacts reproduce with 0 diffs.

## Open Items (documented, do NOT "fix" by re-pinning)

1. **Tangency QP ill-conditioning (E049):** a 1-ulp perturbation still moves
   `min_var` answers by ~1e-05; E041/E042 grid artifacts would drift by 29–133
   diffs if re-pinned. Do **not** re-pin to silence this.
2. **DN low-beta c2c β sign reversal (E041):** the component is only
   market-neutral under the overnight convention, not close-to-close.

## Constraints for Next Session (guardrails — must honor)

- **SEED=42** always (walk-forward + placebo RNG).
- **No goalpost moves:** gates, pre-registration, falsification expectations,
  sensitivity grids, tolerances, decisions, and validated constructions are frozen.
- **No golden re-pins** (`ledger/golden_baseline.json` / `experiments/*.json`) as a
  side effect of running verification; any replacement must be an explicit `--update`
  visible in the diff.
- **No verification output committed.** If a run is interrupted, recover with
  `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`
  only when HEAD is the intended baseline).
- **Primary convention = close-to-close** (v1.2.3); mixed-convention portfolios prohibited.
- Do not commit `__pycache__` or secrets.

## Available Commands

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh                    # or: make check

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py          # or: make verify-quick

# Extended verification (~21 min; structural match, numeric_tol=1e-4)
SEED=42 python3 run_all_verification.py --extended   # or: make verify-extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full        # or: make verify-full

# Convention robustness only (reads JSONs, no writes)
SEED=42 python3 verify_convention_robustness.py        # or: make verify

# Recover golden artifacts after an interrupted verification run
SEED=42 python3 run_all_verification.py --restore-only
```

## Next Bounded Task (if any)

The repository is closed. No new strategy family is warranted on free public data
sources (all exhausted: price/volume, fundamentals, crypto, futures, macro,
options). The surviving edges are the six component strategies above.

If a new session is started, the only valid action is **conformance
re-verification**:
1. `SEED=42 bash scripts/check.sh` — confirm baseline still clean.
2. Report closure.
3. Update this handoff with an accurate HEAD and timestamp when asked.

No commit should be made unless explicitly requested.