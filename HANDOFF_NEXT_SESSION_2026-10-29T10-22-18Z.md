# HANDOFF – Next Session (2026-10-29T10:22:18Z)

## Context
- Repo: Quantitative-Trading-Public-Research-Prompted
- Branch/state: Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`
- Environment: Linux, git repo, SEED=42 convention, offline/cache constraints enforced

## Initial Task for Next Agent (clear, actionable)
Execute in order:

1. **Check repo cleanliness**
   ```bash
   git status --short
   ```
   Ensure no uncommitted changes to `experiments/`. If there are, recover first (step 2).

2. **Baseline integrity (must pass before any changes)**
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   - If it reports a golden mismatch vs HEAD or stale snapshot: `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`) and re-run `scripts/check.sh`.
   - Do **not** re-pin goldens to silence drift. If pins are out of sync with intent, use `scripts/check_golden_baseline.py --update` only with explicit justification.
   - If `.verify_snapshot/ACTIVE.json` exists and no live run is active, follow recovery procedure from AGENTS.md.

3. **Quick verification (establish clean baseline)**
   ```bash
   SEED=42 python3 run_all_verification.py
   ```
   (or `make verify-quick`)
   Must complete fully and restore goldens. If interrupted, do **not** commit — run `--restore-only`.

4. **Orient to open work**
   - Read `ledger/RESEARCH_LEDGER.md` (focus on **E049** – optimizer determinism / numeric drift on ill-conditioned tangency QP)
   - Read `AGENTS.md` (Baseline Integrity, Reproducibility, Gotchas)
   - Only proceed with new work if explicitly requested. Numeric drift in E041/E042 is expected and must not be "fixed" by re-pinning.

## Key Files to Read First
- `AGENTS.md` – commands, conventions, guards
- `ledger/RESEARCH_LEDGER.md` – experiment dispositions and open items
- `run_all_verification.py` – verification flow and guards
- `scripts/check.sh` – full check sequence
- `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py` – guards

## Gotchas / Constraints
- Always use `SEED=42`
- Never leave a verification run half-finished (`.verify_snapshot/` guarded)
- `check_golden_baseline.py` enforces SHA-256 pins in `ledger/golden_baseline.json`
- `check_data_coverage.py` enforces cache coverage; verification runs with `QUANT_RESEARCH_OFFLINE=1`
- Optimizer ill-conditioning causes bounded numeric drift (E041/E042) – do not re-pin
- CI workflow cannot be created by agents (template in `.github/workflow-templates/`)

## Handoff Notes
- Supersedes `HANDOFF_NEXT_SESSION_2026-10-29T10-21-57Z.md`
- Symlinks `HANDOFF.md`, `HANDOFF_CURRENT.md`, `HANDOFF_NEXT.md`, `HANDOFF_NEXT_SESSION.md` updated to point here

(End of file)
