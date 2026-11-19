# Agentic Work Session Handoff — Clear Initial Task Message

**Created**: 2026-11-19T08:57:07Z
**Supersedes**: `handoff_2026-11-19T08-55-06Z_INITIAL_TASK.md` (thin stub) and `handoff_2026-11-19T08-02-14Z` / `NEXT_HANDOFF` refresh (HEAD `03c2b982`) — as the current durable artifact only; no earlier content altered
**Working directory**: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Repository state at creation**: HEAD `53679181` ("chore(kilo): checkpoint agent session", 2026-11-19T08:55:15Z) == `origin/main` (0 ahead / 0 behind); working tree clean; `.verify_snapshot/` and `.verify_reports/` absent.

## INITIAL TASK — read this first

You are continuing an independent, reproducible quantitative-research repository whose
research phase is **CLOSED** (E001–E051 experiments). The authoritative record is
`ledger/RESEARCH_LEDGER.md`. This handoff refreshes state through ledger entry **E528**.

**Default action: orient, verify, then await explicit user instruction.** Do NOT start new
research, open new experiments, change pre-registered gates, re-pin baselines, or modify
experiment artifacts unless the user explicitly asks.

## Start Here (ordered)

1. **Orient** (read-only):
   - `git log --oneline -5`
   - `git status --short --branch`  (expect `## main...origin/main`, clean)
   - `git rev-parse HEAD origin/main`  (must match)
2. **Recover any interrupted verification** — if `.verify_snapshot/` exists, run
   `SEED=42 python3 run_all_verification.py --restore-only` BEFORE anything else.
   Never commit captured verification output over the goldens.
3. **Confirm golden integrity** (fast, pure-stdlib, no writes):
   - `python3 scripts/check_goldens_clean.py`          → "ALL COMMITTED GOLDEN ARTIFACTS MATCH HEAD"
   - `python3 scripts/check_golden_baseline.py`        → "ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT"
   - `git diff --name-only HEAD -- experiments/`       → empty
4. **Install dependencies** (not installed on this runner): `pip install -r requirements.txt`.
5. **Run the fast gate**: `SEED=42 bash scripts/check.sh` (≈seconds, offline) — or `make check`.
6. **Await explicit instruction.** If none is given, do not invent work; refresh this handoff and report.
7. **Before ending**: write your own timestamped handoff (`handoff_<UTC>_INITIAL_TASK.md`),
   repoint aliases with `python3 scripts/repoint_handoff.py <new-filename>`, verify, append a
   ledger entry, and leave changes uncommitted unless asked.

## Verification scopes (only if explicitly requested)

- Always use **`SEED=42`** (walk-forward + placebo RNG).
- `make check` — fast guards (~seconds, offline).
- `SEED=42 python3 verify_convention_robustness.py` — read-only convention check.
- `SEED=42 python3 run_all_verification.py` — quick (~8 min).
- `SEED=42 python3 run_all_verification.py --extended` — extended (~21 min).
- `SEED=42 python3 run_all_verification.py --full` — full (~15 min, E042 n_sim=50 + 96-config grid).
- Verification overwrites and restores `experiments/*.json`; never leave a run half-finished,
  never commit its output over the canonical goldens. Restore with `--restore-only`.

## Integrity Rules (non-negotiable)

- Never commit verification output over `experiments/*.json`.
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` as a side effect.
  Re-pin only with explicit, intentional instruction and a ledger justification
  (`python3 scripts/check_golden_baseline.py --update` / `scripts/check_data_coverage.py --update`).
- Cache coverage is an enforced invariant: under `QUANT_RESEARCH_OFFLINE=1` a missing/pinned-mismatch
  cache entry fails hard instead of downloading (yfinance is not bit-reproducible).
- Optimizer determinism (ledger E049): `src/portfolio_opt.py` validates solver answers on the
  problem's constraints, never on the solver exit status. Do not gate on scipy status codes.
- Known residual drift: E041/E042 1-ulp QP drift (~1e-05) is expected — do NOT re-pin to silence it.
- Closed — do not reopen: E049/E050 (optimizer determinism + exact KKT enumeration).
- Do not create `.github/workflows/` CI gates as an automated agent; a maintainer must add the
  workflow from `.github/workflow-templates/verification-gate.yml`.
- Do not change pre-registered gates/sensitivity grids/falsification expectations or outcomes
  without explicit justification and a ledger update.
- Never commit secrets/keys; never log secrets. Do not commit unless the user explicitly asks.

## Key References

- `AGENTS.md` — commands, reproducibility, baseline-integrity invariants
- `ledger/RESEARCH_LEDGER.md` — all experiment dispositions and open items (handoff refreshes through E528)
- `ledger/PRIORITIZATION.md` — candidate ranking procedure
- `experiments/*.json` — canonical research artifacts (107 pinned of 138 tracked)
- `scripts/check.sh`, `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`,
  `scripts/check_data_coverage.py`, `scripts/repoint_handoff.py`, `run_all_verification.py`

## State verified at handoff creation (this session)

- HEAD `536791815adbd9b945c8842c88e3afd9138d385d` == `origin/main`; tree clean.
- `.verify_snapshot/` and `.verify_reports/` absent; no interrupted verification to recover.
- `check_goldens_clean.py` green; `check_golden_baseline.py` green (107/107); no `experiments/` diff.
- `git ls-files experiments/` → 138 tracked artifacts, 107 of them `experiments/*.json` goldens.
- Environment note: `/usr/bin/python3` 3.12.3; numpy/pandas/scipy/pyarrow/statsmodels are NOT
  installed on this runner. `scripts/check.sh` was not executed here; installing `requirements.txt`
  and running the fast gate are the next session's first substantive steps.
- No golden/data baseline re-pinned, no verification output committed, no new research performed,
  no commit made (changes left uncommitted pending explicit direction).
