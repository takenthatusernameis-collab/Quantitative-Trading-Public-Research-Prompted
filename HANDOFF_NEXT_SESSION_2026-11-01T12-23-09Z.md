# DURABLE HANDOFF — Next Agentic Session

**Timestamp (UTC):** 2026-11-01T12:23:09Z
**Repo:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Branch:** main @ `14b5f38` (chore(kilo): checkpoint agent session)
**State:** Research phase complete (E001–E043). Canonical goldens in `experiments/`, ledger in `ledger/RESEARCH_LEDGER.md`.

## Initial task for next session

1. `pip install -r requirements.txt` if the environment was reset.
2. **Recover the stale verification snapshot.** `.verify_snapshot/ACTIVE.json` exists owning pid 37032 (dead — interrupted ~2026-11-01T11:25Z). The working-tree `experiments/*.json` already match HEAD (verified: `git diff --name-status HEAD -- experiments/` is empty), but the pending marker will fail `scripts/check_goldens_clean.py`. Run:
   ```
   SEED=42 python3 run_all_verification.py --restore-only
   ```
   (equivalently `git checkout -- experiments/` plus remove `.verify_snapshot/`). This clears the marker and restores canonical goldens before anything else.
3. `SEED=42 bash scripts/check.sh` — expect EXIT 0 with `=== All checks passed ===`. This includes `check_goldens_clean.py` (fails if `experiments/` differs from HEAD or a stale snapshot is pending) and `check_golden_baseline.py`.
4. `git status --short` — confirm only `__pycache__/*.pyc` modifications remain (15 tracked pyc files; ignore them). Do NOT commit verification output.
5. Only after steps 1–4 pass cleanly, address the standing open item below. Do not re-pin goldens to silence drift.

## Standing open item (highest value)

**E049 tangency QP ill-conditioning** (`src/portfolio_opt.py`, `max_sharpe` branch). The SLSQP tangency QP at `ftol=1e-12` is chaotically ill-conditioned: a 1-ulp covariance perturbation moves OOS Sharpe by up to 3e-02. E041/E042 sensitivity-grid and E042-primary artifacts still drift vs their goldens by 29–133 numeric diffs (down from 360–9273 after the E049 exit-status fix).

Do NOT re-pin to silence. The intended fix is a *research-engineering* change:
- Route `max_sharpe` through `exact_qp` / `exact_tangency_kkt` active-set enumeration (for N ≤ 5 this is feasible and was used as the reference oracle in E049).
- Fix the `y0 = w_feas / max(mu_s'w_feas, 1e-12)` start point at `src/portfolio_opt.py:253`, which masks a negative denominator; at the 2019-10-16 rebalance it yields magnitude 8.1e+11 and violates `mu'y = 1` by 6.4e+09. A correct start point (a max-`mu_s'w` LP on the feasible simplex) makes SLSQP converge to the exact optimum there and **will change published numbers** — so it belongs to a deliberate re-pin, not a silent fix.
- After the fix, re-run the affected drivers (`experiments/run_e041.py`, `experiments/run_e042.py --n-sim ...`, `experiments/run_e042_lead.py`) and re-pin deliberately with `python3 scripts/check_golden_baseline.py --update`, recording the change in the ledger.

## Constraints

- Always use `SEED=42`.
- Honor pinned cache vintages (`data/vintages.json`, fundamentals pins in `data/fundamentals/` per `data/fundamentals_vintages.json`). Verification runs with `QUANT_RESEARCH_OFFLINE=1`.
- Never leave a verification run half-finished (the `.verify_snapshot/` crash-safe marker exists precisely for this).
- Do not commit verification outputs; only intentional source/data changes.
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or validated constructions.
- CI workflow creation is maintainer-gated (template at `.github/workflow-templates/verification-gate.yml`).

## Quick references

- `make check` | `make verify-quick` | `make verify-extended` | `make verify-full`
- `SEED=42 python3 run_all_verification.py [--extended|--full|--skip-slow|--restore-only]`
- Ledger: `ledger/RESEARCH_LEDGER.md` (E049 entry at line 4805; E041/E042 entries follow)
- AGENTS.md — full commands, reproducibility, and baseline-integrity conventions

## Durable links

- `handoff.md` → this file (latest)
- `handoff_next_session.md` → this file
- `handoff_current.md` → this file
- `HANDOFF_NEXT_SESSION_LATEST.md` → this file

(End of file)