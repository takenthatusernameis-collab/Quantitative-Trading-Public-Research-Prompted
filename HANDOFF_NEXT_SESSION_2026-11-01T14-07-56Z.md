# DURABLE HANDOFF — Next Agentic Session

**Timestamp (UTC):** 2026-11-01T14:09:45Z
**Repo:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Branch:** main (HEAD `b4042eb` — `chore(kilo): checkpoint agent session`)
**State:** Research phase complete (E001–E043). Canonical goldens in `experiments/`, ledger in `ledger/RESEARCH_LEDGER.md`. Working tree clean at HEAD `b4042eb`. No live verification snapshot (`.verify_snapshot/` absent) — nothing to recover.

## Initial task message for the next agentic work session

> **START HERE:** Confirm the clean baseline is still clean, then address the standing E049 open item (tangency QP ill-conditioning) so E041/E042 grid artifacts reproduce within tolerance — without reintroducing solver-status dependence and without re-pinning goldens to silence drift.

1. `pip install -r requirements.txt` if the environment was reset.
2. `SEED=42 bash scripts/check.sh` — expect EXIT 0 with `=== All checks passed ===`.
3. `git status --short` — confirm working tree clean. Do NOT commit verification output.
4. Only after steps 1–3 pass cleanly, address the standing open item below. Do not re-pin goldens to silence drift.

## Standing open item (highest value)

**E049 tangency QP ill-conditioning** (`src/portfolio_opt.py`, `max_sharpe` branch). SLSQP at `ftol=1e-12` is chaotically ill-conditioned: a 1-ulp covariance perturbation moves OOS Sharpe by up to 3e-02. E041/E042 artifacts still drift vs goldens by 29–133 numeric diffs.

Do NOT re-pin to silence. Intended fix:

- Route `max_sharpe` through `exact_qp` / `exact_tangency_kkt` active-set enumeration (N ≤ 5 feasible; reference oracle used in E049).
- Fix the `y0 = w_feas / max(mu_s'w_feas, 1e-12)` start point at `src/portfolio_opt.py:253`.
- After the fix, re-run `experiments/run_e041.py`, `experiments/run_e042.py`, `experiments/run_e042_lead.py`, and re-pin deliberately with `python3 scripts/check_golden_baseline.py --update`, recording the change in the ledger.

## Constraints

- Never commit verification output. Restore goldens first if interrupted (`SEED=42 python3 run_all_verification.py --restore-only`).
- Never re-pin goldens to silence drift.
- Run `python3 -m py_compile` on changed files.
- Always use `SEED=42`.
- Honor pinned cache vintages (`data/vintages.json`, fundamentals pins in `data/fundamentals/`).
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or validated constructions.
- CI workflow creation is maintainer-gated (template at `.github/workflow-templates/verification-gate.yml`).

## Quick references

- `make check` | `make verify-quick` | `make verify-extended` | `make verify-full`
- Ledger: `ledger/RESEARCH_LEDGER.md` (E049 entry at line ~4805)
- AGENTS.md — full commands & conventions
- Durable initial task: `.handoff/20261101T140945Z_INITIAL_TASK.md`
