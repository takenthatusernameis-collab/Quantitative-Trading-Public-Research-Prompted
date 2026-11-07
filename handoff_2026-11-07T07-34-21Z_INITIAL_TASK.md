# INITIAL TASK — Handoff for Next Agent Session

**Timestamp (UTC): 2026-11-07T07:34-21Z**
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** main — `1eb1d389c9605ab65491432cdc37a1ce08d87edd` (chore(kilo): checkpoint agent session)
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Working Tree:** clean for canonical artifacts (`experiments/`, `data/`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`). No live verification run; `.verify_snapshot/` absent.

## Session Summary

- Responded to user request: *"Leave a timestamped clear initial task message for the next agentic work session in a durable handoff !"*
- Verified repository state before writing: HEAD `1eb1d389`, canonical artifacts clean, no pending `.verify_snapshot/`.
- Created this durable handoff and updated symlink pointers so the next session can locate the authoritative initial task.
- Did **not** run verification, modify experiments, change baselines, or take any research action. No explicit user direction beyond the handoff request.

## Initial Task (for next session)

**CLEAR INITIAL TASK:** Await explicit user instructions, then execute the requested work with full adherence to this repository’s reproducibility and baseline-integrity guardrails.

**Default posture (until directed otherwise):**
1. Do not start new experiments, re-run verification “just to be sure,” modify `experiments/*.json` goldens, or re-pin baselines.
2. Do not re-open closed items: **E049/E050** (optimizer determinism + exact KKT enumeration, closed — artifacts reproduce 0 diffs) and **E041/E042** ill-conditioned QP drift context as documented in `AGENTS.md`/ledger (do not re-pin to silence drift).
3. Treat committed goldens and pinned baselines as authoritative: `ledger/golden_baseline.json`, `ledger/data_baseline.json`, `ledger/RESEARCH_LEDGER.md`.

**If the user requests work:**
- First verify state: `git log -1 --format="%H %s"` and `git status --short experiments/ data/`; confirm no `.verify_snapshot/`.
- Run `SEED=42 bash scripts/check.sh` (or `make check`) before substantive changes when appropriate.
- Follow pre-registration, falsification, and multiple-testing discipline (`AGENTS.md`). Use `SEED=42`. Close-to-close is the v1.2.3 primary convention.
- If a verification run is interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/` only when safe per `AGENTS.md` guidance) before committing.

## Quick orientation

- Research phase complete (E001–E043). Surviving validated strategies: `ledger/RESEARCH_LEDGER.md`.
- Commands: `make check`, `make verify-quick`, `make verify-extended`, `make verify-full` (see `AGENTS.md`).
- CI workflow cannot be created by automated agents; use local gates.

## Handoff provenance

- **Supersedes:** `handoff_2026-11-07T07-32-10Z_INITIAL_TASK.md` (and all prior `*_INITIAL_TASK.md` handoffs).
- **Durable copies:** `handoff/handoff_2026-11-07T07-34-21Z_INITIAL_TASK.md`, root `handoff_2026-11-07T07-34-21Z_INITIAL_TASK.md`, `.kilo/handoff/handoff_2026-11-07T07-34-21Z_INITIAL_TASK.md`.
- **Symlinks updated (root):** `INITIAL_TASK.md` → this handoff. (`HANDOFF.md` left as-is unless project convention requires repointing; verify if needed.)

Handoff written by agent at 2026-11-07T07:34:21Z.
