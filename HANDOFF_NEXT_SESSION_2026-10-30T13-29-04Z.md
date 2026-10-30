# Durable Handoff — Next Agentic Work Session

**Generated:** 2026-10-30T13:29:04Z (UTC)
**Session:** handoff-only session (no technical work performed)
**Working dir:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Branch:** main @ `de7aeab` (HEAD)
**Previous handoff:** `HANDOFF_NEXT_SESSION_2026-10-30T13-27-57Z.md`

---

## INITIAL TASK (do first)

**Confirm baseline integrity, then await explicit user direction.**

This session performed no technical work — it only wrote this handoff. The
working tree is clean of source/data changes; the only modifications are
untracked `__pycache__/*.pyc` build artifacts.

1. **Confirm repo state before anything else**
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   Expect exit 0: py_compile, goldens clean vs HEAD, pinned baseline match,
   data coverage, portfolio_opt tests, convention robustness, template
   validation, experiment-script imports. Confirmed passing at
   2026-10-30T13:27:57Z (prior session).

2. **If checks fail**
   - Goldens differ from HEAD → restore from the commit whose SHA-256 matches
     `ledger/golden_baseline.json` (or `SEED=42 python3 run_all_verification.py
     --restore-only`).
   - Never re-pin to silence drift; re-pinning requires
     `python3 scripts/check_golden_baseline.py --update` and must appear in
     the diff.

3. **Then idle awaiting explicit user direction.**
   - Do NOT make source changes or commits unless explicitly asked.
   - Do NOT modify `experiments/*.json` goldens as a side effect of
     verification.

---

## Current state

- **Research phase complete:** E001–E043. Surviving validated strategies in
  `ledger/RESEARCH_LEDGER.md`.
- **Working tree:** `git status --short` shows only `M scripts/__pycache__/*,
  M src/__pycache__/*, M tests/__pycache__/*` (tracked `.pyc` artifacts from
  prior sessions; no source/data changes). No verification snapshot active in
  `.verify_snapshot/` — `ls .verify_snapshot/` returns "no snapshot".
- **Goldens:** `experiments/*.json` match HEAD. `ledger/golden_baseline.json`
  pins 107 tracked artifacts.
- **Environment:** Python 3.12.3. `requirements.txt` already installed in this
  sandbox (numpy 2.5.4, pandas 3.0.6, scipy 1.18.1, pyarrow 26.0.0,
  statsmodels 0.15.0, yfinance 1.7.0). If the next session's environment is
  reset, re-run `pip3 install --break-system-packages -r requirements.txt`
  first — prior CI runs failed with `ModuleNotFoundError: No module named
  'pandas'`.

## Known open items (read AGENTS.md before acting)

- **Optimizer determinism (E049):** `src/portfolio_opt.py` validates solver
  answers on the problem's constraints, never on the solver's exit status;
  pinned by `tests/test_portfolio_opt.py` (first-class step of
  `scripts/check.sh`). The tangency QP itself remains ill-conditioned: a 1-ulp
  input perturbation still moves the `min_var` answers by ~1e-05, so the
  E041/E042 grid artifacts still drift by 29–133 differences. Do NOT re-pin
  them to silence that — see the open item in the ledger.
- **E041 drift root-caused (ledger E049):** 3 structural diffs gone, 133
  numeric remain; open item in the ledger.
- **Cache coverage enforced (E048):** `scripts/check_data_coverage.py`
  validates all data inputs are pinned in `ledger/data_baseline.json`. The
  verification suite re-executes every driver with
  `QUANT_RESEARCH_OFFLINE=1`, so a missing cache entry fails hard instead of
  silently downloading.
- **CI gate workflow** (`.github/workflows/verification-gate.yml`) still
  requires maintainer action (GitHub UI) — automated agents cannot push
  workflows. Copyable template at
  `.github/workflow-templates/verification-gate.yml`.

## Key commands

- `SEED=42 bash scripts/check.sh` — convention-robustness + template validation
  (~seconds, offline)
- `SEED=42 python3 run_all_verification.py` — quick full verification (~8 min)
- `SEED=42 python3 run_all_verification.py --extended` — extended (~21 min)
- `SEED=42 python3 run_all_verification.py --full` — full (~15 min)
- `SEED=42 python3 run_all_verification.py --restore-only` — recover goldens
  after interrupted run
- `python3 -m py_compile` on changed files (no separate linter)

## Notes

- `AGENTS.md` is the source of truth for commands/conventions; re-read before
  running the verification suite.
- The most recent substantive handoff is `HANDOFF_REPRO_CAVEAT.md` (documents
  the E041/E042 grid reproducibility caveat) and the ledger's E049 entry
  (E042-lead root cause). Both describe the *remaining* ill-conditioning, not
  a regression.
- Do not commit verification output; only intentional source/data changes.