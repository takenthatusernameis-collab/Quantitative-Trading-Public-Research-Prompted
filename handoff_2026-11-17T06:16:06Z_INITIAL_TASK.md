# Agentic Work Session Handoff

**Timestamp (UTC)**: 2026-11-17T06:16:06Z
**Handoff ID**: E434 (durable handoff refresh)
**Project**: Quantitative-Trading-Public-Research-Prompted
**Workspace**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Live Git State (captured at handoff time)
- `HEAD`: `f34a72613c503f5bc9dd3cc7ec92b26ca60584a1` (`chore(kilo): checkpoint agent session`)
- `origin/main`: `f34a72613c503f5bc9dd3cc7ec92b26ca60584a1`
- Branch/sync: `main...origin/main`, `0 0` (in sync)
- `git status --short --branch`: `## main...origin/main` (clean at capture; this handoff creates new uncommitted artifacts)
- No `.verify_snapshot/` or `.verify_reports/` present (no interrupted verification run)

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
SEED=42 bash scripts/check.sh
SEED=42 python3 run_all_verification.py
SEED=42 python3 run_all_verification.py --extended
SEED=42 python3 run_all_verification.py --full
```

## Guardrails (must honor)
- `SEED=42` for all reproducibility/verification runs.
- Never leave verification half-finished; recover with `--restore-only`.
- Do not change gates, pre-registration, falsification expectations, sensitivity grids, or validated constructions.
- Do not re-pin golden baselines as a side effect of running verification.
- Do not commit verification output or `__pycache__`.
- Commit only if explicitly directed by the user.

## Clear Initial Task for Next Agentic Work Session
**Refresh the durable handoff for the next agentic work session.**
1. Capture live state: `date -u`, `git rev-parse HEAD`, `git rev-parse origin/main`, `git rev-list --left-right --count origin/main...HEAD`, `git status --short --branch`; confirm no `.verify_snapshot/`/`.verify_reports/` interruption.
2. Delta working tree/HEAD against this handoff (`handoff_2026-11-17T06:16:06Z_INITIAL_TASK.md`, HEAD `f34a7261`); explicitly note any changes to `experiments/`, `data/`, `src/`, `scripts/`, `tests/`, or `research_state/`.
3. Write a fresh timestamped `handoff_<ISO>Z_INITIAL_TASK.md` at repo root and mirror identically to `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/`.
4. Run `python3 scripts/repoint_handoff.py handoff_<ISO>Z_INITIAL_TASK.md` to repoint generic canonical pointers (expect 451 pointers, 0 bad in this layout unless structure changed).
5. Append/update ledger entry as appropriate for the handoff refresh; keep all guardrails intact.
6. Do not commit unless explicitly directed.
