# Agentic Handoff — Quantitative-Trading-Public-Research-Prompted

**Created:** 2026-11-05T03:37:35Z
**Workspace root:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Purpose:** Durable initial task message so the next agentic session can resume without re-discovery.

## Repository state (as of this message)

- This is an independent reproducible quantitative-strategy research repo (2014–2026 US equities, futures, macro).
- Research phase complete: experiments E001–E043. Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- Canonical research artifacts: `experiments/*.json` (must not be left half-finished by a verification run).
- No uncommitted changes are assumed at handoff time; verify with `git status` before acting.

## Recommended initial task for next session

Run the fast convention-robustness check + template validation to confirm the tree is green before starting any new work:

```bash
SEED=42 bash scripts/check.sh
# or
make check
```

If that passes, the next concrete coding task is still to be defined by the user — no feature/bug work was assigned in this session.

## Key commands (from AGENTS.md)

| Purpose | Command |
|---|---|
| Fast check (convention + template validation) | `SEED=42 bash scripts/check.sh` / `make check` |
| Quick full verification (~8 min) | `SEED=42 python3 run_all_verification.py` / `make verify-quick` |
| Extended verification | `SEED=42 python3 run_all_verification.py --extended` / `make verify-extended` |
| Full verification | `SEED=42 python3 run_all_verification.py --full` / `make verify-full` |
| Recover golden artifacts after interrupted run | `SEED=42 python3 run_all_verification.py --restore-only` |
| Individual driver | `SEED=42 python3 experiments/run_e0XX.py` |

## Important guardrails

- `experiments/*.json` are canonical; a verification run overwrites then restores them. Never commit verification output. If interrupted, run `--restore-only` before committing.
- Data coverage is enforced: `scripts/check_data_coverage.py` requires every `data.download()` cache file to exist, be git-tracked, and match `ledger/data_baseline.json`. Drivers run with `QUANT_RESEARCH_OFFLINE=1`.
- Lint/typecheck: run `python3 -m py_compile` on changed Python files (no separate linter configured).
- Seed for reproducibility: always `SEED=42`.

## Files of note

- `AGENTS.md` — project commands & conventions (authoritative).
- `ledger/RESEARCH_LEDGER.md` — documented surviving strategies & open items.
- `ledger/golden_baseline.json` — SHA-256 fingerprints of committed experiment artifacts.
- `ledger/data_baseline.json` — pinned data cache fingerprints.
- `scripts/check.sh`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`, `scripts/check_goldens_clean.py`.
- `run_all_verification.py`, `src/batch_run.py`, `src/validate.py`, `src/portfolio_opt.py`.
- `.verify_snapshot/` (gitignored) — backup during live verification runs; `ACTIVE.json` holds owning pid.

## Open items (from ledger / AGENTS.md)

- E041 optimizer determinism: 133 remaining numeric diffs (1-ulp QP sensitivity) still exceed 1e-4 tolerance; do not re-pin to silence. See ledger E049.
- CI verification gate `.github/workflows/verification-gate.yml` cannot be created by automated agents; template at `.github/workflow-templates/verification-gate.yml` (maintainer must create via GitHub UI).

## Next session entry point

Read `AGENTS.md`, run `SEED=42 bash scripts/check.sh`, then await the user's actual task. This handoff file is the durable starting point — update it if the session produces durable state changes.