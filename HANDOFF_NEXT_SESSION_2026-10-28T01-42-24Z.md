# Handoff: Next Agent Session

**Created:** $(date -u +%Y-%m-%dT%H:%M:%SZ)
**Branch:** $(git branch --show-current)
**HEAD:** $(git log -1 --oneline)

## Current State

Research phase is complete (E001–E043). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`. All experiments pre-registered with falsification expectations and promotion gates.

**Recent activity (last 5 commits):**
$(git log --oneline -5)

## Verification & Integrity Status

- **Goldens:** `experiments/*.json` are canonical. Never leave verification run half-finished - use `--restore-only` if interrupted.
- **Quick check:** `SEED=42 bash scripts/check.sh` or `make check` (~seconds, offline)
- **Quick verification:** `SEED=42 python3 run_all_verification.py` (~8 min)
- **Extended:** `SEED=42 python3 run_all_verification.py --extended` (~21 min)
- **Full:** `SEED=42 python3 run_all_verification.py --full` (~15 min)
- **Baseline guards:** `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py` run in check/verify. If golden mismatch reported, fix before committing.
- **Data coverage:** `scripts/check_data_coverage.py` enforces pinned caches (offline mode in verification).

## Known Constraints

- **Seed:** Always use `SEED=42`
- **Do not commit verification output** - restore goldens if interrupted
- **Optimizer determinism (E049):** SLSQP status 8 handled correctly (validate on constraints not solver status). Ill-conditioned QP still causes small numeric drift in E041/E042 grids (tolerated in comparison).
- **Data:** Fundamentals pinned for E029; 16-ETF panel pinned for E030. All drivers run offline in verification.
- **CI:** No workflows created by agents (controller restores .github/workflows/). Template at `.github/workflow-templates/verification-gate.yml`.

## Immediate Task for Next Session

**[LEAVE CLEAR INITIAL TASK]**

The user says: "Leave a timestamped clear initial task message for the next agentic work session in a durable handoff !"

**Recommended starting action:**
1. Run `SEED=42 bash scripts/check.sh` to verify baseline integrity is clean (goldens match HEAD, baseline pinned correctly, py_compile passes)
2. If clean, assess next work based on `ledger/RESEARCH_LEDGER.md` - research phase complete, focus may be on documentation/maintenance, or addressing any open items
3. If issues found, restore from baseline before proceeding

**Key files to review:**
- `ledger/RESEARCH_LEDGER.md` - current state of all experiments
- `AGENTS.md` - full project conventions
- `run_all_verification.py` - verification orchestration

## Environment
- Platform: linux
- Git repo: yes
- Today's date: $(date -u +%Y-%m-%d)
