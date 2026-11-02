# DURABLE HANDOFF — Next Agentic Session

**Timestamp (UTC):** 2026-11-02T08:37:28Z
**Repo:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Branch:** main (HEAD `ea3f6f4 chore(kilo): checkpoint agent session`)
**State:** Research phase complete (E001–E057). Baseline verified clean. Working tree clean except gitignored `__pycache__/*.pyc` (13 files, pre-existing noise, not committed). No live verification snapshot (`.verify_snapshot/` absent) — nothing to recover. No open research task. Board is empty (no peer messages, no pending coordination).

## Initial task message for the next agentic work session

> **START HERE:** The repository is genuinely done. E057 (CI gate template audit) is complete and committed at HEAD. There is no open task. Wait for the user to give you a new instruction; do not invent one. Do **not** re-run `scripts/check.sh` to "confirm" the baseline — already done this session (exit 0, `=== All checks passed ===`). Do **not** write another handoff unless the user asks.

**If the user gives no new instruction, your entire job is to report status and stop.** If they do give one, follow the required sequence below.

## Required sequence (only if a new instruction arrives)

1. **Environment** — `pip install -r requirements.txt` if dependencies missing (numpy, pandas, scipy, pyarrow, statsmodels, yfinance). `cvxpy`/`cvxopt` optional; the optimizer falls back to `scipy.optimize`.
2. **Verify clean baseline** — `SEED=42 bash scripts/check.sh` — expect EXIT 0 with `=== All checks passed ===`. Confirm `git status --short` shows only `__pycache__/*.pyc` noise. The FAIL lines in that output are *negative test fixtures* (malformed JSONs in `tests/test_json_guard`, interrupted-run/pid-999999 detection in `tests/test_golden_baseline`, missing-cache/`panel.parquet`/`nope.json` cases in `tests/test_data_coverage`) — not real regressions.
3. **Recover if needed** — If verification was interrupted previously, restore goldens with `SEED=42 python3 run_all_verification.py --restore-only` before committing anything. The suite self-recovers at startup and refuses to start while another live run owns the snapshot.
4. **Identify next task** — Read `ledger/RESEARCH_LEDGER.md` top to bottom. The highest-value bounded task named in the ledger (E040, line ~3797) is a durable close-out summary table of all experiments; it is **not** pre-registered and must not be treated as a gate change. If all items are COMPLETE/CLOSED, confirm that explicitly and report status without changing gates, pre-registrations, or re-pinning artifacts.

## Constraints (standing, non-negotiable)

- **Never commit verification output.** Restore goldens first if interrupted (`SEED=42 python3 run_all_verification.py --restore-only`). The backup lives in the gitignored `.verify_snapshot/` with an `ACTIVE.json` pid marker.
- **Never re-pin goldens to silence drift.** Numeric drift from ill-conditioned solvers (E041 133 numeric diffs, E030/E029 0 since their panels were pinned) must remain visible. Only re-pin via `python3 scripts/check_golden_baseline.py --update` with explicit justification in the ledger.
- **Preserve pre-registrations.** Do not change gate logic, falsification expectations, sensitivity grids, pre-registered outcomes, or validated constructions.
- **Honor caches.** Respect pinned vintages (`data/vintages.json` → 2026-10-12), pinned fundamentals (`data/fundamentals/` per `data/fundamentals_vintages.json`), and `ledger/data_baseline.json`. The suite runs with `QUANT_RESEARCH_OFFLINE=1`; a missing cache entry fails hard instead of silently downloading (yfinance is not bit-reproducible).
- **Always use `SEED=42`.** Run `python3 -m py_compile` on any script you touch.
- **CI is maintainer-gated.** Do not create or commit anything under `.github/workflows/` (the controller restores that directory at checkpoints; the repo token lacks `workflows` push permission). Use the copyable template at `.github/workflow-templates/verification-gate.yml`; instructions are in `VERIFICATION_GATE_TEMPLATE.md`. The only remaining human step is copying that file into `.github/workflows/verification-gate.yml` via the GitHub UI.
- **Follow repo conventions** in `AGENTS.md`.

## Quick references

- **Checks:** `make check` | `make verify-quick` | `make verify-extended` | `make verify-full` | `SEED=42 python3 verify_convention_robustness.py`
- **Recovery:** `SEED=42 python3 run_all_verification.py --restore-only` (also `--skip-slow`, `--restore-only`)
- **Guards:** `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`, `scripts/check_json_artifacts.py`, `scripts/diff_golden.py`
- **Docs:** `AGENTS.md`, `ledger/RESEARCH_LEDGER.md`, `ledger/PRIORITIZATION.md`, `README.md`, `RELEASE_NOTES.md`, `PROMPT.MD`
- **Preceding handoff:** `HANDOFF_NEXT_SESSION_2026-11-02T08-35-16Z.md`

(End of file)