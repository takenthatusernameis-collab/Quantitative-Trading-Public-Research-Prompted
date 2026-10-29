# HANDOFF – Next Session (2026-10-29T10:21:57Z)

## Context
- Repo: Quantitative-Trading-Public-Research-Prompted
- Branch/state: Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`
- Environment: Linux, git repo, SEED=42 convention, offline/cache constraints

## Current State (as of this handoff)
- Verification harness and golden baseline guards are in place (`scripts/check.sh`, `run_all_verification.py`, `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`)
- Canonical artifacts live in `experiments/*.json` (goldens). Never modify them via ad-hoc runs — use restore if interrupted.
- Known open items: E049 (optimizer determinism / numeric drift on ill-conditioned tangency QP; E041/E042 still show bounded numeric differences). See `ledger/RESEARCH_LEDGER.md`.

## Initial Task for Next Agent (clear, actionable)
1. **Baseline integrity** (must pass before any changes)
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   If it reports a golden mismatch or stale snapshot, recover: `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/` and re-check). Do not re-pin goldens to silence drift.

2. **Quick verification** (establish clean baseline)
   ```bash
   SEED=42 python3 run_all_verification.py
   ```
   Or `make verify-quick`. Ensure it completes fully and restores goldens.

3. **Orient to open work**
   - Read `ledger/RESEARCH_LEDGER.md` for E049 status and any recently opened items
   - Read `AGENTS.md` for commands/conventions (especially "Baseline Integrity")
   - If user request is unclear, propose next concrete step based on ledger + verification state

## Key Files to Read First
- `AGENTS.md` – commands, conventions, guards
- `ledger/RESEARCH_LEDGER.md` – disposition of all experiments, open items
- `run_all_verification.py` – verification flow and guards
- `scripts/check.sh` – full check sequence

## Gotchas / Constraints
- Always use `SEED=42`
- Never leave a verification run half-finished (backup in `.verify_snapshot/`, guarded)
- `check_golden_baseline.py` enforces SHA-256 pins in `ledger/golden_baseline.json` — changing a golden requires explicit `--update` with intent
- `check_data_coverage.py` enforces cache coverage; offline mode used by verification
- Numeric drift from optimizer ill-conditioning is expected in places (E041/E042) — do not "fix" by re-pinning
- CI workflow cannot be created by agents (template in `.github/workflow-templates/`)

## Handoff Notes
- This handoff is durable and timestamped. Supersedes `HANDOFF_NEXT_SESSION_2026-10-29T09-28-23Z.md`.
- Symlinks `HANDOFF.md`, `HANDOFF_CURRENT.md`, `HANDOFF_NEXT.md`, `HANDOFF_NEXT_SESSION.md` should point here.

(End of file)