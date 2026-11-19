# Agentic Work Session Handoff — Initial Task

**Timestamp**: 2026-11-19T11:57:01Z
**HEAD at write time**: `d44b888598d3f21cf0fda0f7fdb9a7e1a3cad606` (== `origin/main`, branch `main`)
**Working Directory**: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Supersedes**: `handoff_2026-11-19T11-07-34Z_INITIAL_TASK.md` (content only; no history is altered).

## Initial task for the next session

No research task is open and no code change was requested. The repository is **closed** (research E001–E043 complete; surviving strategies in `ledger/RESEARCH_LEDGER.md`). Your job is to confirm that state, leave the baseline untouched, and then wait for an explicit instruction. Do these in order:

1. **Orient.** `git log -1 --format='%H %ci %s'` and `git status --short --branch`. Expect a clean tree on `main` in sync with `origin/main`. Ignore gitignored `__pycache__/` artifacts; never commit them.
2. **Confirm no interrupted verification run.** `.verify_snapshot/` must be absent. If it exists: check `ACTIVE.json` for a live pid; recover with `SEED=42 python3 run_all_verification.py --restore-only`.
3. **Confirm the goldens were not contaminated.** `scripts/check_goldens_clean.py` (working tree vs `HEAD`) and `scripts/check_golden_baseline.py` (vs the SHA-256 pins in `ledger/golden_baseline.json`) must both pass. `git diff --name-only HEAD -- experiments/` must be empty and `git ls-files experiments/` must list 138 artifacts.
4. **Prepare the environment.** `pip install -r requirements.txt`. This runner has Python 3.12.3 and **no numpy/pandas/scipy** in the bare interpreter, so the gate cannot pass before installing.
5. **Run the fast gate.** `SEED=42 bash scripts/check.sh` (seconds, offline). Only escalate to `run_all_verification.py` / `--extended` / `--full` if asked.
6. **Await direction.** Do not start new research, do not re-pin a baseline, and do not "fix" the E041/E042 numeric drift by re-pinning.
7. **Before ending your session**, leave your own timestamped handoff using the procedure at the bottom of this file, and add a ledger entry for it.

## Verified state at write time

- `git status --short --branch` → `## main...origin/main` (clean apart from gitignored `__pycache__/` .pyc mods).
- `git rev-parse HEAD` == `git rev-parse origin/main` == `d44b8885…`.
- `git diff --name-only HEAD -- experiments/` → empty (0 files).
- `git ls-files experiments/` → 138 canonical golden artifacts.
- `.verify_snapshot/` and `.verify_reports/` absent → nothing to recover.
- `ledger/golden_baseline.json` and `ledger/data_baseline.json` present and parse.

## Guardrails (non-negotiable)

1. **The committed golden is authoritative.** `experiments/*.json` are canonical research artifacts. The verification suite backs them up and restores them; a half-finished run must be recovered, not committed.
2. **Never commit verification output.** A checkpoint commit that captures a live run silently replaces the baseline. Restore first.
3. **Do not re-pin to silence drift.** E041/E042 grid artifacts drift by 29–133 differences from 1-ulp sensitivity of an ill-conditioned QP. Re-pinning is forbidden.
4. **Data coverage is an invariant.** Every `data.download()` input must exist, be git-tracked, and match `ledger/data_baseline.json`. Adding an input means committing the file and re-pinning with `scripts/check_data_coverage.py --update`.
5. **Seed is always `SEED=42`.** Walk-forward and placebo RNG depend on it.
6. **CI workflows cannot be created by agents.** `.github/scripts/kilo-controller.sh` reverts `.github/workflows/`, and the token lacks `workflows` push permission. Use the maintainer template `.github/workflow-templates/verification-gate.yml`.
7. **Pre-registration is binding.** Gates, falsification expectations, and sensitivity grids are fixed before execution; goalposts are never moved.

## Command reference

```bash
SEED=42 bash scripts/check.sh                                   # fast gate, seconds, offline
SEED=42 python3 run_all_verification.py                         # quick, ~8 min
SEED=42 python3 run_all_verification.py --extended              # ~21 min, 26 drivers
SEED=42 python3 run_all_verification.py --full                  # E042 n_sim=50 + 96-config grid
SEED=42 python3 run_all_verification.py --skip-slow             # convention only
SEED=42 python3 run_all_verification.py --restore-only          # recover after interruption
SEED=42 python3 verify_convention_robustness.py                 # reads JSONs, no writes
python3 scripts/check_goldens_clean.py                          # tree vs HEAD
python3 scripts/check_golden_baseline.py                        # tree vs pinned SHA-256
python3 scripts/check_data_coverage.py                          # data invariant
```

## Where things live

- `AGENTS.md` — full project conventions, verification scope, reproducibility rules.
- `ledger/RESEARCH_LEDGER.md` — every experiment disposition and open item.
- `ledger/PRIORITIZATION.md` — surviving-strategy priorities.
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints.
- `experiments/` — 138 canonical golden JSONs; drivers `run_e0NN.py`.
- `src/` — backtest engine, portfolio optimizer, data/fundamentals access.
- `tests/` — `test_portfolio_opt.py` pins the solver-validation rule.

## Recurring handoff procedure

1. Write `handoff_<UTC>_INITIAL_TASK.md` at the repo root. Use `date -u +%Y-%m-%dT%H-%M-%SZ` for the name and an ISO second-precision timestamp in the body.
2. Mirror it byte-identically into `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, and `.kilo/handoff/` and confirm all six SHA-256 digests match.
3. Repoint the generic pointers: `python3 scripts/repoint_handoff.py <new-file>`. Expect `generic pointers found: 18 repointed: 18` and `checked=18 bad=0`. Timestamped historical files are intentionally left untouched.
4. Append a ledger entry (`## E533: …`) recording HEAD, the six-copy SHA-256, the verification checks you ran, and the constraints honored.
5. Do not commit unless the user explicitly asks.
