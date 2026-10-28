# HANDOFF — Timestamped initial task for next agentic session

Timestamp (UTC): 2026-10-28T07-31-04Z
Repo: Quantitative-Trading-Public-Research-Prompted
Branch: main
HEAD: bd0ac2afb059fc5919121430f618430cff16b80c
Working tree: check with `git status --short` (only __pycache__ expected)
Verify snapshot: none active (.verify_snapshot/ACTIVE.json absent)

## Mission for next session
Start here and verify baseline integrity before making any changes. This repo is in post-research state (E001–E043) with strict baseline/verification guards.

## Current known state
- Research complete; surviving validated strategies in `ledger/RESEARCH_LEDGER.md`
- Verification guards: `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`
- Optimizer determinism pinned by `tests/test_portfolio_opt.py` (solver exit status must not gate feasibility/optimality)
- Data: pinned vintages `data/vintages.json` (2026-10-12), committed 2026-10-11 vintage, E029 fundamentals pinned in `data/fundamentals/` per `data/fundamentals_vintages.json`
- Verification driver: `run_all_verification.py` (`--quick`/`--extended`/`--full`/`--skip-slow`/`--restore-only`). Backups in `.verify_snapshot/` (gitignored) with `ACTIVE.json` marker.
- CI workflow cannot be created by agents (controller restores `.github/workflows/`, token lacks `workflows` push). Template at `.github/workflow-templates/verification-gate.yml`.

## Immediate priorities (do in order)
1. **Clean baseline** — Run `git status --short`. If any tracked files differ, do **not** re-pin goldens. Follow AGENTS.md baseline integrity rules.
2. **Sanity check** — Run `SEED=42 bash scripts/check.sh` (convention-robustness + template validation + golden/data/coverage guards). All must pass.
3. **Verify reproducibility (choose scope)** — If check passes:
   - Quick (~8 min): `SEED=42 python3 run_all_verification.py`
   - Extended (~21 min): `SEED=42 python3 run_all_verification.py --extended` (E041 still has numeric drift; do **not** re-pin)
   - Full (~15–30 min): only if explicitly needed
