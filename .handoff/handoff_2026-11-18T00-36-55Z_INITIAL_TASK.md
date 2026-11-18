# Agentic Work Session Handoff

**Timestamp**: 2026-11-18T00:36:55Z
**Session ID**: Initial handoff for next agentic work session (E477)
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**HEAD**: 4f10b8792a85cd8e240ee17e00d3dd6e93c070c6 (== origin/main, 0 ahead / 0 behind)

## Project Context

This is an independent reproducible quantitative-strategy research project on
2014–2026 US equities, futures, and macro data. All experiments are
pre-registered with falsification expectations and promotion gates. **Research
phase is complete (E001–E051).** Surviving validated strategies are documented
in `ledger/RESEARCH_LEDGER.md`. The ledger records durable-handoff refreshes
through E474; this session is E477. (Handoff artifacts E475 and E476 exist at
the repo root but were not written back to the ledger; this entry resumes the
ledger sequence at E477.)

## Reproduce / Verify (Quick Start)

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh
#   or
make check

# Quick full verification (~8 min; 8 experiment drivers + batch_run + validate + E042 n_sim=2)
SEED=42 python3 run_all_verification.py
#   or
make verify-quick

# Extended verification (~21 min; quick + 18 more committed drivers, structural match)
SEED=42 python3 run_all_verification.py --extended
#   or
make verify-extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full
#   or
make verify-full

# Recover the golden artifacts after an interrupted verification run
SEED=42 python3 run_all_verification.py --restore-only
```

## Baseline Integrity (read before running the suite)

`experiments/*.json` are the canonical research artifacts. The verification
suite overwrites them while re-running drivers and restores them afterward, so
**a verification run must never be left half-finished**:

- The backup lives in repo-local, gitignored `.verify_snapshot/` with an
  `ACTIVE.json` marker holding the owning pid. A killed run (SIGKILL / OOM /
  session timeout) stays recoverable.
- `scripts/check_goldens_clean.py` fails when a tracked artifact under
  `experiments/` differs from HEAD or when a stale snapshot is pending.
- `scripts/check_golden_baseline.py` compares every tracked artifact with the
  SHA-256 fingerprint pinned in `ledger/golden_baseline.json`. Replacing an
  artifact requires re-pinning (`python3 scripts/check_golden_baseline.py
  --update`). Never re-pin as a side effect of running the verification suite —
  the committed golden is the authoritative record, not the latest re-run.
- Recovery: `SEED=42 python3 run_all_verification.py --restore-only`
  (or `git checkout -- experiments/`, or `git checkout <commit> --
  experiments/<file>` for the SHA-256-pinned artifact).

## Reproducibility Notes

- **Seed**: always `SEED=42` (walk-forward + placebo RNG).
- **Convention**: close-to-close is the v1.2.3 primary convention; overnight
  decomposition is reported alongside every strategy.
- **Data**: cached parquet in `data/` (gitignored except the pinned
  2026-10-12 and 2026-10-11 vintages). Cache coverage is an enforced invariant
  (`scripts/check_data_coverage.py`); unpinned inputs are live downloads and
  yfinance is not bit-reproducible. Verification runs with `QUANT_RESEARCH_OFFLINE=1`.
- **Dependencies**: `pip install -r requirements.txt` (numpy, pandas, scipy,
  pyarrow, statsmodels, yfinance). `cvxpy`/`cvxopt` optional; optimizer falls
  back to `scipy.optimize`.
- **Optimizer determinism (ledger E049)**: the E041/E042 grid artifacts still
  drift by 29–133 differences due to an ill-conditioned QP (1-ulp sensitivity).
  Do **not** re-pin them to silence that.

## Current Status (as of 2026-11-18T00:36:55Z)

- Branch `main`; HEAD `4f10b879` == `origin/main` (0 ahead / 0 behind).
- Working tree clean apart from 15 tracked `__pycache__/*.pyc` (bytecode noise,
  not source changes).
- No `.verify_snapshot/` or `.verify_reports/` pending.
- 107 golden artifacts under `experiments/` match `ledger/golden_baseline.json`
  and HEAD.
- CI: `.github/workflows/` cannot be created by agents; a copyable template
  lives at `.github/workflow-templates/verification-gate.yml` (maintainer must
  create the real workflow via the GitHub UI).

## Next Steps for New Session

1. Run `SEED=42 bash scripts/check.sh` (convention robustness + goldens guards).
2. Run `SEED=42 python3 run_all_verification.py` (verify-quick) to confirm
   end-to-end reproducibility.
3. Review `ledger/RESEARCH_LEDGER.md` for surviving strategies and open items
   (E041/E042 optimizer-drift disposition).
4. If a task is assigned beyond handoff refresh, confirm scope with the user
   before running the full/extended suites or re-pinning any baseline.

## Standing Constraints

- Research phase complete (E001–E051); handoff refreshes continue the ledger
  (E477).
- Do not commit verification output; do not re-pin golden/data baselines unless
  the user explicitly directs it.
- This handoff is a durable artifact; leave it uncommitted unless the user asks
  to commit.

---

*This handoff was created automatically to provide context for the next agentic
work session. Durable artifact mirrored to `handoff/`, `HANDOFFS/`,
`.handoff/`, `.kilo/`, `.kilo/handoff/` with generic alias pointers repointed
via `scripts/repoint_handoff.py`.*