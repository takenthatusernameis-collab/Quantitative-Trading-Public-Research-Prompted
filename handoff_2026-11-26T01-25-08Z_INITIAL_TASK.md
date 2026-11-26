# Handoff — Next Agentic Work Session

**Timestamp:** 2026-11-26T01:25:08Z
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**HEAD:** 33c87609fbd5d961bb6d438958e1bcf7ad4d3e57 (`main`, in sync with `origin/main`, `0 0`)

## Read this first — the handoff-refresh loop

This repository is in a **runaway handoff-refresh loop** (ledger E652–E742+). ~94% of
git-tracked files are handoff artifacts (8,800+), plus ~120 root generic-alias symlinks.
Refreshing the handoff is *not* real work. **Do NOT manufacture an E743-style refresh as a
substitute for the tasks below.** If you catch yourself writing another timestamped handoff
file, stop: that is the loop, not progress.

Research phase is **complete (E001–E043)**; surviving strategies are in
`ledger/RESEARCH_LEDGER.md`. There is no open research to advance without new user direction.

## Prioritized real-work task list (do these instead of refreshing)

1. **Verify and stop.** Run `SEED=42 bash scripts/check.sh` (fast, offline). If green,
   report PASS and stop. Do not commit verification output.
2. **Reproduce (only if deps available).** `pip install -r requirements.txt`, then
   `SEED=42 python3 run_all_verification.py --extended`. Report drift *precisely*
   (per-driver numeric vs structural). **Do NOT re-pin goldens** to silence drift.
3. **Confirm E049/E050 tangency-QP drift stays closed** without re-pinning
   (E041/E042 bit-reproducible under the exact active-set enumeration).
4. **Propose (do NOT execute) a cleanup**: a `.gitignore` entry for handoff artifacts +
   `git rm --cached` of the 8,800+ tracked handoff files and alias symlinks. Present the
   plan to the user; deletion of tracked files requires explicit approval.

## Environment state this session

- `git status` clean apart from tracked `src/__pycache__/cache_keys.cpython-312.pyc` build noise.
- **Dependencies NOT importable** (`import numpy` -> `ModuleNotFoundError`).
  `pip install -r requirements.txt` is required before any verification run.
- `.verify_snapshot/` and `.verify_reports/` absent (no interrupted run to recover).

## Critical integrity notes

1. **Never leave verification half-finished** — it overwrites `experiments/*.json` and
   restores after. If interrupted: `SEED=42 python3 run_all_verification.py --restore-only`
   (or `git checkout <last-good-commit> -- experiments/`).
2. **Golden baseline is pinned** in `ledger/golden_baseline.json` (SHA-256). Never re-pin as
   a side effect of verification.
3. **Data coverage is enforced** — `scripts/check_data_coverage.py` requires every cache file
   to exist, be tracked, and match `ledger/data_baseline.json`.
4. **Optimizer determinism** — SLSQP status 8 is valid at a constrained optimum; gating on it
   caused environment-dependent E042 (fixed by E050 exact active-set enumeration).
5. **CI gate cannot be created by agents** — template at
   `.github/workflow-templates/verification-gate.yml`; a maintainer must create the workflow.

## Default action

Await explicit user instructions. If acting autonomously, do task 1 (verify-and-stop) and
report; do not extend into a handoff refresh or new research.