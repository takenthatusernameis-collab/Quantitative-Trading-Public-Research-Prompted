# Agentic Work Session Handoff

**Timestamp (UTC)**: 2026-11-17T06:17:28Z
**Handoff ID**: E434 (durable handoff refresh)
**Project**: Quantitative-Trading-Public-Research-Prompted
**Workspace**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Live Git State (captured at handoff time)
- `HEAD`: `b5f2fb3f89fca240854429ef6cb16b068dad27f3` (`chore(kilo): checkpoint agent session`)
- `origin/main`: `b5f2fb3f89fca240854429ef6cb16b068dad27f3`
- Branch/sync: `main...origin/main`, `0 0` (in sync)
- `git status --short --branch`: `## main...origin/main` (clean at capture; this handoff creates new uncommitted artifacts)
- No `.verify_snapshot/` or `.verify_reports/` present (no interrupted verification run)

## Delta vs Prior Durable Handoff
- Prior: `handoff_2026-11-17T04:16:01Z_INITIAL_TASK.md` (HEAD `eabb6b67`, E433)
- Commits since prior: `b5f2fb3f` — checkpoint/handoff bookkeeping only
- Changed paths: handoff artifacts/symlinks under root, `.handoff/`, `.kilo/`, `handoff/`, `HANDOFFS/`, and `ledger/RESEARCH_LEDGER.md`
- **No changes to** `experiments/`, `data/`, `src/`, `scripts/`, `tests/`, or `research_state/` (data/code/test state unchanged)
- Prior state adopted: **E001–E051 research complete**; durable-handoff refreshes through E433. Repository remains in closed/research-complete state.

## Project Status
- Research phase complete (E001–E043 core; through E051 including later items as recorded in `ledger/RESEARCH_LEDGER.md`). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- Golden artifacts in `experiments/*.json` are canonical. Do not re-pin as a side effect of verification.

## Open Items (carry-forward, do not "fix" by re-pinning)
- **E041 drift**: 133 numeric differences remain (1-ulp sensitivity of ill-conditioned QP). Extended still reports drift; **do not re-pin**.
- **E029**: offline-reproducible since 2026-10-20 (fundamentals pinned in `data/fundamentals/`).
- **E030**: reproduces with 0 differences since 2026-10-20 (16-ETF panel committed).
- **E042 tangency QP**: ill-conditioned; do not re-pin to silence drift.

## Verification / Reproduction (SEED=42)
```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh      # or: make check

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py            # or: make verify-quick

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended # or: make verify-extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full     # or: make verify-full

# Convention robustness only (reads JSONs, no writes)
SEED=42 python3 verify_convention_robustness.py    # or: make verify

# Recover golden artifacts after interrupted verification
SEED=42 python3 run_all_verification.py --restore-only
```

## Guardrails (must honor)
- `SEED=42` for all reproducibility/verification runs.
- **Never leave verification half-finished**; if interrupted, recover with `--restore-only` (or `git checkout -- experiments/` only when HEAD is the intended baseline).
- Do **not** change gates, pre-registration, falsification expectations, sensitivity grids, or validated constructions.
- Do **not** re-pin golden baselines (`ledger/golden_baseline.json` / `experiments/*.json`) as a side effect of running verification.
- Do **not** commit verification output or `__pycache__`.
- Commit only if explicitly directed by the user.

## Clear Initial Task for Next Agentic Work Session
**Refresh the durable handoff for the next agentic work session.**
1. Capture live state: `date -u`, `git rev-parse HEAD`, `git rev-parse origin/main`, `git rev-list --left-right --count origin/main...HEAD`, `git status --short --branch`; confirm no `.verify_snapshot/`/`.verify_reports/` interruption.
2. Delta working tree/HEAD against this handoff (`handoff_2026-11-17T06:17:28Z_INITIAL_TASK.md`, HEAD `b5f2fb3f`); explicitly note any changes to `experiments/`, `data/`, `src/`, `scripts/`, `tests/`, or `research_state/`.
3. Write a fresh timestamped `handoff_<ISO>Z_INITIAL_TASK.md` at repo root and mirror identically to `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/`.
4. Run `python3 scripts/repoint_handoff.py handoff_<ISO>Z_INITIAL_TASK.md` to repoint generic canonical pointers (expect 451 pointers, 0 bad in this layout unless structure changed).
5. Append/update ledger entry as appropriate for the handoff refresh; keep all guardrails intact.
6. Do **not** commit unless explicitly directed.