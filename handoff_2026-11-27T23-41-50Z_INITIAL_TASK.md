# Durable Handoff — Initial Task Message

**Created:** 2026-11-27T23:41:50Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** main — 5e58e79ccf0bd3911ca4e879e8fa67e3a18f6981 (2026-11-27 23:41:50 +0000) == origin/main
**Working directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Working tree:** clean for canonical artifacts (`experiments/`, `data/`, `ledger/`); no `.verify_snapshot/` (no interrupted run pending recovery).
**Supersedes:** handoff_2026-11-27T18-39-52Z_INITIAL_TASK.md

## Initial task for next session

No specific research/engineering task was assigned in this session beyond creating this durable handoff. The next agentic session should:

1. Read `AGENTS.md` (baseline integrity, reproducibility, cache coverage invariant).
2. Confirm canonical state: `git log -1 --format="%H"`, `git status --short experiments/ data/ ledger/`; confirm HEAD == origin/main and no `.verify_snapshot/`.
3. Confirm goldens match the pinned baseline: `python3 scripts/check_goldens_clean.py` and `python3 scripts/check_golden_baseline.py`.
4. If a verification run was interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout <pinned-commit> -- experiments/<file>`).
5. Read `ledger/RESEARCH_LEDGER.md` for surviving validated strategies and open items (research phase closed, E001–E043).
6. Optionally run `SEED=42 bash scripts/check.sh` (or `make check`) to confirm goldens + data coverage + JSON guards are green — only if the user directs it.
7. Then pick up the next research/engineering task from the user. If this session itself hands off, create its own timestamped durable handoff following the established pattern (`handoff_YYYY-MM-DDTHH-MM-SSZ_INITIAL_TASK.md` at repo root) and update the `handoff_LATEST` symlink and `.handoff.md` pointer.

Do **not** re-run the full verification suite, modify `experiments/`, or change baselines without explicit direction. Do **not** invent new tasks, create additional handoffs unprompted, or re-open closed items (E049/E050 optimizer determinism + exact KKT enumeration; E041/E042 ill-conditioned QP drift — all closed, artifacts reproduce 0 diffs).

## Key conventions

- Always run with `SEED=42`. Close-to-close is the v1.2.3 primary convention.
- `experiments/*.json` are canonical goldens — never commit verification output over them; never leave a run half-finished.
- Golden baseline enforced by `scripts/check_golden_baseline.py` vs `ledger/golden_baseline.json`; data coverage by `scripts/check_data_coverage.py` vs `ledger/data_baseline.json`.
- Cache coverage is enforced: every `data.download()` call site must have a pinned, git-tracked cache entry; `QUANT_RESEARCH_OFFLINE=1` enforced during verification.
- Optimizer: validate on problem constraints, not solver exit status (see `tests/test_portfolio_opt.py`, ledger E049/E050).
- Run `python3 -m py_compile` on any changed Python file.
- `cvxpy`/`cvxopt` optional; optimizer falls back to `scipy.optimize`.
- CI workflow cannot be created by automated agents. Use local `make check/verify/*`.
- E050 exact KKT active-set solver (commit `72dc947`) made E041/E042 bit-reproducible; do not re-pin to silence a tolerance violation — none remains.

## Handoff provenance

Supersedes previous INITIAL_TASK handoff `handoff_2026-11-27T18-39-52Z_INITIAL_TASK.md`. This file is the authoritative initial-task message for the next session.

Handoff written by agent at 2026-11-27T23:41:50Z.
" filePath">
/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted/handoff_2026-11-27T23-41-50Z_INITIAL_TASK.md