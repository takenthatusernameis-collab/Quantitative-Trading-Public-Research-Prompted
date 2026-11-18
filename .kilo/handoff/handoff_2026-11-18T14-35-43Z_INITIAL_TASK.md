# Handoff — Initial Task for Next Agentic Work Session

**Created (UTC):** 2026-11-18T14-35-43Z
**Session type:** Durable handoff refresh (no new research performed)
**Repository:** `Quantitative-Trading-Public-Research-Prompted`

## Current HEAD / sync state
- Branch: `main` (tracking `origin/main`)
- `HEAD`: `9fc8925b` (full `9fc8925b1c0c2cc34aef6cda1da3e50edb550a59`)
- Working tree at handoff creation: clean (`git status --short` empty)
- No `.verify_snapshot/ACTIVE.json` present
- `git diff --name-only HEAD -- experiments/` → empty (goldens match HEAD)

## Project status (authoritative)
- Research phase **complete (E001–E051)**; dispositions documented in `ledger/RESEARCH_LEDGER.md`. Repository in closed, reproducibility-focused state.
- `experiments/*.json` canonical golden artifacts; `ledger/golden_baseline.json` pins SHA-256. Replacing requires explicit re-pinning — never as side effect of verification.
- Data inputs pinned per `ledger/data_baseline.json` and `data/vintages.json`; cache coverage enforced by `scripts/check_data_coverage.py`. Verification runs with `QUANT_RESEARCH_OFFLINE=1`.
- Known open technical note (ledger E049): E041/E042 grid artifacts exhibit 1-ulp QP sensitivity; do not re-pin to silence.

## Initial task for the next agentic work session
1. **Orient (read-only):** read `AGENTS.md`, tail of `ledger/RESEARCH_LEDGER.md`, and this handoff. Confirm `git status --short`, `git rev-parse --short HEAD`, branch/sync state, absence of `.verify_snapshot/ACTIVE.json`.
2. **Fast integrity gate (offline, ~seconds):** run `SEED=42 bash scripts/check.sh` (or `make check`). Resolve any golden/baseline/coverage issues before any commit.
3. **If deeper verification needed:** run `SEED=42 python3 run_all_verification.py` (quick/extended/full). Always finish or recover with `--restore-only`; do not commit verification output.
4. **Do not start new research or code changes unless explicitly requested and pre-registered.** Preserve multiple-testing discipline, negative-result recording, baseline integrity.

## Handoff provenance
- **Durable artifact (this file):** `handoff_2026-11-18T14-35-43Z_INITIAL_TASK.md` (repo root), mirrored byte-identically to `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/`.
- **Canonical pointers:** repointed with `python3 scripts/repoint_handoff.py handoff_2026-11-18T14-35-43Z_INITIAL_TASK.md`.
- Supersedes operationally: `handoff_2026-11-18T12-26-45Z_INITIAL_TASK.md` (retained for history).

_End of durable handoff. No new research requested; awaiting explicit user instructions._
