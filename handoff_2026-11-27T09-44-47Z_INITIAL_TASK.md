# Durable Handoff — Initial Task Message

**Created:** 2026-11-27T17:37:59Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Working directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Initial task for next session

No specific task was assigned in this session beyond creating this durable handoff. The next agentic session should:

1. Read `AGENTS.md` (baseline integrity, reproducibility, cache coverage invariant).
2. Confirm the repo is clean: `git status` — no half-finished verification run left in `experiments/`.
3. If a verification run was interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only`.
4. Then pick up the next research/engineering task from the user.

## Key conventions

- Always run with `SEED=42`.
- `experiments/*.json` are canonical goldens — never commit verification output.
- Cache coverage is enforced: every `data.download()` call site must have a pinned, git-tracked cache entry (ledger `data_baseline.json`).
- Run `python3 -m py_compile` on any changed Python file.
- `cvxpy`/`cvxopt` optional; optimizer falls back to `scipy.optimize`.
