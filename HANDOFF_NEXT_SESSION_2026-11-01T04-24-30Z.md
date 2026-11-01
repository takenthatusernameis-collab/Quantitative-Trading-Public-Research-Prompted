# Handoff (timestamp: 2026-11-01T04:24:30Z)

## Status
- Repo: Quantitative-Trading-Public-Research-Prompted
- Branch/HEAD: a7586db
- Working tree: clean except __pycache__ artifacts (ignored noise)

## Initial task for next agentic session
No specific code task assigned. Session opens fresh. First action: verify baseline integrity.

## Immediate priorities for next agent
1. **Verify baseline integrity before any changes**
   - Run `SEED=42 bash scripts/check.sh`.
   - If goldens differ from HEAD or snapshot stale -> `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`.
   - Ensure `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py` pass.
2. **Understand current ledger/open items**
   - Read `ledger/RESEARCH_LEDGER.md` (E049 optimizer determinism, extended-drift notes).
   - E041/E042 grid artifacts may still drift numerically due to ill-conditioned QP (do not re-pin to silence).
3. **Only proceed with explicitly requested work**
   - Follow AGENTS.md: do not commit verification output; do not re-pin goldens as side effect of verification.
   - Use SEED=42 for reproducibility.

## Quick commands
```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 verify_convention_robustness.py
```

## Notes
- CI workflow cannot be created by agents; template at .github/workflow-templates/verification-gate.yml.
- Data: cached parquet in data/ (gitignored except pinned vintages). Fundamentals pinned for E029.
