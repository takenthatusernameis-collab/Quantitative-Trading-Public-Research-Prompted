# Handoff — Next Agentic Session (timestamped initial task message)

Created (UTC): 2026-10-31T20-31-13Z
Repo: Quantitative-Trading-Public-Research-Prompted
Commit: 9e20563 (branch: main)
Working tree: clean at handoff (no uncommitted source changes)

## Session Context
Research phase complete (E001–E049). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`. Verification baseline integrity guards are in place (`scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`). The verification suite is the source of truth for reproducing canonical artifacts.

## Initial Task (clear, durable)
**Do not start large-scale refactors.** For this session, perform a quick health check and verify baseline integrity before doing any new work.

1. **Health check**
   - `git status --short` (expect clean; only tracked bytecode caches may appear)
   - `git log -1 --oneline`
   - Confirm no active snapshot: check `.verify_snapshot/` does not contain `ACTIVE.json` (if it exists, read it; do **not** delete blindly)

2. **Baseline integrity (must pass)**
   - `SEED=42 bash scripts/check.sh` (convention-robustness + template validation + baseline guards). This should complete quickly and report success.
   - If it fails on golden mismatch, follow AGENTS.md recovery guidance (`SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`). Never re-pin baselines as a side effect of verification.

3. **Reproducibility sanity (optional but recommended)**
   - `SEED=42 python3 verify_convention_robustness.py` (reads JSONs only). Or run `make verify-quick` only if explicitly asked to re-verify; otherwise skip slow runs.

## Active Known Constraints (read before changes)
- **Never overwrite canonical `experiments/*.json` via ad-hoc runs.** The verification suite backs up/restores; do not commit verification output.
- **Data coverage is enforced.** Adding any new `data.download()` requires committing the cache file and re-pinning via `scripts/check_data_coverage.py --update` (see AGENTS.md).
- **Optimizer determinism (E049):** `src/portfolio_opt.py` validates on problem constraints (not solver exit status). Tangency/min-var grids may still show small numeric drift; do not re-pin to silence 1-ulp sensitivity.
- **Offline reproducibility:** Drivers are run with `QUANT_RESEARCH_OFFLINE=1` by verification; live network downloads are not expected and will fail if unpinned.

## Next Suggested Priorities (if health check passes)
- Review `ledger/RESEARCH_LEDGER.md` for any open items (notably E049 numeric drift note) and confirm disposition.
- If extending research, follow pre-registration discipline (gates, falsification, sensitivity reported not gated, placebo). Update ledger entries before/when promoting.
- Keep verification hygiene intact: run `scripts/check.sh` before any commit that touches experiment artifacts or data coverage.

## Handoff Notes
- This file is the durable initial task message for the next agentic session.
- Prior handoffs remain for history: see `HANDOFF_NEXT_SESSION_2026-10-30T01-39-41Z.md`, `HANDOFF-2026-10-30T18-19-14Z.md`, etc.
- No live verification snapshot is expected. If present, do not start a new verification run until it is cleared/recovered.
