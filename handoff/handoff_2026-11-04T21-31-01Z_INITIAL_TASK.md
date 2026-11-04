# INITIAL TASK - Handoff for Next Agent Session

**Timestamp (UTC): 2026-11-04T21-31-01Z**
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** main — 21c267aaf791197fea0c8ab9a4c87d350648accc (2026-11-04 21:30:42 +0000) "chore(kilo): checkpoint agent session"
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Working Tree:** clean. `git status --short` empty; 138 goldens under `experiments/` match HEAD; `.verify_snapshot/` absent → no interrupted verification run.

## Session Summary

- Responded to user request: *Leave a timestamped clear initial task message for the next agentic work session in a durable handoff.*
- Verified live repo state before writing: `date -u`, `git log -1`, `git status --short`, golden counts.
- Did not run verification, modify experiments, or change baselines.

## Initial Task

**CLEAR INITIAL TASK:** *Leave a timestamped clear initial task message for the next agentic work session in a durable handoff.*

The next agentic work session must create its own timestamped durable handoff following the established pattern (`handoff/handoff_YYYY-MM-DDTHH-MM-SSZ_INITIAL_TASK.md` under `handoff/`, mirrored at repo root and `.kilo/handoff/`, repointing all root + `.kilo/handoff/` + `handoff/` symlinks) that leaves a clear initial task message for the session after it, with explicit guardrails and current state.

**Action required:** Wait for explicit user instructions before any research action. Do not re-run verification, modify experiments, or change baselines without explicit direction. Baseline is clean and recoverable. Do not invent new tasks, re-run verification "just to be sure", create additional handoffs unprompted, or re-open closed items (E049/E050 optimizer determinism; E041/E042 ill-conditioned QP drift; E057 CI gate — the only remaining human step is copying `.github/workflow-templates/verification-gate.yml` into `.github/workflows/` via the GitHub UI).

## First Steps (verify state)

- `git log -1 --format="%H"` and `git status --short` — confirm HEAD clean and canonical artifacts unmodified.
- Confirm no `.verify_snapshot/` directory exists.
- Read `ledger/RESEARCH_LEDGER.md` for surviving validated strategies and open items (E001–E083; repository closed).
- Quick check: `SEED=42 bash scripts/check.sh` (or `make check`) before any change.

## Key Constraints (from AGENTS.md)

- `experiments/*.json` are committed goldens — verification backs them up and restores them; never commit verification output or leave a run half-finished.
- Golden baseline enforced by `scripts/check_golden_baseline.py` vs `ledger/golden_baseline.json`; data coverage by `scripts/check_data_coverage.py` vs `ledger/data_baseline.json`.
- Optimizer: validate on problem constraints, not solver exit status (see `tests/test_portfolio_opt.py`, ledger E049/E050).
- Always use `SEED=42`. Close-to-close is the v1.2.3 primary convention.
- CI workflow cannot be created by automated agents. Use local `make check/verify/*`.
- Never re-pin artifacts to silence drift unless following the re-pinning process; the committed golden is the authoritative record.

## Handoff provenance

- Created: 2026-11-04T21-31-01Z
- Supersedes: `handoff_2026-11-04T21-26-32Z_INITIAL_TASK.md` (HEAD `32771be` → now `21c267a`).
- Durable locations: `handoff/handoff_2026-11-04T21-31-01Z_INITIAL_TASK.md`, mirrored at repo root and `.kilo/handoff/`. All symlinks repointed to this artifact and verified to resolve.

Handoff written by agent at 2026-11-04T21-31-01Z.
