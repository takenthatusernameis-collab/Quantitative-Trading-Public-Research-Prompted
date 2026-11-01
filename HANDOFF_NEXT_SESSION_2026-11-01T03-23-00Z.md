# Handoff (timestamp: 2026-11-01T03:23:00Z)

## Status
- Repo: Quantitative-Trading-Public-Research-Prompted
- Branch/HEAD: c9e34ca
- Working tree: clean (only __pycache__ artifacts; no source changes)

## Project state (from AGENTS.md)
- Research phase complete (E001–E043). Surviving validated strategies in ledger/RESEARCH_LEDGER.md.
- Golden artifacts: experiments/*.json are canonical. Verification backs up/restores (.verify_snapshot/); never leave verification half-finished.
- Pre-registration, multiple-testing discipline, negative results recorded honestly.
- Offline reproducibility enforced for verification (QUANT_RESEARCH_OFFLINE=1) and data coverage pinned (ledger/data_baseline.json).

## Immediate priorities for next agent
1. **Verify baseline integrity before any changes**
   - Run `SEED=42 bash scripts/check.sh` (fast: convention-robustness + template validation).
   - If goldens differ from HEAD or snapshot stale -> `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`.
   - Ensure `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py` pass.

2. **Understand current ledger/open items**
   - Read `ledger/RESEARCH_LEDGER.md` for open items (notably E049/optimizer determinism, extended-drift notes).
   - Note: E041/E042 grid artifacts may still drift numerically due to ill-conditioned QP (do not re-pin to silence).

3. **Only proceed with explicitly requested work**
   - Follow AGENTS.md: do not commit verification output; do not re-pin goldens as side effect of verification.
   - Use SEED=42 for reproducibility.
   - Respect pre-registration and promotion gates.

## Quick commands
```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 run_all_verification.py --skip-slow  # convention only fast path
SEED=42 python3 verify_convention_robustness.py
```

## Notes
- CI workflow cannot be created by agents (controller restores .github/workflows/); template at .github/workflow-templates/verification-gate.yml.
- Data: cached parquet in data/ (gitignored except pinned vintages). Fundamentals pinned for E029.
- This is an initial-task handoff; no prior task work performed in this session.
