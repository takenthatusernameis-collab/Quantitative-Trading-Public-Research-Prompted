# INITIAL TASK — Handoff for Next Agent Session

**Timestamp (UTC): 2026-11-27T15:35:52Z**
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** main — 5fd5c69b64990384c25e1ee735953c217977de16 (2026-11-27 15:35:45 +0000) == origin/main
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Working Tree:** clean for `experiments/`, `data/`, `ledger/`; no `.verify_snapshot/` present (no interrupted run to recover).

## CLEAR INITIAL TASK

The research phase is complete (E001–E043); surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

The next agentic work session must:

1. Confirm canonical state: `git log -1 --format="%H"`, `git status --short experiments/ data/ ledger/`, confirm HEAD == origin/main (`5fd5c69b...`), confirm no `.verify_snapshot/`.
2. Run `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py` to confirm goldens match the pinned baseline (`ledger/golden_baseline.json`).
3. Run `SEED=42 bash scripts/check.sh` (or `make check`) to confirm goldens + data coverage + JSON guards are green — only if the user directs it.
4. If this session itself hands off, create its own timestamped durable handoff following the established pattern (`handoff_YYYY-MM-DDTHH-MM-SSZ_INITIAL_TASK.md` at repo root).

Do **not** re-run the full verification suite, modify `experiments/`, change baselines, re-pin artifacts, or re-open closed items (E049/E050 optimizer determinism; E041/E042 QP drift — all closed, artifacts reproduce with 0 diffs) without explicit user direction. Do **not** invent new tasks or create additional handoffs unprompted.

## Quick Start

```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 run_all_verification.py --restore-only   # only if an interrupted run is present
git log -1 --format="%H"
git status --short experiments/ data/ ledger/
```

## Handoff provenance

Supersedes prior INITIAL_TASK handoffs. This file is the authoritative initial-task message for the next session.

Handoff written by agent at 2026-11-27T15:35:52Z.
