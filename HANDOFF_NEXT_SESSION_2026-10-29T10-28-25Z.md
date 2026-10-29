# HANDOFF – Next Session (2026-10-29T10:28:25Z)

## Context
- Repo: Quantitative-Trading-Public-Research-Prompted
- Branch/state: `main`, up to date with `origin/main`. Research phase COMPLETE (E001–E049). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md` (§E040 close-out; E049 is the last experiment).
- Working tree: clean except regenerated `__pycache__/*.pyc` bytecode (`git status` shows them as modified; not source changes — ignore or `git checkout`'d).
- Environment: Linux, git repo, SEED=42 convention, offline/cache constraints enforced (`QUANT_RESEARCH_OFFLINE=1` during verification).

## Last session summary
- Created/updated handoffs; verified repo state and last commits.
- Baseline appears stable following E049 fixes (optimizer determinism).

## Initial Task for Next Agent (clear, actionable)
Execute in order:

1. **Check repo cleanliness**
   ```bash
   git status --short
   ```
   Expect only `__pycache__/*.pyc` modifications. Ensure no uncommitted changes to `experiments/` or `src/`.

2. **Baseline integrity (must pass before any changes)**
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   - If it reports a golden mismatch vs HEAD or stale snapshot: `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`) and re-run `scripts/check.sh`.
   - Do **not** re-pin goldens to silence drift. If pins are out of sync with intent, use `scripts/check_golden_baseline.py --update` only with explicit justification.
   - If `.verify_snapshot/ACTIVE.json` exists and no live run is active, follow the recovery procedure from AGENTS.md.

3. **Quick verification (establish clean baseline)**
   ```bash
   SEED=42 python3 run_all_verification.py
   ```
   Must complete fully and restore goldens. If interrupted, do **not** commit — run `--restore-only`.

4. **Orient to open work**
   - Read `ledger/RESEARCH_LEDGER.md` (focus on **E049** optimizer determinism / numeric drift on ill-conditioned tangency QP, and **E040** close-out).
   - Read `AGENTS.md` (Baseline Integrity, Reproducibility).
   - **No mandated next research task.** Research phase is complete; proceed only when the user provides a concrete objective. Numeric drift in E041/E042 is expected and must not be "fixed" by re-pinning.

## Key Files to Read First
- `AGENTS.md`
- `ledger/RESEARCH_LEDGER.md`
- `run_all_verification.py`
- `scripts/check.sh`
- `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`

## Gotchas / Constraints
- Always use `SEED=42`
- Never leave a verification run half-finished (`.verify_snapshot/` guarded)
- `check_golden_baseline.py` enforces SHA-256 pins in `ledger/golden_baseline.json`
- `check_data_coverage.py` enforces cache coverage; verification runs with `QUANT_RESEARCH_OFFLINE=1`
- Optimizer ill-conditioning causes bounded numeric drift (E041/E042) — do not re-pin
- CI workflow cannot be created by agents (template in `.github/workflow-templates/`)

## Handoff Notes
- Supersedes `HANDOFF_NEXT_SESSION_2026-10-29T10-27-55Z.md`
- Symlinks `HANDOFF.md`, `HANDOFF_CURRENT.md`, `HANDOFF_NEXT.md`, `HANDOFF_NEXT_SESSION.md` and `.kilo/handoff.md`, `.kilo/handoff_next_session.md` updated to point here
- Initial task: run baseline integrity + quick verification, then orient; no new research task mandated

## Key commands
- `SEED=42 bash scripts/check.sh` — fast convention-robustness + template validation (~seconds, offline)
- `SEED=42 python3 run_all_verification.py` — verify-quick (~8 min)
- `SEED=42 python3 run_all_verification.py --extended` — verify-extended (~21 min)
- `SEED=42 python3 run_all_verification.py --full` — verify-full (~15 min)
- `SEED=42 python3 run_all_verification.py --restore-only` — recover goldens after interrupted run
- `python3 -m py_compile` on changed files (no separate linter)
