# HANDOFF – Next Session (2026-10-29T10:32:40Z)

## Context
- Repo: Quantitative-Trading-Public-Research-Prompted
- Branch/state: `main`, up to date with `origin/main`. Research phase COMPLETE (E001–E049). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- Working tree: clean except regenerated `__pycache__/*.pyc` bytecode (ignore or `git checkout`).
- Environment: Linux, SEED=42 convention, offline/cache constraints enforced (`QUANT_RESEARCH_OFFLINE=1` during verification).

## Clear initial task for next agent (do this first, in order)

1. **Check repo cleanliness**
   ```bash
   git status --short
   ```
   Expect only `__pycache__/*.pyc` modifications.

2. **Baseline integrity (must pass before any changes)**
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   - If golden mismatch or stale snapshot: `SEED=42 python3 run_all_verification.py --restore-only` then re-run check.
   - Do not re-pin goldens to silence drift; use `scripts/check_golden_baseline.py --update` only with explicit justification.
   - If `.verify_snapshot/ACTIVE.json` exists with no live run, follow recovery procedure in AGENTS.md.

3. **Quick verification (establish clean baseline)**
   ```bash
   SEED=42 python3 run_all_verification.py
   ```
   Must complete fully and restore goldens. If interrupted, run `--restore-only`; do not commit.

4. **Orient to open work**
   - Read `AGENTS.md` (Baseline Integrity, Reproducibility).
   - Read `ledger/RESEARCH_LEDGER.md` (focus on E049 optimizer determinism / ill-conditioned tangency QP numeric drift, and E040 close-out).
   - No mandated next research task; research phase complete. Proceed only when user provides a concrete objective. Numeric drift in E041/E042 is expected — do not re-pin.

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
- Supersedes `HANDOFF_NEXT_SESSION_2026-10-29T10-31-42Z.md`
- Symlinks `HANDOFF.md`, `HANDOFF_CURRENT.md`, `HANDOFF_NEXT.md`, `HANDOFF_NEXT_SESSION.md` and `.kilo/handoff.md`, `.kilo/handoff_next_session.md` updated to point here
- Initial task: run baseline integrity + quick verification, then orient; no new research task mandated
