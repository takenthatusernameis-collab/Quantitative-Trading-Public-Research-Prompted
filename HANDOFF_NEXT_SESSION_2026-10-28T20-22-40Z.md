# HANDOFF — Agentic Work Session

**Timestamp:** 2026-10-28T20:22:53Z
**Branch:** `main`
**Last commit:** `f2d8b89 chore(kilo): checkpoint agent session`
**Working tree:** clean except for modified `__pycache__/*.pyc` files (gitignored, no action needed)

---

## Initial Task Message for Next Session

> **Task:** Resume quantitative-strategy research on the US equities/futures/macro repo.
> Research phase E001–E043 is complete and documented in `ledger/RESEARCH_LEDGER.md`.
>
> **Immediate priorities:**
> 1. **Verify baseline integrity before any commit.** Run `SEED=42 bash scripts/check.sh` (or `make check`). If it reports a golden mismatch under `experiments/`, fix it *before* committing — a checkpoint commit that captures verification output silently replaces the canonical baseline (see AGENTS.md "Baseline Integrity"). Recovery: `SEED=42 python3 run_all_verification.py --restore-only`, or `git checkout <commit> -- experiments/<file>` using the last commit whose SHA-256 matches `ledger/golden_baseline.json`.
> 2. **Never re-pin goldens as a side effect of verification.** The committed golden is the authoritative record, not the latest re-run. Re-pinning requires `python3 scripts/check_golden_baseline.py --update` and must be an explicit, deliberate act.
> 3. **Known drift (do not re-pin to silence):**
>    - E041: 133 numeric diffs (1-ulp sensitivity of ill-conditioned QP) + 0 structural. Open item in ledger.
>    - E042 grid artifacts: drift by 29–133 differences for the same reason.
>    - E030 / E029: now reproduce with 0 differences since 2026-10-20 (inputs pinned).
> 4. **Data coverage invariant:** `scripts/check_data_coverage.py` enforces that every `data.download()` call site resolves to a git-tracked cache file matching `ledger/data_baseline.json`. The suite runs drivers with `QUANT_RESEARCH_OFFLINE=1`. To add a data input, commit the file and re-pin.
> 5. **Reproducibility:** Always use `SEED=42`. Quick verify: `SEED=42 python3 run_all_verification.py` (~8 min). Extended: `--extended` (~21 min). Full: `--full` (~15 min).
> 6. **CI gate:** The intended `.github/workflows/verification-gate.yml` cannot be created by automated agents (controller restores `.github/workflows/` at checkpoints; repo `GITHUB_TOKEN` lacks `workflows` push permission). A copyable template is at `.github/workflow-templates/verification-gate.yml` — a maintainer must create the actual workflow via the GitHub UI.
> 7. **Lint/format:** No separate linter. Run `python3 -m py_compile` on changed files.
>
> **Standing dispositions:** Negative results are recorded honestly (REJECTED / PARTIAL with evidence). Sensitivity grids are "reported, not gated." Goalposts are never moved post-hoc.

---

## Context Notes

- Project: Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data.
- Conventions: close-to-close is the v1.2.3 primary convention; overnight decomposition is reported alongside.
- Dependencies: `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance). `cvxpy`/`cvxopt` optional; optimizer falls back to `scipy.optimize`.
- The most recent substantive work predates the checkpoint commits; consult `ledger/RESEARCH_LEDGER.md` for the authoritative record of surviving strategies and open items.