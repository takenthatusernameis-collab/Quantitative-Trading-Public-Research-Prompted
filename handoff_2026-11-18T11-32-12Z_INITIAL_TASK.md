# Agentic Work Session Handoff

**Timestamp:** 2026-11-18T11:32:12Z
**Session type:** Durable initial task message for the next agentic work session
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Initial Task

Leave a timestamped clear initial task message for the next agentic work session in a durable handoff. This file is that durable handoff: it is the first thing the next agentic session should read. It records the current project state, the standing rules, and the concrete first actions to take.

## Project Context

Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. The research phase is complete (E001–E043). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`; open items and dispositions are in `ledger/PRIORITIZATION.md`.

## First Actions for the Next Session

1. Read this handoff, then `AGENTS.md` (baseline-integrity rules are mandatory).
2. Sanity-check the working tree: `git status` — confirm no half-finished verification run left driver output in `experiments/`.
3. Run the fast, offline check: `SEED=42 bash scripts/check.sh`.
4. Skim `ledger/RESEARCH_LEDGER.md` and `ledger/PRIORITIZATION.md` for current strategy dispositions and open items before starting any new work.

## Key Verification Commands

```bash
SEED=42 bash scripts/check.sh                              # Fast convention-robustness check (seconds, offline)
SEED=42 python3 run_all_verification.py                    # Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py --extended         # Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --full             # Full verification (~15 min)
SEED=42 python3 run_all_verification.py --restore-only     # Recover golden artifacts after an interrupted run
```

## Critical Rules (from AGENTS.md — do not violate)

- **Golden artifacts:** `experiments/*.json` are the canonical research record. The verification suite overwrites them during a re-run and restores them afterward; a run must never be left half-finished.
- **Never commit verification output.** A checkpoint commit that captures a re-run silently replaces the canonical baseline (this has happened and been reverted multiple times).
- **Baseline guards:** `scripts/check_goldens_clean.py` (working tree vs HEAD) and `scripts/check_golden_baseline.py` (working tree vs SHA-256 in `ledger/golden_baseline.json`) are first-class `scripts/check.sh` steps. If a golden mismatches, fix it before committing; never re-pin to silence drift.
- **Reproducibility:** always use `SEED=42`. Cache coverage is an enforced invariant — every `data.download()` input must be committed and pinned in `ledger/data_baseline.json`. Drivers run with `QUANT_RESEARCH_OFFLINE=1`.
- **Optimizer determinism:** `src/portfolio_opt.py` validates a solver answer on the problem's constraints, not on the solver's exit status. The tangency QP remains ill-conditioned; do not re-pin E041/E042 artifacts to hide that.

## Known Drift (expected, do not "fix" by re-pinning)

- E011, E030: small numeric drift, within tolerance.
- E041: 133 numeric differences remain (1-ulp sensitivity of an ill-conditioned QP); its decision and gate flags are unchanged. Open item — see ledger.
- E042: grid artifacts drift for the same reason.
- E029: offline-reproducible since its fundamentals snapshot was pinned in `data/fundamentals/`.

## Current State

- Research phase complete (E001–E043); no experiment drivers running.
- Working tree clean at the time of writing (`git status` empty).
- This handoff is the durable initial task message; the `handoff_*`, `latest`, `next`, and `next_session` symlinks at repo root point to it.