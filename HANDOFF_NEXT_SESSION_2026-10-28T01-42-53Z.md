# Next Task Handoff (prepared 2026-10-28T01:42:53Z)

## Repository state

Research phase complete (E001–E046). The repository is clean and fully verified. Last session (E047) fixed a documentation contradiction in README.md regarding E041/E042 reproducibility. No code, golden, gate, or decision was changed.

## Current verified state

- `SEED=42 bash scripts/check.sh` passes (ALL CHECKS PASSED)
- Research documented in `ledger/RESEARCH_LEDGER.md` (E001–E047)
- Surviving validated strategies documented
- Golden baselines pinned and verified
- Crash-safety snapshot/restore mechanism in place

## What the next agent should do

**No required work.** The repository is in a clean, verified state.

If there is user-directed work, follow these priorities:

1. **If maintainer requests CI workflow creation** - Create `.github/workflows/verification-gate.yml` from template at `.github/workflow-templates/verification-gate.yml`. Note: agent cannot push to `.github/workflows/` due to controller policy; maintainer must create via GitHub UI per AGENTS.md.

2. **If investigating environment-sensitive drivers** - E030 and E041 show numeric drift between builds/environments (documented as reporting-only). Do NOT re-pin goldens to silence drift. See ledger E048, E049 for details. E041 has optimizer determinism issues (ill-conditioned QP), E030 had missing cache pinning (now fixed).

3. **If extending research** - Any new experiments must follow pre-registration discipline, multiple-testing gates, and golden baseline update process with justification via `scripts/check_golden_baseline.py --update`.

## Quick verification commands

```bash
# Fast check
SEED=42 bash scripts/check.sh

# Full verification
SEED=42 python3 run_all_verification.py

# Restore goldens if needed
SEED=42 python3 run_all_verification.py --restore-only
```

## Constraints

- Always use `SEED=42`
- Never modify committed goldens without deliberate re-pin with justification
- Run verification drivers in isolated copies if debugging reproducibility (they overwrite `experiments/*.json`)
- Follow all policies in AGENTS.md
- The golden baseline is authoritative
