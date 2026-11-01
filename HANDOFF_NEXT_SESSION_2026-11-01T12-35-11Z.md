# DURABLE HANDOFF — Next Agentic Session

**Timestamp (UTC):** 2026-11-01T12-35-11Z
**Repo:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Branch:** main @ `6b4796d` (chore(kilo): checkpoint agent session)
**State:** Research phase complete (E001–E043). Canonical goldens in `experiments/`, ledger in `ledger/RESEARCH_LEDGER.md`.

## Initial task for next session

1. `pip install -r requirements.txt` if the environment was reset.
2. `SEED=42 bash scripts/check.sh` — expect EXIT 0 with `=== All checks passed ===`.
3. `git status --short` — confirm only `__pycache__/*.pyc` modifications remain. Do NOT commit verification output.
4. Only after steps 1–3 pass cleanly, address the standing open item below. Do not re-pin goldens to silence drift.

## Baseline-integrity note (carried forward)

The interrupted-run recovery (`SEED=42 python3 run_all_verification.py --restore-only`) cleared the stale `.verify_snapshot/` marker. The working tree differs from HEAD on exactly **3** `experiments/*.json` files by ~1e-16 (`corr_spy` last-significant-digit drift):

- `experiments/cointegration_large_liquid.json`
- `experiments/dollar_neutral_lowbeta_large_liquid.json`
- `experiments/pairs_large_liquid.json`

This is expected and correct, not a defect:

- `python3 scripts/check_goldens_clean.py` → **FAIL 3** (compares worktree vs HEAD).
- `python3 scripts/check_golden_baseline.py` → **ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT** (compares worktree vs `ledger/golden_baseline.json`).

The worktree matches the pinned baseline for all 107 artifacts; the 3 mismatches are HEAD-only. The pinned baseline is the authoritative record. **Do not `git checkout -- experiments/`** — that would break `check_golden_baseline.py`.

## Standing open item (highest value)

**E049 tangency QP ill-conditioning** (`src/portfolio_opt.py`, `max_sharpe` branch). SLSQP at `ftol=1e-12` is chaotically ill-conditioned: a 1-ulp covariance perturbation moves OOS Sharpe by up to 3e-02. E041/E042 artifacts still drift vs goldens by 29–133 numeric diffs (down from 360–9273 after the E049 exit-status fix).

Do NOT re-pin to silence. Intended fix:

- Route `max_sharpe` through `exact_qp` / `exact_tangency_kkt` active-set enumeration (N ≤ 5 feasible; reference oracle used in E049).
- Fix the `y0 = w_feas / max(mu_s'w_feas, 1e-12)` start point at `src/portfolio_opt.py:253`, which masks a negative denominator; at the 2019-10-16 rebalance it yields magnitude 8.1e+11 and violates `mu'y = 1` by 6.4e+09. A correct start point makes SLSQP converge to the exact optimum there and **will change published numbers** — so it belongs to a deliberate re-pin.
- After the fix, re-run `experiments/run_e041.py`, `experiments/run_e042.py --n-sim ...`, `experiments/run_e042_lead.py`, and re-pin deliberately with `python3 scripts/check_golden_baseline.py --update`, recording the change in the ledger.

## Constraints

- Always use `SEED=42`.
- Honor pinned cache vintages (`data/vintages.json`, fundamentals pins per `data/fundamentals_vintages.json`). Verification runs with `QUANT_RESEARCH_OFFLINE=1`.
- Never leave a verification run half-finished (`.verify_snapshot/` crash-safe marker).
- Do not commit verification outputs; only intentional source/data changes.
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or validated constructions.
- CI workflow creation is maintainer-gated (template at `.github/workflow-templates/verification-gate.yml`).

## Quick references

- `make check` | `make verify-quick` | `make verify-extended` | `make verify-full`
- `SEED=42 python3 run_all_verification.py [--extended|--full|--skip-slow|--restore-only]`
- Ledger: `ledger/RESEARCH_LEDGER.md` (E049 entry; E041/E042 entries follow)
- AGENTS.md — full commands, reproducibility, baseline-integrity conventions

## Durable links

- `handoff.md` → this file (latest)
- `handoff_next_session.md` → this file
- `handoff_current.md` → this file
- `handoff_next.md` → this file
- `HANDOFF_NEXT_SESSION_LATEST.md` → this file
