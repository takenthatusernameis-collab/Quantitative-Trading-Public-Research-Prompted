# Handoff for Next Agentic Work Session

**Timestamp:** 2026-10-30T11:29:17Z (UTC)
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Branch:** main
**Snapshot state:** `.verify_snapshot/` does NOT exist

This session created this durable handoff. No source changes were made and no verification run was executed.

## INITIAL TASK (START HERE)

**PRIORITY 1 - Baseline integrity:** Run `SEED=42 bash scripts/check.sh` and confirm repo is clean. All checks must pass before proceeding.

**PRIORITY 2 - E049 follow-up (if checks pass):** Investigate and fix tangency QP ill-conditioning causing E041/E042 grid artifacts to drift. Goal: make E041/E042 reproduce within tolerance WITHOUT reintroducing solver-status dependence (preserve "judge answer on problem constraints, not solver status" invariant). Do NOT re-pin goldens to silence drift without ledger justification.

## Constraints

- Always use `SEED=42`. Use `QUANT_RESEARCH_OFFLINE=1` for verification.
- Never leave `run_all_verification.py` half-finished; recover with `--restore-only`.
- Do not re-pin goldens/baselines to silence drift without ledger justification.
- Do not commit verification outputs; only intentional source/data changes.
- Follow `AGENTS.md`; preserve "judge answer on problem constraints, not solver status" invariant.
