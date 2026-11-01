# DURABLE HANDOFF — Next Agentic Session

**Timestamp (UTC):**
**Repo:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Branch:** main
**State:** Research phase complete (E001–E043). Canonical goldens in experiments/, ledger in ledger/RESEARCH_LEDGER.md.

## Initial task for next session

> **START HERE:** Confirm the clean baseline is still clean, then address the standing E049 open item (tangency QP ill-conditioning) so E041/E042 grid artifacts reproduce within tolerance — without reintroducing solver-status dependence and without re-pinning goldens to silence drift.

1. pip install -r requirements.txt if the environment was reset.
2. SEED=42 bash scripts/check.sh — expect EXIT 0 with "=== All checks passed ===".
3. git status --short — confirm working tree clean. Do NOT commit verification output. If a verification run was interrupted, recover with SEED=42 python3 run_all_verification.py --restore-only.
4. Only after steps 1–3 pass cleanly, address the standing open item below.

## Current state

- Phase: Research complete (E001–E043). Surviving validated strategies documented in ledger/RESEARCH_LEDGER.md (last entries E044–E049).
- Baselines: experiments/*.json are canonical goldens, pinned by ledger/golden_baseline.json and ledger/data_baseline.json.
- Known reproducible offline: E029, E030 (run with QUANT_RESEARCH_OFFLINE=1).
- Open item (highest value): tangency QP in src/portfolio_opt.py max_sharpe branch remains ill-conditioned (SLSQP at ftol=1e-12); 1-ulp covariance perturbations move OOS Sharpe by up to 3e-02. E041/E042 sensitivity grid and E042-primary artifacts still drift vs goldens by 29–133 diffs. **Do not re-pin to silence.** Route max_sharpe through exact_qp/exact_tangency_kkt active-set enumeration, fix the y0 = w_feas / max(mu_s'w_feas, 1e-12) start point, then re-pin affected artifacts deliberately with python3 scripts/check_golden_baseline.py --update, recording the change in the ledger.

## Constraints

- Never commit verification output. Restore goldens first if interrupted (SEED=42 python3 run_all_verification.py --restore-only).
- Never re-pin goldens to silence drift.
- Run python3 -m py_compile on changed files.
- Always use SEED=42.
- Honor pinned cache vintages (data/vintages.json, fundamentals pins in data/fundamentals/).
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or validated constructions.
- CI workflow creation is maintainer-gated (template at .github/workflow-templates/verification-gate.yml).

## Quick references

- make check | make verify-quick | make verify-extended | make verify-full
- Ledger: ledger/RESEARCH_LEDGER.md
- AGENTS.md — full commands & conventions
