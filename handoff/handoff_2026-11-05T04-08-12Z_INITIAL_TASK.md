# INITIAL TASK - Handoff for Next Agent Session

**Timestamp (UTC): 2026-11-05T04:08:12Z**
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** main — 8ed2fd187b11a48df944026c48dc157354e41c93 "chore(kilo): checkpoint agent session"
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Session Summary

- Responded to user request: *Leave a timestamped clear initial task message for the next agentic work session in a durable handoff.*
- Verified live repo state before writing: `date -u` (2026-11-05T04:08:12Z), `git log -1` (8ed2fd18), `git status --short` (empty).
- Did not run verification, modify experiments, change baselines, or take any research action. No explicit user direction beyond the handoff request.

## Initial Task

**CLEAR INITIAL TASK:** Wait for explicit user instructions before taking any action. Do not assume or infer additional tasks.

The next agentic work session must wait for explicit user instructions before any research action. Do not re-run verification, modify experiments, or change baselines without explicit direction. Baseline is clean and recoverable. Do not invent new tasks, re-run verification "just to be sure", create additional handoffs unprompted, or re-open closed items (E049/E050 optimizer determinism + exact KKT enumeration; E041/E042 ill-conditioned QP drift — all closed; E057 CI gate — the only remaining human step is copying `.github/workflow-templates/verification-gate.yml` into `.github/workflows/` via the GitHub UI).

## First Steps (verify state)

```bash
git status --short && git rev-parse HEAD origin/main
ls -la .verify_snapshot/ 2>&1 | head
SEED=42 bash scripts/check.sh
```

## Verification Commands (if explicitly asked to reproduce)

```bash
SEED=42 python3 run_all_verification.py            # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended # (~21 min)
SEED=42 python3 run_all_verification.py --full     # (~15 min)
SEED=42 python3 run_all_verification.py --restore-only
SEED=42 python3 verify_convention_robustness.py
```

## Key Constraints (from AGENTS.md)

- `experiments/*.json` are committed goldens — verification backs them up and restores them; never commit verification output or leave a run half-finished.
- Golden baseline enforced by `scripts/check_golden_baseline.py` vs `ledger/golden_baseline.json`; data coverage by `scripts/check_data_coverage.py` vs `ledger/data_baseline.json`.
- Optimizer: validate on problem constraints, not solver exit status (see `tests/test_portfolio_opt.py`, ledger E049/E050).
- Always use `SEED=42`. Close-to-close is the v1.2.3 primary convention.
- CI workflow cannot be created by automated agents. Use local `make check/verify/*`.
- Never re-pin artifacts to silence drift unless following the re-pinning process; the committed golden is the authoritative record.

## Handoff provenance

- Created: 2026-11-05T04:08:12Z
- HEAD: 8ed2fd187b11a48df944026c48dc157354e41c93
- Supersedes: handoff/handoff_2026-11-05T04-07-54Z_INITIAL_TASK.md
- Durable locations: `handoff/handoff_2026-11-05T04-08-12Z_INITIAL_TASK.md`, mirrored at repo root via repointed symlinks.

(End of file)
