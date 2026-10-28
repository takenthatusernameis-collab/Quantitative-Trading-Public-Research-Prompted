# HANDOFF — Agentic Work Session

**Timestamp:** 2026-10-28T23-05-14Z
**Branch:** `main`
**Last commit:** `de4092e chore(kilo): checkpoint agent session`
**Working tree:** clean
?? HANDOFF_NEXT_SESSION_2026-10-28T23-05-14Z.md (untracked, this file)
**Verify snapshot:** none active (`.verify_snapshot/` absent)
**Golden baseline:** assumed pinned per `ledger/golden_baseline.json`; re-verify before committing

---

## Initial Task Message for Next Session

> **Task:** Resume quantitative-strategy research on the US equities/futures/macro repo. Research phase E001–E043 is complete and documented in `ledger/RESEARCH_LEDGER.md`. No new research is warranted unless explicitly requested by the user.
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

- Project: Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. Research phase E001–E043 complete; surviving validated strategies in `ledger/RESEARCH_LEDGER.md`.
- Conventions: close-to-close is the v1.2.3 primary convention; overnight decomposition is reported alongside.
- Dependencies: `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance). `cvxpy`/`cvxopt` optional; optimizer falls back to `scipy.optimize`.
- Data: pinned vintages `data/vintages.json` (2026-10-12), committed 2026-10-11 vintage, E029 fundamentals pinned in `data/fundamentals/`.
- Verification driver: `run_all_verification.py` (`--quick`/`--extended`/`--full`/`--skip-slow`/`--restore-only`).
- Ledger inconsistency to resolve if relevant: E048 says E042-lead is unfixed and breaks the primary gate; E049 says it is fixed. The authoritative check is `run_all_verification.py` itself.
- Consult `ledger/RESEARCH_LEDGER.md` for the authoritative record of surviving strategies and open items.

---

## Session event log (this session)

- Received request: "Leave a timestamped clear initial task message for the next agentic work session in a durable handoff !"
- Created durable handoff at: 2026-10-28T23-05-14Z
- Verified state: branch `main` at `de4092e`; working tree clean; no `.verify_snapshot/`.
- Repointed durable symlinks `HANDOFF.md`, `HANDOFF_CURRENT.md`, `HANDOFF_NEXT.md`, `HANDOFF_NEXT_SESSION.md` to this file.

---

## Suggested first command

```bash
git status --short && echo "---" && SEED=42 bash scripts/check.sh
```

## Current handoff pointer

This session's durable handoff: `HANDOFF_NEXT_SESSION_2026-10-28T23-05-14Z.md` (see also `HANDOFF_CURRENT.md`, `HANDOFF.md`).
