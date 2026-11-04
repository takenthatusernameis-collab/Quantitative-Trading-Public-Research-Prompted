# INITIAL TASK - Handoff for Next Agent Session

**Timestamp (UTC): 2026-11-04T21-34-19Z**
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** main — 2668ac8315a6fd40d3f77cacab6028943817fc57 2026-11-04 21:34:02 +0000
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Working Tree:** clean. `git status --short` empty; `.verify_snapshot/` absent → no interrupted verification run.

## Session Summary

- Responded to user request: *"Leave a timestamped clear initial task message for the next agentic work session in a durable handoff."*
- Created this timestamped durable handoff following the established pattern.
- Did not run verification, modify experiments, or change baselines.

## Initial Task

**CLEAR INITIAL TASK:** *Leave a timestamped clear initial task message for the next agentic work session in a durable handoff.*

The next agentic work session must create its own timestamped durable handoff following the established pattern (`handoff/handoff_YYYY-MM-DDTHH-MM-SSZ_INITIAL_TASK.md` under `handoff/`, mirrored at repo root and `.kilo/handoff/`, repointing all root + `.kilo/handoff/` + `handoff/` symlinks) that leaves a clear initial task message for the session after it, with explicit guardrails and current state.

**Action required:** Wait for explicit user instructions before any research action. Do not re-run verification, modify experiments, or change baselines without explicit direction. Baseline is clean and recoverable. Do not invent new tasks, re-run verification "just to be sure", create additional handoffs unprompted, or re-open closed items (E049/E050 optimizer determinism; E041/E042 ill-conditioned QP drift; E057 CI gate — the only remaining human step is copying `.github/workflow-templates/verification-gate.yml` into `.github/workflows/` via the GitHub UI).

## First Steps (verify state)

- `git log -1 --format="%H"` and `git status --short` — confirm HEAD clean and canonical artifacts unmodified.
- Confirm no `.verify_snapshot/` directory exists.
- Read `ledger/RESEARCH_LEDGER.md` for surviving validated strategies and open items.
- Quick check: `SEED=42 bash scripts/check.sh` (or `make check`) before any change.

## Key Constraints (from AGENTS.md)

- `experiments/*.json` are committed goldens — verification backs them up and restores them; never commit verification output or leave a run half-finished.
- Golden baseline enforced by `scripts/check_golden_baseline.py` vs `ledger/golden_baseline.json`; data coverage by `scripts/check_data_coverage.py` vs `ledger/data_baseline.json`.
- Optimizer: validate on problem constraints, not solver exit status (see `tests/test_portfolio_opt.py`, ledger E049/E050).
- Always use `SEED=42`. Close-to-close is the v1.2.3 primary convention.
- CI workflow cannot be created by automated agents. Use local `make check/verify/*`.
- Never re-pin artifacts to silence drift unless following the re-pinning process; the committed golden is the authoritative record.

## Handoff provenance

Created by this session at 2026-11-04T21:34:19Z. Supersedes previous INITIAL_TASK handoffs.
" filePath="/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted/handoff/handoff_2026-11-04T21-34-19Z_INITIAL_TASK.md"