4. **Recovery if interrupted** — If verification was cut off or goldens look modified: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`. Confirm `.verify_snapshot/ACTIVE.json` removed.

## Known open items
- **E041 numeric drift (133 diffs)** due to 1-ulp sensitivity of ill-conditioned tangency QP. Structural diffs resolved, gates/decision unchanged. Open in ledger; do **not** silence by re-pinning.
- **E030/E029** now offline-reproducible via pinned inputs; do not revert to live yfinance downloads.
- **Data coverage invariant**: any new `data.download()` inputs must be committed and re-pinned via `python3 scripts/check_data_coverage.py --update`.

## Suggested first command
=== Fast verification checks ===
checked 114 committed JSON artifacts
ALL COMMITTED JSON ARTIFACTS PARSE OK
ALL COMMITTED GOLDEN ARTIFACTS MATCH HEAD
ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT
ALL 35 PINNED DATA INPUTS ARE PRESENT, TRACKED AND UNCHANGED
FAIL experiments/d.json: SCHEMA: DATA_INFEASIBILITY missing required field 'decision'
FAIL experiments/d.json: SCHEMA: DATA_INFEASIBILITY missing identifier field ['experiment', 'experiment_id']
checked 1 committed JSON artifacts
JSON ARTIFACT CHECKS FAILED (2 malformed)
FAIL experiments/d2.json: SCHEMA: DATA_INFEASIBILITY missing required field 'decision'
checked 1 committed JSON artifacts
JSON ARTIFACT CHECKS FAILED (1 malformed)
checked 1 committed JSON artifacts
ALL COMMITTED JSON ARTIFACTS PARSE OK
checked 1 committed JSON artifacts
ALL COMMITTED JSON ARTIFACTS PARSE OK
FAIL experiments/b.json: JSONDecodeError: Expecting property name enclosed in double quotes: line 1 column 2 (char 1)
checked 1 committed JSON artifacts
JSON ARTIFACT CHECKS FAILED (1 malformed)
FAIL experiments/x.json: SCHEMA: unrecognized artifact structure
checked 1 committed JSON artifacts
JSON ARTIFACT CHECKS FAILED (1 malformed)
FAIL experiments/e2.json: SCHEMA: unrecognized artifact structure
checked 1 committed JSON artifacts
JSON ARTIFACT CHECKS FAILED (1 malformed)
FAIL experiments/badlist.json: SCHEMA: unexpected top-level list
checked 1 committed JSON artifacts
JSON ARTIFACT CHECKS FAILED (1 malformed)
FAIL experiments/u.json: SCHEMA: unrecognized artifact structure
checked 1 committed JSON artifacts
JSON ARTIFACT CHECKS FAILED (1 malformed)
ALL COMMITTED GOLDEN ARTIFACTS MATCH HEAD
verification run in progress (pid 36571); the golden artifacts are temporarily modified by design
FAIL 1 golden artifact(s) differ from HEAD:
   M experiments/e001.json
  the committed baseline was modified outside the verification suite
  recover with: git checkout -- experiments/
FAIL interrupted verification run: snapshot /home/runner/work/_temp/kilo-tmp/tmpqn31sae9/.verify_snapshot is owned by pid 999999, which is no longer running
  the committed goldens in experiments/ may be overwritten by that run
  recover with: python3 run_all_verification.py --restore-only
  (or: git checkout -- experiments/)
NOTE 1 untracked file(s) under experiments/ (not a baseline failure):
  ?? experiments/e042_quick.json
ALL COMMITTED GOLDEN ARTIFACTS MATCH HEAD
NOTE 1 pinned data file(s) were not rediscovered by the static scan (they are kept pinned on purpose - a request that is only reachable dynamically):
  data/panel.parquet
ALL 1 PINNED DATA INPUTS ARE PRESENT, TRACKED AND UNCHANGED
FAIL 1 pinned data file(s) missing from the working tree:
  data/panel.parquet
  a driver that needs this input will re-download it from the network
NOTE 1 pinned data file(s) were not rediscovered by the static scan (they are kept pinned on purpose - a request that is only reachable dynamically):
  data/panel.parquet
FAIL cannot read manifest: No such file or directory: /home/runner/work/_temp/kilo-tmp/tmp1ltq0nro/nope.json
  the pinned data fingerprint is missing or unreadable
  regenerate with: python3 scripts/check_data_coverage.py --update
FAIL 1 pinned data file(s) differ from the pinned fingerprint:
  data/panel.parquet
    pinned: 320e00e73a7d24a9a44cde87e98d150e10e72b05ccffb74e7332354fdd85c5e5
    actual: 9d6f965ac832e40a5df6c06afe983e3b449c07b843ff51ce76204de05c690d11
  the committed artifacts were derived from the pinned snapshot
NOTE 1 pinned data file(s) were not rediscovered by the static scan (they are kept pinned on purpose - a request that is only reachable dynamically):
  data/panel.parquet
FAIL 1 pinned data file(s) are not git-tracked:
  data/panel.parquet
  a fresh clone would not contain them and would re-download from the network
  add them with: git add -f <path>   (.gitignore ignores data/*.parquet)
NOTE 1 pinned data file(s) were not rediscovered by the static scan (they are kept pinned on purpose - a request that is only reachable dynamically):
  data/panel.parquet
============================================================
CONVENTION-ROBUSTNESS VERIFICATION
Policy v1.2.3: Primary = close-to-close
============================================================

=== TSM Pure (Equity Flagship) ===
  OOS Sharpe (c2c):       1.739  (target: 1.739)
  OOS Sharpe (overnight): 2.157  (target: 2.157)
  Beta vs SPY (c2c):      -0.119  (target: -0.119)
  Beta vs SPY (overnight):-0.065  (target: -0.065)
  ✓ PASS

=== Dollar-Neutral Low-Beta Sort ===
  OOS Sharpe (c2c):       1.053  (from README final summary)
  OOS Sharpe (overnight): 1.287  (target: 1.287, committed E013 value)
  Beta vs SPY (c2c):      +1.02  (from E041 convention_findings)
  Beta vs SPY (overnight): -0.035  (from README)
  ✓ PASS

=== Futures TSM 18m (de-seamed) ===
  OOS Sharpe (c2c):       0.805  (target: 0.805)
  Beta vs SPY (c2c):      -0.010  (target: -0.010)
  Overnight: balanced split (E024 audit)
  ✓ PASS

=== Futures Carry (Realized Roll Yield) ===
  OOS Sharpe (c2c):       0.523  (target: 0.523)
  Beta vs SPY (c2c):      0.014  (target: +0.014)
  Overnight: balanced split (E024 audit)
  ✓ PASS

=== Macro Momentum (Brooks 2017) ===
  OOS Sharpe (c2c):       0.006  (from README final summary)
  OOS Sharpe (overnight): 0.428  (target: 0.428)
  Beta vs SPY (c2c):      -0.011  (target: -0.011)
  ✓ PASS

=== Low-Vol Flagship (unlevered) ===
  OOS Sharpe (c2c):       1.728  (target: 1.728)
  Beta vs SPY (c2c):      1.084  (target: +1.084)
  Overnight: not separately reported (E024 audit would show concentration)
  ✓ PASS

=== E024 Overnight-Intraday Decomposition (part_b) ===
  reversal           c2c 1.461 (target 1.461) | overnight 2.288 (target 2.288) | conv_dep True (target True)
  low_vol            c2c 1.591 (target 1.591) | overnight 1.748 (target 1.748) | conv_dep False (target False)
  momentum           c2c 1.150 (target 1.150) | overnight 1.248 (target 1.248) | conv_dep True (target True)
  value              c2c 1.015 (target 1.015) | overnight 1.120 (target 1.120) | conv_dep False (target False)
  quality            c2c 1.485 (target 1.485) | overnight 1.523 (target 1.523) | conv_dep False (target False)
  short_reversal     c2c 0.931 (target 0.931) | overnight 0.776 (target 0.776) | conv_dep False (target False)
  mean_reversion_5   c2c 0.608 (target 0.608) | overnight 0.087 (target 0.087) | conv_dep False (target False)
  price_trend        c2c 0.539 (target 0.539) | overnight 1.064 (target 1.064) | conv_dep False (target False)
  ✓ PASS (8/8 strategies match recorded E024 decomposition)

=== E042 Min-Variance Market-Neutral Blend ===
  OOS Sharpe (c2c):       0.979  (target: 0.979, gate: ≥0.8 → PASS)
  Placebo z (constrained): 1.60  (stochastic 50-sim; gate: ≥3.0 → FAIL)
  Beta vs SPY (full):     0.094  (target: +0.094, gate: ≤0.1 → PASS)
  Bear Sharpe:            1.97  (target: +1.967, gate: >0 → PASS)
  Turnover:               0.0043  (target: 0.0043, gate: ≤0.15 → PASS)
  Gates passed: False (4/5)
  Decision: PARTIAL
  ✓ PASS (PARTIAL 4/5 as recorded — G2 placebo-significance fails; not promoted)

============================================================
ALL VERIFICATIONS PASSED
============================================================
OK
OK   run_e011.py: calls+imports
OK   run_e012.py: calls+imports
OK   run_e013.py: calls+imports
OK   run_e015.py: calls+imports
OK   run_e016.py: calls+imports
OK   run_e017.py: calls+imports
OK   run_e018.py: calls+imports
OK   run_e019.py: calls+imports
OK   run_e020.py: calls+imports
OK   run_e021.py: calls+imports
OK   run_e022.py: calls+imports
OK   run_e023.py: calls+imports
OK   run_e024.py: calls+imports
OK   run_e025.py: calls+imports
OK   run_e026.py: calls+imports
OK   run_e027.py: calls+imports
OK   run_e028.py: calls+imports
OK   run_e029.py: calls+imports
OK   run_e030.py: calls+imports
OK   run_e034.py: calls+imports
OK   run_e035.py: calls+imports
OK   run_e036.py: calls+imports
OK   run_e037.py: calls+imports
OK   run_e039.py: calls+imports
OK   run_e041.py: calls+imports
OK   run_e042.py: calls+imports
OK   run_e042_lead.py: calls+imports
ALL EXPERIMENT SCRIPT IMPORTS OK
=== All checks passed ===

## Hard rules
- Always use `SEED=42`
- Close-to-close is primary convention v1.2.3; overnight decomposition reported
- Pre-registration + multiple-testing discipline apply
- **Never** commit verification output. Restore goldens if left modified.
- **Never** re-pin `experiments/*.json` or `ledger/golden_baseline.json` as a side effect of running verification
