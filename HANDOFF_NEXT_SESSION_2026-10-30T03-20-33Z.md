# Handoff for Next Agentic Work Session

**Timestamp:** 2026-10-30T03:20:33Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Branch:** main
**Working tree:** clean (no source changes this session).
**Created by:** Kilo

No specific task was provided this session. This durable handoff establishes the initial task for the next agentic work session: establish baseline integrity and wait for direction.

## Initial Task (Start Here)

**Task:** Verify repository stability before any new work, then await explicit instruction.

1. Run the fast integrity check: `SEED=42 bash scripts/check.sh` — all checks green.
2. Confirm tree state: `git status --short` — only `__pycache__/*.pyc` allowed.
3. If a previous verification run was interrupted, recover first: `SEED=42 python3 run_all_verification.py --restore-only`.
4. Do not make source changes or re-run experiment drivers unless explicitly requested.

## Context

- Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- Optimizer determinism fix (E049) is in place: `src/portfolio_opt.py` validates answers against problem constraints, not solver `success` status.
- Known open item: tangency QP ill-conditioning; E041 (~133 diffs) and E042 (~29 diffs) grid artifacts still drift vs goldens; deliberately not re-pinned.
- Symlinks `handoff.md`, `handoff_next.md`, `handoff_next_session.md` point to this file.

## Constraints (Do Not Violate)

- Always use `SEED=42`.
- Never leave `run_all_verification.py` half-finished.
- Do **not** re-pin goldens/`ledger/golden_baseline.json`/`ledger/data_baseline.json` to silence drift without ledger justification.
- Do **not** commit verification outputs; only intentional source/data changes.
- Follow `AGENTS.md`; honor "judge answer on problem constraints, not solver status" invariant.
- No goalpost moves; decisions unchanged unless evidence forces (pre-registered).

## Quick Commands

```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 run_all_verification.py        # quick (~8 min)
SEED=42 python3 run_all_verification.py --restore-only
git status --short
```

## Key Files

- `AGENTS.md` — verification commands, golden protection rules, cache/data invariants
- `ledger/RESEARCH_LEDGER.md` — validated strategies and open items
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints
- `scripts/check.sh`, `run_all_verification.py`, `check_goldens_clean.py`, `check_golden_baseline.py`

(End of file)
