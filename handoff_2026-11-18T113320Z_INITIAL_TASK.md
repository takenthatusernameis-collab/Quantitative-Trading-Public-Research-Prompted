# Agentic Work Session Handoff

**Timestamp:** 2026-11-18T11:33:20Z (UTC)
**Type:** Durable initial task message for the next agentic work session
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Initial Task (start here)

1. Read this handoff and `AGENTS.md` (baseline-integrity rules are mandatory).
2. Check state before touching anything:
   - `git status --short --branch`
   - `SEED=42 bash scripts/check.sh` (fast, offline; catches golden mismatches/snapshot issues)
3. Review current research dispositions/open items:
   - `ledger/RESEARCH_LEDGER.md`
   - `ledger/PRIORITIZATION.md`
4. If a verification run was interrupted or goldens look dirty, recover before committing:
   - `SEED=42 python3 run_all_verification.py --restore-only`
   - or `git checkout -- experiments/` (only if `HEAD` already matches the pinned golden baseline)

## Project Snapshot

- Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data.
- Research phase complete (E001–E043). Surviving validated strategies and dispositions are in `ledger/RESEARCH_LEDGER.md`.
- Pre-registration, falsification gates, and honest negative results are required. Do not move goalposts post-hoc.

## Key Commands

```bash
SEED=42 bash scripts/check.sh                              # Fast checks: goldens clean/pinned, templates, convention robustness
SEED=42 python3 run_all_verification.py                    # Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py --extended         # Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --full             # Full verification (~15 min)
SEED=42 python3 run_all_verification.py --restore-only     # Restore artifacts after interrupted run
```

## Critical Rules (do not violate)

- `experiments/*.json` are canonical golden artifacts. Verification overwrites during runs and restores afterward; never leave a run half-finished.
- **Never commit verification output.** Fix golden/baseline mismatches before committing.
- Baseline guards: `scripts/check_goldens_clean.py` (tree vs HEAD) and `scripts/check_golden_baseline.py` (tree vs `ledger/golden_baseline.json`). Do not re-pin to silence drift.
- Reproducibility: always `SEED=42`. Data/cache coverage is enforced (`ledger/data_baseline.json`, pinned vintages); drivers run with `QUANT_RESEARCH_OFFLINE=1`.
- Optimizer determinism: `src/portfolio_opt.py` validates solutions against problem constraints (not solver exit status). Tangency QP remains ill-conditioned.

## Known/Expected Drift (not to "fix" by re-pinning)

- E011/E030: small numeric drift within tolerance.
- E041: 133 numeric differences remain (1-ulp sensitivity, ill-conditioned QP); decision/gates unchanged. E042 grid artifacts drift similarly. Open ledger item — do not re-pin E041/E042 artifacts to hide this.
- E029 fundamentals pinned for offline reproducibility.

## Current Session Note

- Git HEAD at handoff creation: `663a4660 chore(kilo): checkpoint agent session`.
- This file is the durable, timestamped initial task message for the next agentic session. Canonical handoff pointers should be repointed to it.
