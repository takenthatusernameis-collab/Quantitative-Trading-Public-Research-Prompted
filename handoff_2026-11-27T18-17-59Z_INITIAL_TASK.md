# Durable Handoff — Initial Task Message

**Created:** 2026-11-27T18:17:59Z
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
- Canonical state clean (HEAD == origin/main; no `.verify_snapshot/`; no pending recovery). Before any change, read `ledger/RESEARCH_LEDGER.md`, optionally `SEED=42 bash scripts/check.sh`. Then stop and await explicit user instructions. Do not re-run verification or modify baselines unprompted.
