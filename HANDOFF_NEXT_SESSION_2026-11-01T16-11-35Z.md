# DURABLE HANDOFF — Next Agentic Session

**Timestamp (UTC):** 2026-11-01T16:11:35Z
**Repo:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Branch:** main (HEAD `05e9720`)
**State:** Research phase complete (E001–E043). Canonical goldens in `experiments/`, ledger in `ledger/RESEARCH_LEDGER.md` (E049 entry at line ~4805). Working tree clean at HEAD `05e9720`. No live verification snapshot (`.verify_snapshot/` absent) — nothing to recover. The only commits since `dfaa45c` are `d920f7c` and `05e9720`, both `chore(kilo): checkpoint agent session`, and their diffs are confined to handoff files + symlinks.

## Initial task message for the next agentic work session

> **START HERE:** Confirm the clean baseline is still clean, then address the standing E049 open item (tangency QP ill-conditioning) so E041/E042 grid artifacts reproduce within tolerance — without reintroducing solver-status dependence and without re-pinning goldens to silence drift.

1. `pip install -r requirements.txt` if the environment was reset.
2. `SEED=42 bash scripts/check.sh` — expect EXIT 0 with `=== All checks passed ===`.
3. `git status --short` — confirm working tree clean. Do NOT commit verification output.
4. Only after steps 1–3 pass cleanly, address the standing open item below. Do not re-pin goldens to silence drift.

## Standing open item (highest value)

**E049 tangency QP ill-conditioning** (`src/portfolio_opt.py`, `max_sharpe` branch, lines ~453–519). SLSQP at `ftol=1e-12` is chaotically ill-conditioned: a 1-ulp covariance perturbation moves OOS Sharpe by up to 3e-02. E041/E042 artifacts still drift vs goldens by 29–133 numeric diffs.

Do NOT re-pin to silence. Intended fix:

- Route `max_sharpe` through `exact_qp` / `exact_tangency_kkt` active-set enumeration (N ≤ 5 feasible; reference oracle used in E049). Note `exact_qp` is already wired in at `src/portfolio_opt.py:482` — the `max_sharpe` branch already calls it first and only falls back to SLSQP when `_tangency_feasible(y_kkt, ...)` is False (line 486). Verify that fallback path is actually being taken on the drifting rebalances, and if the exact KKT point is being found but then rejected by `_tangency_feasible`, tighten/fix that predicate rather than loosening it.
- Fix the `y0 = w_feas / max(mu_s'w_feas, 1e-12)` start point at `src/portfolio_opt.py:492` (ledger says `:253` — that line number is stale; the live line is 492). The `max(..., 1e-12)` guard masks a *negative* denominator: at the 2019-10-16 rebalance the initial point has magnitude 8.1e+11 and violates `mu'y = 1` by 6.4e+09, SLSQP returns garbage (objective 3.7e+20), and the feasibility check correctly rejects it so the shipped code falls back to the LP vertex exactly as the golden did. A correct start point (a max-`mu_s'w` LP on the feasible simplex) makes SLSQP converge to the exact optimum there and would **change the published numbers** — hence the same deliberate re-pin decision.
- After the fix, re-run `experiments/run_e041.py`, `experiments/run_e042.py`, `experiments/run_e042_lead.py`, and re-pin deliberately with `python3 scripts/check_golden_baseline.py --update`, recording the change in the ledger.

## Constraints

- Never commit verification output. Restore goldens first if interrupted (`SEED=42 python3 run_all_verification.py --restore-only`).
- Never re-pin goldens to silence drift.
- Run `python3 -m py_compile` on changed files.
- Always use `SEED=42`.
- Honor pinned cache vintages (`data/vintages.json`, fundamentals pins in `data/fundamentals/` per `data/fundamentals_vintages.json`).
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or validated constructions.
- CI workflow creation is maintainer-gated (template at `.github/workflow-templates/verification-gate.yml`).

## Quick references

- `make check` | `make verify-quick` | `make verify-extended` | `make verify-full`
- `SEED=42 python3 run_all_verification.py --skip-slow` | `--restore-only`
- Ledger: `ledger/RESEARCH_LEDGER.md` (E049 entry at line ~4805; E045/E046/E047/E048 precede it)
- `src/portfolio_opt.py` — `_tangency_feasible` at line 75, `exact_qp` at 116, `exact_tangency_kkt` at 273, `max_sharpe` branch 453–519, `y0` at 492
- AGENTS.md — full commands & conventions