# DURABLE HANDOFF — Next Agentic Session

**Timestamp (UTC):** ${TS}
**Repo:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Branch:** main
**State:** Research phase complete and closed (E001–E050). Canonical goldens in `experiments/`; ledger closed in `ledger/RESEARCH_LEDGER.md` (final entry E050). Working tree clean at HEAD. No live verification snapshot (`.verify_snapshot/` absent).

## Initial task message for the next agentic work session

> **START HERE:** The research phase is complete and closed. There is **no open research task** — do not start a new strategy family, do not re-open any experiment, do not re-pin goldens, and do not move any gate or goalpost. Your job is a **conformance pass only**: confirm the baseline is still clean, confirm closure, and report.

**Required sequence (do in order):**

1. **Environment** — `pip install -r requirements.txt` if dependencies are missing (numpy, pandas, scipy, pyarrow, statsmodels, yfinance). `cvxpy`/`cvxopt` optional.
2. **Verify clean baseline** — `SEED=42 bash scripts/check.sh` — expect EXIT 0 with `=== All checks passed ===`. Also run `git status --short` and confirm only `__pycache__/*.pyc` noise is acceptable.
3. **Confirm closure** — Read the tail of `ledger/RESEARCH_LEDGER.md` (E049/E050) and the E040 close-out table to confirm: novelty search exhausted (39 experiments E001–E039), market-neutral blend line closed (E041 REJECTED, E042 PARTIAL/G2-FAIL, E042b REJECTED/G2-FAIL), all gates and decisions final, no goalposts moved.
4. **Report status** — Confirm explicitly that all items are COMPLETE/CLOSED. Do **not** change gates, pre-registrations, falsification expectations, sensitivity grids, or validated constructions. Do **not** commit verification output.

## Constraints

- **Never commit verification output.** Restore goldens first if interrupted (`SEED=42 python3 run_all_verification.py --restore-only`).
- **Never re-pin goldens to silence drift.** Numeric drift from ill-conditioned solvers must remain visible; only re-pin via `python3 scripts/check_golden_baseline.py --update` with explicit justification in the ledger.
- **Preserve pre-registrations.** Do not change gate logic, falsification expectations, sensitivity grids, pre-registered outcomes, or validated constructions.
- **Honor caches.** Respect pinned vintages (`data/vintages.json`), pinned fundamentals (`data/fundamentals/`), and `ledger/data_baseline.json`. If adding data inputs, commit files and re-pin coverage via `python3 scripts/check_data_coverage.py --update`.
- **Always use SEED=42.** Offline behavior enforced in verification (`QUANT_RESEARCH_OFFLINE=1`).
- **Lint changes.** Run `python3 -m py_compile` on any modified Python files.
- **CI is maintainer-gated.** Do not attempt to create `.github/workflows/` — use template at `.github/workflow-templates/verification-gate.yml`.
- **Follow conventions.** Adhere to `AGENTS.md` throughout.

## Quick references

- **Checks:** `make check` | `make verify-quick` | `make verify-extended` | `make verify-full`
- **Recovery:** `SEED=42 python3 run_all_verification.py --restore-only`
- **Guards:** `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`, `scripts/check_json_artifacts.py`
- **Docs:** `AGENTS.md`, `ledger/RESEARCH_LEDGER.md`, `README.md`, `PROMPT.MD`

**Handoff created:** ${TS} (UTC)
