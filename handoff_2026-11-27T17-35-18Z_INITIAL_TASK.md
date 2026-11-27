# Durable Handoff — Initial Task for Next Agentic Work Session

**Timestamp**: 2026-11-27T17-35-18Z
**Project**: Quantitative-Trading-Public-Research-Prompted
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Durable artifact**: `handoff_2026-11-27T17-35-18Z_INITIAL_TASK.md` (repo root)
**Supersedes**: `handoff_2026-11-27T17-34-07Z_INITIAL_TASK.md`

## Initial Task (for the next agentic work session)

The research phase is **closed** (E001–E043). There is no new research to invent. Do not manufacture a handoff refresh as a substitute for real work.

The next agentic work session must:

1. **Confirm canonical state** before any change:
   - `git log -1 --format="%H"` → expect `623ad3f7`
   - `git status --short experiments/ data/ ledger/` → expect empty
   - Confirm HEAD == `origin/main` (`623ad3f7`)
   - Confirm no `.verify_snapshot/` directory exists (no interrupted run to recover).
2. **Read `ledger/RESEARCH_LEDGER.md`** for surviving validated strategies and open items.
3. **Only if directed** by the user, run `SEED=42 bash scripts/check.sh` (or `make check`) to confirm goldens + data coverage + JSON guards are green.
4. **Do NOT** re-run verification, modify experiments, change baselines, re-pin artifacts, or commit without explicit user direction.
5. **If the session hands off**, create its own timestamped durable handoff at repo root (`handoff_YYYY-MM-DDTHH-MM-SSZ_INITIAL_TASK.md`) and update these pointers.

## Baseline Integrity Verification (2026-11-27T17-35-18Z)

- ✅ No active verification run: `.verify_snapshot/` absent.
- ✅ Git tree clean: `git status --short experiments/ data/ ledger/` empty. Branch `main`; HEAD `623ad3f7` == `origin/main`.
- ✅ Canonical artifacts unmodified: `experiments/`, `data/`, `ledger/` match HEAD.
- ⚠️ Untracked/generated: `src/__pycache__/cache_keys.cpython-312.pyc` modified (not canonical; safe to ignore).

## Project Status

Research phase complete (E001–E043). Surviving validated strategies are documented in
`ledger/RESEARCH_LEDGER.md`. Golden artifacts in `experiments/*.json` are the authoritative
record; never re-pin or overwrite them as a side effect of running verification.

## Quick Start Commands

```bash
SEED=42 bash scripts/check.sh                          # fast convention + template validation (offline)
SEED=42 python3 run_all_verification.py                # quick full verification (~8 min)
SEED=42 python3 run_all_verification.py --extended     # +18 drivers, structural match (~21 min)
SEED=42 python3 run_all_verification.py --restore-only # recover goldens if interrupted
```

## Key Artifacts

- **Golden files**: `experiments/*.json`
- **Ledger**: `ledger/RESEARCH_LEDGER.md` (E001–E043)
- **Pinned baselines**: `ledger/golden_baseline.json`, `ledger/data_baseline.json`

## Handoff Context

Created at the user's explicit request to leave a timestamped, clear initial task message for the
next agentic work session. Baseline re-verified clean at this timestamp; no snapshot recovery
needed; no code changes made. Left uncommitted pending explicit direction.

**Warning — runaway handoff loop:** this repository carries thousands of git-tracked files,
the vast majority of which are `handoff`-prefixed artifacts produced by repeated refresh loops.
Do NOT add to that by manufacturing another refresh as a substitute for the real work above.
This handoff is the deliverable.

(End of file)
