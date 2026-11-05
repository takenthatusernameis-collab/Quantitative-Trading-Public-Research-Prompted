# DURABLE HANDOFF — Next Agentic Session

**Timestamp (UTC):** 2026-11-05T22:57:35Z
**Repo:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Branch:** main
**HEAD:** c319b7b chore(kilo): checkpoint agent session
**State:** Research phase complete (E001–E043; closed items through E050). Working tree clean at handoff creation. No live verification snapshot. No open task in queue.

## Initial task message for the next agentic work session

> **START HERE:** The repository is in a clean, closed state at HEAD `c319b7b`. There is **no open task in the queue**. Wait for explicit user instructions before taking any action.
>
> Do **not** invent new tasks, do **not** re-run verification "just to be sure", do **not** create additional handoffs unprompted, and do **not** re-open closed items. Follow all standing constraints in `AGENTS.md`.

## Current state (at handoff time)

- `git status --short`: clean
- `.verify_snapshot/ACTIVE.json`: absent — no live or pending verification run
- Canonical artifacts: `experiments/*.json` (golden baseline), `ledger/golden_baseline.json`, `ledger/data_baseline.json`
- Research phase complete; surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`
- Known closed/drift items (do not re-open): E049/E050 optimizer determinism; E041/E042 ill-conditioned QP 1-ulp drift (structural issue resolved in E049, residual numeric drift remains; do **not** re-pin to silence). E029/E030 offline-reproducible via pinned caches.

## Standing constraints (must follow)

- Never commit verification output. If a run is interrupted, restore goldens: `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/` only when HEAD is known-good per `ledger/golden_baseline.json`).
- `experiments/*.json` are canonical. Never re-pin artifacts to silence verification drift. Re-pinning requires explicit justification and `python3 scripts/check_golden_baseline.py --update`.
- Honor pinned cache vintages (`data/vintages.json`, `data/fundamentals_vintages.json`, `ledger/data_baseline.json`). Verification uses `QUANT_RESEARCH_OFFLINE=1`; unpinned inputs fail hard.
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or validated constructions without explicit justification and a ledger entry.
- Use `SEED=42` for reproducibility runs. Close-to-close is the v1.2.3 primary convention.
- Do not create/modify `.github/workflows/` (controller-managed; template at `.github/workflow-templates/verification-gate.yml`).

## Quick Start (only if explicitly requested)

1. `git log -1 --oneline && git status --short`
2. Read `AGENTS.md` and `ledger/RESEARCH_LEDGER.md` for context
3. Fast check: `SEED=42 bash scripts/check.sh` (or `make check`)
4. Run heavier verification **only** on explicit request:
   - `make verify-quick` / `SEED=42 python3 run_all_verification.py`
   - `make verify-extended` / `--extended`
   - `make verify-full` / `--full`
5. Restore on interruption before any commit: `SEED=42 python3 run_all_verification.py --restore-only`

## Notes

- Dependencies may not be installed in the active environment; `pip install -r requirements.txt` if verification is explicitly requested.
- Pre-registration, multiple-testing discipline, and falsification expectations remain in force for any future requested experiments.
- This handoff is informational; it does not authorize new work.
