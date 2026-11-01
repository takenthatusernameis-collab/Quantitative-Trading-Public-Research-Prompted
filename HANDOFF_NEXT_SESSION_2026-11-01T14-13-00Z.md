# DURABLE HANDOFF — Next Agentic Session

**Timestamp (UTC):** 2026-11-01T14-13-00Z
**Repo:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Branch:** main
**State:** Research phase complete (E001–E043). Canonical goldens in `experiments/`, ledger in `ledger/RESEARCH_LEDGER.md`. Working tree clean. No live verification snapshot.

## Initial task message for the next agentic work session

> **START HERE:** Run the baseline verification first. If clean, tackle the standing E049 open item (tangency QP ill-conditioning) without re-pinning goldens to silence drift.

**Steps (in order):**
1. Verify environment: `pip install -r requirements.txt` if needed.
2. Run convention check: `SEED=42 bash scripts/check.sh` — must exit 0 (`=== All checks passed ===`).
3. Confirm clean state: `git status --short` — working tree must be clean. Do NOT commit verification output.
4. If steps 1–3 pass, address E049: fix `src/portfolio_opt.py` `max_sharpe` path to avoid solver-status dependence and use a stable tangency/QP formulation (route via exact KKT/active-set enumeration as noted in ledger). Fix start point at `y0 = w_feas / max(mu_s'w_feas, 1e-12)` if needed.
5. Reproduce affected artifacts: run `experiments/run_e041.py`, `experiments/run_e042.py`, `experiments/run_e042_lead.py`. Verify drift decreases within numeric tolerance.
6. If fix is correct and within tolerance, re-pin deliberately with `python3 scripts/check_golden_baseline.py --update` and record the change in `ledger/RESEARCH_LEDGER.md` (E049). Do NOT re-pin to mask drift.

## Standing open item (highest value)
**E049 tangency QP ill-conditioning** — SLSQP ill-conditioned; E041/E042 grid still drift (29–133 numeric diffs). Do not silence with re-pins. See ledger ~E049 and `src/portfolio_opt.py`.

## Constraints
- Never commit verification output. If interrupted: `SEED=42 python3 run_all_verification.py --restore-only`.
- Never re-pin goldens to silence drift.
- Always use `SEED=42`. Honor pinned caches/vintages.
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or validated constructions.
- Run `python3 -m py_compile` on changed files.

## Quick refs
- `make check` | `make verify-quick` | `make verify-extended` | `make verify-full`
- `ledger/RESEARCH_LEDGER.md` (E049)
- `AGENTS.md`

(End of file)
" \
filePath="/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted/HANDOFF_NEXT_SESSION_2026-11-01T14-13-00Z.md