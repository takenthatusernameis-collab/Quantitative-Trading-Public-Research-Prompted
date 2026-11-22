# Durable Handoff — Next Agentic Work Session

**Created:** 2026-11-22T01:59:54Z
**Session:** Pre-handoff (no task assigned yet — awaiting user instructions)
**Live HEAD at creation:** `68f1a9e6` on `main` (== `origin/main`)

## Repository Context
- Path: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
- Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data.
- Research phase complete (E001–E043); surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- Canonical research artifacts live under `experiments/*.json` (committed goldens). Verification overwrites then restores them — never leave a verification run half-finished.
- Key conventions (AGENTS.md): `SEED=42`, offline mode (`QUANT_RESEARCH_OFFLINE=1`) for verification, pinned data/fundamentals caches in `data/`, pre-registered `pre_registered` blocks, goalposts never moved post-hoc.

## Commands
```bash
# Convention robustness only (~seconds, offline)
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py

# Individual experiment driver example
SEED=42 python3 experiments/run_e042.py --n-sim 50
```

## Lint / Typecheck
- No separate linter configured; run `python3 -m py_compile` on changed Python files.

## Initial Task for Next Session
No task has been assigned yet. On resumption:
1. Read this handoff file and `AGENTS.md` for conventions.
2. Await the user's specific task instructions before making changes.
3. Do not commit unless explicitly asked.
4. After code changes, run `python3 -m py_compile` on changed files.
5. If verifying, use `SEED=42` and offline mode, and never leave a verification run half-finished (restore goldens with `SEED=42 python3 run_all_verification.py --restore-only`).

## Safety / Constraints
- Never commit changes without an explicit user request.
- Never commit verification output (goldens under `experiments/`).
- Never re-pin golden/data baselines as a side effect of verification.
- Never guess/generate URLs unless confident they aid programming.
- Do not add comments to code unless asked.