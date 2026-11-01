# DURABLE HANDOFF — Next Agentic Session

**Timestamp (UTC):** 2026-11-01T11-34-08Z
**Repo:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Branch:** main @ HEAD (checkpoint commit)
**State:** Research phase complete (E001–E043). Canonical goldens in `experiments/`, ledger in `ledger/RESEARCH_LEDGER.md`.

## Initial task for next session

Confirm the clean baseline is still clean, then address the standing E049 follow-up (tangency QP ill-conditioning) so E041/E042 grid artifacts reproduce within tolerance without reintroducing solver-status dependence.

1. `pip install -r requirements.txt` if the environment was reset.
2. `SEED=42 bash scripts/check.sh` — expect EXIT 0 with "=== All checks passed ===".
3. `git status --short` — confirm only `__pycache__/*.pyc` modifications remain. If a verification run was interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only`.
4. Only after steps 1–3 pass cleanly, address the open item below.

## Current state

- **Phase:** Research complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md` (last entries E044–E049).
- **HEAD:** checkpoint commit, branch `main`, up to date with `origin/main`.
- **Working tree:** clean except `__pycache__/*.pyc` recompilations (binary-only, no source changes).
- **Baselines:** `experiments/*.json` are canonical goldens, pinned by `ledger/golden_baseline.json` and `ledger/data_baseline.json`.
- **Snapshot state:** `.verify_snapshot/` does **NOT** exist — no recovery needed.
- **Open item (highest value):** tangency QP in `src/portfolio_opt.py` `max_sharpe` branch still ill-conditioned (SLSQP at `ftol=1e-12`); 1-ulp covariance perturbations move OOS Sharpe by up to 3e-02. E041/E042 sensitivity grid and E042-primary artifacts still drift vs goldens by 29–133 diffs. **Do not re-pin to silence.** Route `max_sharpe` through `exact_qp`/`exact_tangency_kkt` active-set enumeration, fix the `y0 = w_feas / max(mu_s'w_feas, 1e-12)` start point (`src/portfolio_opt.py:492`), then re-pin affected artifacts deliberately. See `ledger/RESEARCH_LEDGER.md` E049.
- **Known reproducible offline:** E029, E030. Run drivers with `QUANT_RESEARCH_OFFLINE=1`.
- **Recovery:** `SEED=42 python3 run_all_verification.py --restore-only`.
- **Caveat:** stale `HANDOFF_*.md` files are tracked in git. Do not commit handoffs; the controller checkpoints already cover that.

## Quick references

- `make check` | `make verify-quick` | `make verify-extended` | `make verify-full`
- Ledger: `ledger/RESEARCH_LEDGER.md`
- AGENTS.md — full commands & conventions

(End of file)
