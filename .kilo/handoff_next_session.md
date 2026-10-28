# Durable Handoff — Next Agentic Work Session

**Timestamp:** 2026-10-28T23:02:14Z
**Session status:** clean working tree (no uncommitted changes). Last commits were `chore(kilo): checkpoint agent session`. No task assigned yet — awaiting user instruction.

## Repo
Path: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

Independent reproducible quantitative-strategy research (2014–2026 US equities, futures, macro). Research phase complete (E001–E043). Surviving strategies documented in `ledger/RESEARCH_LEDGER.md`. Committed artifacts live in `experiments/*.json` (canonical baselines, pinned in `ledger/golden_baseline.json`).

## Key commands (from AGENTS.md)
- `SEED=42 bash scripts/check.sh` — fast convention-robustness + template validation (~seconds, offline)
- `SEED=42 python3 run_all_verification.py` — verify-quick (~8 min; 8 drivers E012/E023/E024/E027/E035/E037/E039/E042-lead)
- `SEED=42 python3 run_all_verification.py --extended` — verify-extended (~21 min)
- `SEED=42 python3 run_all_verification.py --full` — verify-full (~15 min)
- `SEED=42 python3 run_all_verification.py --restore-only` — recover goldens after interrupted run
- `python3 -m py_compile` on changed files (no separate linter)

## Baseline integrity (critical)
- `experiments/*.json` are overwritten by verification runs and restored afterwards — never leave a run half-finished; never commit verification output.
- `scripts/check_goldens_clean.py` fails if a tracked artifact under `experiments/` differs from HEAD or a stale snapshot is pending.
- `scripts/check_golden_baseline.py` compares every `experiments/` artifact to the SHA-256 pinned in `ledger/golden_baseline.json`. Replacing an artifact requires `--update`.
- `scripts/check_data_coverage.py` requires every `data.download()` cache file to exist, be git-tracked, and match `ledger/data_baseline.json` (runs offline with `QUANT_RESEARCH_OFFLINE=1`).
- `cvxpy`/`cvxopt` optional; portfolio optimizer falls back to `scipy.optimize`.

## Clear initial task message for next session
**TASK:** Awaiting user instruction. Start with AGENTS.md; run `SEED=42 bash scripts/check.sh` to establish a clean baseline state before making changes. If the user provides a specific objective, read relevant drivers/tests, make minimal changes, run `python3 -m py_compile` on modified files, and run the appropriate verification (`check`/`verify-quick`/`verify-extended`) as needed. Do not commit or modify golden artifacts without explicit user request; use `run_all_verification.py --restore-only` if experiments/ are dirty from a prior interrupted run.

## Next-step guidance
1. Read AGENTS.md conventions and the relevant driver/test files.
2. Implement, then run `python3 -m py_compile` on changed files.
3. Run the applicable verification step (`make check` / `make verify-quick` / extended) before declaring done.
4. Do not commit unless explicitly asked; restore goldens if verification wrote to `experiments/`.

(End of file)
