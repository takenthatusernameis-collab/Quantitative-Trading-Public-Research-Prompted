# Agentic Handoff — Initial Task Message

**Created:** 2026-11-12T05:06:52Z (UTC)
**Session:** New agentic work session — durable handoff
**Status:** Initial — no work completed in this session yet.

## Repository state

- Repo: quantitative trading research (2014–2026 US equities/futures/macro). Research phase complete (E001–E043); validated strategies in `ledger/RESEARCH_LEDGER.md`.
- HEAD: `81c9ea8d` chore(kilo): checkpoint agent session
- Canonical artifacts: `experiments/*.json` are committed goldens; verification suite backs them up and restores them. Never commit verification output.
- `.kilo/` populated with handoff symlinks + historical handoffs. Board empty.
- Dependencies: `pip install -r requirements.txt` (numpy, pandas, scipy, pyarrow, statsmodels, yfinance).

## Clear initial task (next session)

Establish a clean, verified baseline before any edits:

```bash
SEED=42 bash scripts/check.sh
#   or
make check
```

This runs `py_compile`, `check_goldens_clean.py` (working tree vs HEAD under `experiments/`), `check_golden_baseline.py` (SHA-256 vs `ledger/golden_baseline.json`), `check_data_coverage.py`, and `tests/test_portfolio_opt.py`. Offline, seconds-long, writes nothing to `experiments/`.

**Success criterion:** `scripts/check.sh` exits 0 with no golden mismatch or coverage failure. If a mismatch is reported, fix it before committing (do not let a verification run capture output into `experiments/`).

## Verified state at handoff

- `git status --short --branch` → `## main...origin/main` (in sync, `+0 -0`); tracked modifications are only `__pycache__/*.pyc` build artifacts (timestamp drift, not committed).
- `git ls-files experiments/` → 138 tracked entries (107 golden JSONs + 31 drivers).
- `.verify_snapshot/` absent → no interrupted verification run to recover.
- Prior session confirmed: `check_golden_baseline.py` → ALL 107 PINNED GOLDEN ARTIFACTS MATCH; `check_data_coverage.py` → ALL 35 PINNED DATA INPUTS PRESENT, TRACKED, UNCHANGED.

## Known open items (do not paper over)

- **E041:** 133 numeric diffs remain from 1-ulp QP sensitivity (ledger E049); extended verification still reports drift. Do **not** re-pin `experiments/e041*.json` to silence this.
- **E042:** min-var confirmatory is **PARTIAL** (4/5; G2 β-constrained placebo z 2.11 < 3.0 FAIL); market-neutral-total-portfolio line is **CLOSED**, not promoted. Confirmatory run with full placebo already executed and recorded — no further promotion path.
- **Process:** never re-pin golden/data baselines as a side effect of verification; baseline replacement requires explicit `--update` + review.

## Notes

- Never commit verification output; interrupted runs leave driver output in `experiments/` — restore with `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`.
- To re-pin a golden: `python3 scripts/check_golden_baseline.py --update` (puts replacement in the diff).
- To add a data input: commit the file and re-pin with `python3 scripts/check_data_coverage.py --update`.
- Reproducibility: always use `SEED=42`. Suite re-executes drivers with `QUANT_RESEARCH_OFFLINE=1`.
- No separate linter configured; run `python3 -m py_compile` on changed Python files. Follow existing code style; no comments/emojis unless requested. Do not commit secrets.