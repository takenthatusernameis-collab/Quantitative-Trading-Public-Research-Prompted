# DURABLE HANDOFF — Next Agentic Session

**Timestamp (UTC):** 2026-11-01T23:55:31Z
**Repo:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Branch:** main (HEAD `a93684e chore(kilo): checkpoint agent session`)
**State:** Research phase complete (E001–E050). Canonical goldens in `experiments/`, ledger in `ledger/RESEARCH_LEDGER.md`. Baseline verified clean at this session's start: `SEED=42 bash scripts/check.sh` → EXIT 0, `=== All checks passed ===`. No live verification snapshot (`.verify_snapshot/` absent) — nothing to recover. Working tree clean except gitignored `__pycache__/*.pyc` noise. E049/E050 (tangency-QP optimizer determinism) closed via exact KKT enumeration fix in `src/portfolio_opt.py`.

## Initial task message for the next agentic work session

> **START HERE:** The baseline is verified clean and the E049/E050 tangency-QP open item is **closed**. Confirm the clean baseline is still clean (`SEED=42 bash scripts/check.sh` + `git status --short`), then take up the next task from the ledger — do **not** re-open the optimizer determinism item and do **not** re-pin goldens to silence drift.

1. `pip install -r requirements.txt` if the environment was reset (numpy, pandas, scipy, pyarrow, statsmodels, yfinance).
2. `SEED=42 bash scripts/check.sh` — expect EXIT 0 with `=== All checks passed ===`.
3. `git status --short` — confirm working tree clean (only `__pycache__/*.pyc` noise). Do NOT commit verification output. If a verification run was interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only`.
4. Only after steps 1–3 pass cleanly, read `ledger/RESEARCH_LEDGER.md` (and `ledger/PRIORITIZATION.md`) to identify the next task and proceed.
5. Run `python3 -m py_compile` on every touched file.

## The actual open work

The novelty search (E001–E039) is closed and every family is gated. The post-close-out experiments E040–E050 were all reliability / reproducibility / documentation work — no new strategy research was registered. There is **no pre-registered E051 strategy experiment** in the ledger. The last strategy-level "next task" note in the ledger body is E038 (macro-data feasibility screen), resolved: E039 ran extended macro momentum (REJECTED) and E040 recorded the repository close-out.

If a new strategy candidate is warranted, re-read first:
- `ledger/PRIORITIZATION.md` (v1.2.5 active; weighted ranking criteria, source priority order, v1.2.x data-extension constraints gating fundamental/accounting families).
- `ledger/RESEARCH_LEDGER.md` E040 close-out table (REJECTED vs DATA-INFEASIBLE families) so the next pick is genuinely untested.
- The AGENTS.md data-coverage invariant: any new `data.download()` call site requires committing the cache file and re-pinning `ledger/data_baseline.json` via `python3 scripts/check_data_coverage.py --update`.

Pre-register any new candidate (gates, falsification expectations, sensitivity grid) in the driver docstring and the ledger *before* running.

## Constraints

- Never commit verification output; restore goldens first if interrupted (`SEED=42 python3 run_all_verification.py --restore-only`).
- Never re-pin goldens to silence drift — only via `python3 scripts/check_golden_baseline.py --update` with ledger justification.
- Run `python3 -m py_compile` on changed files.
- Always use `SEED=42`. Verification runs with `QUANT_RESEARCH_OFFLINE=1`.
- Honor pinned cache vintages (`data/vintages.json`, fundamentals pins in `data/fundamentals/`).
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or validated constructions.
- CI workflow creation is maintainer-gated (template at `.github/workflow-templates/verification-gate.yml`).
- Follow repo conventions in `AGENTS.md`.

## Quick references

- `make check` | `make verify-quick` | `make verify-extended` | `make verify-full`
- Ledger: `ledger/RESEARCH_LEDGER.md` (E040 close-out, E049/E050 entries)
- `ledger/PRIORITIZATION.md` — ranking procedure for the next candidate
- AGENTS.md — full commands & conventions
- Latest durable initial task: `.kilo/handoff/20261101T235531Z_INITIAL_TASK.md`