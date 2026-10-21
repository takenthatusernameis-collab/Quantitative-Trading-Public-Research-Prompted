# Session Handoff: Hardened committed-artifact schema guard

## What changed

No prior agent assignment existed (single commit `caf2fb7`, clean tree). I
inspected the repo, confirmed the handoff chain is fully closed (all 27
experiment drivers committed, all goldens reproduce structurally under SEED=42,
convention gate covers 15 strategies, `check.sh` green), and then executed the
bounded task left in `HANDOFF_NEXT_SESSION.md` which had **not** been
implemented: hardening `scripts/check_json_artifacts.py` beyond parse-only.

- `scripts/check_json_artifacts.py` rewritten to enforce a *schema* invariant
  on top of parse validity. Every committed experiment record must now carry a
  stable identifier (`experiment` or `experiment_id`) and the structural
  markers of its schema class: `grid` + `n_configs` for sensitivity grids,
  `strategy` + `benchmark` + `oos_sharpe` for batch_run per-strategy
  evaluations, `decision` for study records. Non-experiment artifacts (batch
  summary, validation summary, cost-sweep lists, E024 sub-parts, the
  data-vintage manifest) are allowlisted by name so the guard cannot be
  satisfied by deleting files. The parse check is retained as the inner loop.
- Documentation updated to record the hardening:
  - `README.md` reproducibility section: guard now asserts parse AND schema.
  - `ledger/RESEARCH_LEDGER.md`: E031 Erratum 2 (schema hardening).
  - `RELEASE_NOTES.md`: new "Release follow-ups (post v1.2.3)" section.

## What was actually verified (evidence)

- Baseline: `SEED=42 bash scripts/check.sh` -> `=== All checks passed ===`
  (exit 0), 107/107 committed JSON artifacts parse AND schema-check OK.
- `SEED=42 python3 run_all_verification.py --skip-slow` -> OVERALL: ALL
  CHECKS PASSED (new schema guard + convention robustness).
- Negative tests (all confirmed `rc=1` with the offending file named, then
  restored): (1) malformed JSON — stray `]` closing a dict (the E031 class);
  (2) stripped `experiment` identifier from a sensitivity grid; (3) stripped
  `decision` from a data-infeasibility study; (4) stripped `oos_sharpe` from a
  strategy-eval artifact; (5) deleted an experiment file — guard still fails
  (read error), so it cannot be satisfied by deletion.
- `python3 -m py_compile scripts/check_json_artifacts.py` -> OK.
- `SEED=42 python3 run_all_verification.py` (quick, ~8 min) -> 2 FAILs:
  `run_e037.py` (28 numeric diffs) and `run_e042_lead.py` (22 numeric diffs).
  **Both match the documented baseline in `HANDOFF_REPRO_CAVEAT.md` exactly**
  (E037: 28 numeric diffs, ~1e-7 rel; E042_lead: 22 diffs incl. OOS 0.866 ->
  0.822, beta -0.001 -> +0.035). They are the known SLSQP BLAS/LAPACK
  float-drift, not regressions from this change — the JSON guard (step 0.5)
  passed in both suite runs. Direct re-runs confirm: E037 reproduces with 0
  diffs when executed alone; E042_lead reproduces with 0 structural diffs and
  only the documented numeric drift.
- `git diff --name-only` contains only `README.md`, `RELEASE_NOTES.md`,
  `ledger/RESEARCH_LEDGER.md`, `scripts/check_json_artifacts.py`. **No
  committed golden JSON was modified.**

## What remains unresolved

- The E041/E042 sensitivity grids and the full E042 confirmatory golden are
  not byte-reproducible in this sandbox (SLSQP drift); documented in
  `HANDOFF_REPRO_CAVEAT.md`. No gate or decision is affected.
- CI gate workflow (`.github/workflows/verification-gate.yml`) still requires
  maintainer creation via GitHub UI (template at
  `.github/workflow-templates/verification-gate.yml`); automated agents cannot
  push workflows.

## Which approaches have already failed and why

- No approach failed this session. The schema guard was prototyped first
  (classify every committed artifact by structure, check candidate required
  fields) to avoid misclassifying legitimate artifacts — this caught two
  real bugs during implementation (a `rel`/`basename` mismatch on
  `data/vintages.json`, and an over-strict `status` requirement that E033
  legitimately omits). Both were fixed by making the requirement
  identifier-based rather than field-list-based, not by loosening the check.
- The quick-verification suite's 2 FAILs are the documented float-drift baseline,
  reproduced identically before and after this change; they are not caused by
  the guard edit (the guard runs before the drivers and passed both times).

## One precise next task

The repository is in a clean, fully-documented state and the recommended
bounded task is complete. The only remaining durable action outside agent scope
is the maintainer-gated CI workflow creation. If a further bounded in-session
task is desired, the lowest-risk option is to re-run
`SEED=42 bash scripts/check.sh` (already passing) and confirm `git diff`
contains only the four documentation/guard files listed above.

### Constraints
- Do NOT modify committed goldens; rely on `run_all_verification.py`'s
  backup/restore mechanism.
- Honor `SEED=42` and the cached 2026-10-12 parquet vintage.
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or
  validated constructions (`src/backtest.py`, `src/strategies.py`,
  `src/futures.py`, `src/macro.py`, `src/portfolio_opt.py`).