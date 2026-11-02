# DURABLE HANDOFF — Next Agentic Session

**Timestamp (UTC):** 2026-11-02T02-46-32Z
**Repo:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Branch:** main (HEAD c22f650 chore(kilo): checkpoint agent session)
**State:** Research phase complete (E001–E050). Canonical goldens in `experiments/`, ledger in `ledger/RESEARCH_LEDGER.md`. Baseline verified clean at HEAD. No live verification snapshot (`.verify_snapshot/` absent). Working tree clean except gitignored `__pycache__/*.pyc`.

## Initial task message for the next agentic work session

> **START HERE:** The baseline is verified clean and all known optimizer determinism issues (E049/E050) are closed. Do **not** re-open the optimizer determinism item and do **not** re-pin goldens to silence drift. Pick up the next actionable item from the research ledger and proceed methodically.

**Required sequence (do in order):**

1. **Environment** — `pip install -r requirements.txt` if dependencies missing (numpy, pandas, scipy, pyarrow, statsmodels, yfinance). `cvxpy`/`cvxopt` optional.
2. **Verify clean baseline** — `SEED=42 bash scripts/check.sh` — expect EXIT 0 with `=== All checks passed ===`. Also run `git status --short` and confirm only `__pycache__/*.pyc` noise.
3. **Recover if needed** — If verification was interrupted previously, restore goldens with `SEED=42 python3 run_all_verification.py --restore-only` before committing anything.
4. **Identify next task** — Read `ledger/RESEARCH_LEDGER.md` from top to bottom to identify the highest-priority open item (if any). If all items marked COMPLETE/CLOSED, confirm that explicitly and report status without changing gates/pre-registrations or re-pinning artifacts.

## Constraints

- **Never commit verification output.** Restore goldens first if interrupted (`SEED=42 python3 run_all_verification.py --restore-only`).
- **Never re-pin goldens to silence drift.** Numeric drift from ill-conditioned solvers must remain visible; only re-pin via `python3 scripts/check_golden_baseline.py --update` with explicit justification in the ledger.
- **Preserve pre-registrations.** Do not change gate logic, falsification expectations, sensitivity grids, pre-registered outcomes, or validated constructions.
- **Honor caches.** Respect pinned vintages (`data/vintages.json`), pinned fundamentals (`data/fundamentals/`), and `ledger/data_baseline.json`. If adding data inputs, commit files and re-pin coverage.
- **Always use SEED=42.** Follow offline behavior where applicable (`QUANT_RESEARCH_OFFLINE=1` is enforced in verification).
- **Lint changes.** Run `python3 -m py_compile` on any modified Python files.
- **CI is maintainer-gated.** Do not attempt to create `.github/workflows/` — use template at `.github/workflow-templates/verification-gate.yml`.
- **Follow conventions.** Adhere to `AGENTS.md` throughout.

## Quick references

- **Checks:** `make check` | `make verify-quick` | `make verify-extended` | `make verify-full`
- **Recovery:** `SEED=42 python3 run_all_verification.py --restore-only`
- **Guards:** `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`
- **Docs:** `AGENTS.md`, `ledger/RESEARCH_LEDGER.md`, `README.md`

(End of file)
