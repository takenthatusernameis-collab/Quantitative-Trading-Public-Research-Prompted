# Initial Task Message (for next agentic session) — 2026-11-01T09:13:29Z

> **START HERE:** Confirm the clean baseline is still clean, then address the standing E049 follow-up (tangency QP ill-conditioning) so E041/E042 grid artifacts reproduce within tolerance without reintroducing solver-status dependence.
>
> **Durable handoff:** `HANDOFF_NEXT_SESSION_2026-11-01T09-13-29Z.md` (also reachable via the `handoff.md`, `handoff_next.md`, `handoff_next_session.md`, `handoff_current.md`, `HANDOFF.md`, `HANDOFF_CURRENT.md`, `HANDOFF_NEXT_SESSION.md`, and `HANDOFF_NEXT_SESSION_LATEST.md` symlinks).

## Next Task

1. `pip install -r requirements.txt` if the environment was reset.
2. `SEED=42 bash scripts/check.sh` — expect EXIT 0 with "=== All checks passed ===".
3. `git status --short` — confirm only `__pycache__/*.pyc` modifications remain. If a verification run was interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only`.
4. Only after steps 1–3 pass cleanly, address the open item below.

## Context

This session (handoff written 2026-11-01T09:13:29Z) leaves a durable initial task message for the next agentic work session.

- HEAD `ef2591a` (chore(kilo): checkpoint agent session), branch `main`.
- Working tree clean except `__pycache__/*.pyc` (15 tracked pyc modifications; ignore them).
- No live verification snapshot (`.verify_snapshot/` absent, no `ACTIVE.json`). No run is in progress; nothing to recover.
- Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Open item (highest value)

Tangency QP in `src/portfolio_opt.py` `max_sharpe` branch still ill-conditioned (SLSQP at `ftol=1e-12`); 1-ulp covariance perturbations move OOS Sharpe by up to 3e-02. E041/E042 sensitivity grid and E042-primary artifacts still drift vs goldens by 29–133 diffs. **Do not re-pin to silence.** Route `max_sharpe` through `exact_qp`/`exact_tangency_kkt` active-set enumeration, fix the `y0 = w_feas / max(mu_s'w_feas, 1e-12)` start point, then re-pin affected artifacts deliberately. See `ledger/RESEARCH_LEDGER.md` E049.

## Constraints

- Always use `SEED=42`.
- Honor pinned cache vintages (`data/vintages.json`, fundamentals pins in `data/fundamentals/`).
- Never leave a verification run half-finished.
- Do not commit verification outputs; only intentional source/data changes.
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or validated constructions.
- CI workflow creation is maintainer-gated (template at `.github/workflow-templates/verification-gate.yml`).

## Quick references

- `make check` | `make verify-quick` | `make verify-extended` | `make verify-full`
- Ledger: `ledger/RESEARCH_LEDGER.md`
- AGENTS.md — full commands & conventions
