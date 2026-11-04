# HANDOFF — Next Agentic Work Session

**Timestamp:** 2026-11-04T03:05:13Z
**Session:** `ses_e5b7b77bcffeoCR4ur6DN2pcxT` (main, code agent, busy)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

---

## Current Task

**Leave a timestamped clear initial task message for the next agentic work session in a durable handoff.**

Status: **IN PROGRESS** — this handoff file is the deliverable. No prior sub-task was running; the board (`board_read`) is empty and this is a fresh main session.

## Project Context

Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. Research phase is **complete (E001–E043)**; surviving validated strategies are in `ledger/RESEARCH_LEDGER.md`.

Key conventions (see `AGENTS.md`):
- **Seed:** always `SEED=42`.
- **Verification:** `SEED=42 python3 run_all_verification.py` (quick, ~8 min), `--extended` (~21 min), `--full` (~15 min). Equivalents: `make verify-quick`, `make verify-extended`, `make verify-full`.
- **Convention robustness only:** `SEED=42 python3 verify_convention_robustness.py` or `make verify`.
- **Fast check:** `SEED=42 bash scripts/check.sh` or `make check`.
- **Recovery after interrupted verification:** `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`).
- **Baseline integrity:** `experiments/*.json` are canonical goldens. Never commit verification output. The suite backs up to `.verify_snapshot/` (gitignored, `ACTIVE.json` marker holds owning pid) and restores afterward. `scripts/check_goldens_clean.py` fails on working-tree vs HEAD mismatch; `scripts/check_golden_baseline.py` compares against SHA-256 pinned in `ledger/golden_baseline.json`. Re-pin only with `python3 scripts/check_golden_baseline.py --update` — never as a side effect of verification.
- **Data coverage invariant:** `scripts/check_data_coverage.py` requires every `data.download()` call site's cache file to exist, be git-tracked, and match `ledger/data_baseline.json`. Verification runs with `QUANT_RESEARCH_OFFLINE=1`.
- **Known drift (do NOT re-pin):** E041 (133 numeric diffs, ill-conditioned QP 1-ulp sensitivity), E042 grid artifacts drift 29–133 diffs. E029/E030 reproduce with 0 diffs since 2026-10-20 (inputs pinned).
- **Dependencies:** `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance). cvxpy/cvxopt optional; optimizer falls back to scipy.optimize.
- **Lint:** no separate linter; run `python3 -m py_compile` on changed files.

## Git State

- HEAD: `868d6bc chore(kilo): checkpoint agent session` (most recent of several `chore(kilo): checkpoint agent session` commits).
- Working tree: only `__pycache__/*.pyc` files modified (stale bytecode, gitignored-ish). No source changes pending. No uncommitted source work.

## Immediate Next Steps

1. Confirm the handoff file is complete and accurate (this file).
2. If a real task arrives, start from the board (`board_read`) and the AGENTS.md quick-start commands above.
3. Before any commit: run `SEED=42 bash scripts/check.sh` and ensure goldens match HEAD and `ledger/golden_baseline.json`.
4. Do not create `.github/workflows/verification-gate.yml` directly — controller cleans that dir; use the template at `.github/workflow-templates/verification-gate.yml` + `VERIFICATION_GATE_TEMPLATE.md`.

## Open Items / Blockers

- None active. Research phase complete; no running experiment or blocker.