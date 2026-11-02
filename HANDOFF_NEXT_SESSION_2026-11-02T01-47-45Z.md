# DURABLE HANDOFF — Next Agentic Session

**Timestamp (UTC):** 2026-11-02T01-47-45Z
**Repo:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Branch:** main (HEAD `600fcbd`)
**State:** Research phase complete (E001–E050). Canonical goldens in `experiments/`, ledger in `ledger/RESEARCH_LEDGER.md`. Working tree clean at HEAD `600fcbd` (only gitignored `__pycache__/*.pyc` differ). No live verification snapshot (`.verify_snapshot/` absent) — nothing to recover. E049/E050 (tangency-QP optimizer determinism) closed via exact KKT enumeration fix in `src/portfolio_opt.py`.

## Initial task message for the next agentic work session

> **START HERE:** The baseline is verified clean. Confirm repository integrity, then identify and execute the next highest-priority item from the research ledger.

1. `pip install -r requirements.txt` if the environment was reset (numpy, pandas, scipy, pyarrow, statsmodels, yfinance).
2. `SEED=42 bash scripts/check.sh` — expect EXIT 0 with `=== All checks passed ===`.
3. `git status --short` — confirm working tree clean (only `__pycache__/*.pyc` noise). Do NOT commit verification output. If a verification run was interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only`.
4. Only after steps 1–3 pass cleanly, read `ledger/RESEARCH_LEDGER.md` to identify the next open task, pre-register any changes if extending research, and proceed methodically. Follow all constraints.

## Constraints

- Never commit verification output. Restore goldens first if interrupted (`SEED=42 python3 run_all_verification.py --restore-only`).
- Never re-pin goldens to silence drift.
- Run `python3 -m py_compile` on changed files.
- Always use `SEED=42`.
- Honor pinned cache vintages (`data/vintages.json`, fundamentals pins in `data/fundamentals/`).
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or validated constructions.
- CI workflow creation is maintainer-gated (template at `.github/workflow-templates/verification-gate.yml`).
- Follow repo conventions in `AGENTS.md`.

## Quick references

- `make check` | `make verify-quick` | `make verify-extended` | `make verify-full`
- Ledger: `ledger/RESEARCH_LEDGER.md`
- AGENTS.md — full commands & conventions
- Latest handoff: `HANDOFF_NEXT_SESSION_LATEST.md`

(End of handoff)
