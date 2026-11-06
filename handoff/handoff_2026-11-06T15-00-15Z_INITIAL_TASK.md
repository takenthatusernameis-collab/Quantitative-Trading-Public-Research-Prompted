# DURABLE HANDOFF — Next Agentic Session (Initial Task)

**Timestamp (UTC):** 2026-11-06T15:00:15Z
**Repo:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Branch:** main
**HEAD:** b41d9fa chore(kilo): checkpoint agent session
**Working tree:** clean (`git status --short` empty)
**State:** Research phase complete (E001–E043; E044–E050 closed). No open task in queue. No live verification snapshot (`.verify_snapshot/` absent).

## Initial task message for the next agentic work session

**START HERE — no open task.** Wait for explicit user instructions before taking any action.

- Do **not** invent new tasks, re-run verification "just to be sure", create additional handoffs unprompted, or re-open closed items.
- Read `AGENTS.md` and `ledger/RESEARCH_LEDGER.md` for context only if needed; follow all standing constraints.
- The committed golden artifacts and baselines are authoritative.

## Standing constraints (must follow)

- Never commit verification output. If a run is interrupted, restore goldens first: `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`).
- `experiments/*.json` are canonical goldens. Never re-pin to silence numeric drift from verification runs. Re-pinning requires explicit justification and `python3 scripts/check_golden_baseline.py --update`.
- Honor pinned inputs/baselines: `data/vintages.json`, `data/fundamentals_vintages.json`, `ledger/data_baseline.json`, `ledger/golden_baseline.json`. Verification uses `QUANT_RESEARCH_OFFLINE=1`; unpinned inputs fail hard.
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or validated constructions without explicit justification and a ledger entry.
- Follow `AGENTS.md`: `SEED=42`, close-to-close primary convention, pre-registration/multiple-testing discipline.
- Do not create/modify GitHub workflows (`.github/workflows/` is controller-managed; template only at `.github/workflow-templates/verification-gate.yml`).

## Current state snapshot

- `git log -1 --oneline`: `b41d9fa chore(kilo): checkpoint agent session`
- `.verify_snapshot/`: absent (no pending/live verification recovery)
- Key references: `AGENTS.md`, `ledger/RESEARCH_LEDGER.md`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`, `ledger/PRIORITIZATION.md`
- Closed items (do not re-open): E049/E050 optimizer determinism; E041/E042 ill-conditioned QP numeric drift (1e-5 scale) — do not re-pin; E029/E030 offline-reproducible via pinned caches.

## Verification commands (run only if explicitly requested)

- Fast check: `SEED=42 bash scripts/check.sh` (or `make check`)
- Quick verify: `SEED=42 python3 run_all_verification.py` (or `make verify-quick`)
- Extended: `SEED=42 python3 run_all_verification.py --extended` (or `make verify-extended`)
- Full: `SEED=42 python3 run_all_verification.py --full` (or `make verify-full`)
- Convention robustness only: `SEED=42 python3 verify_convention_robustness.py` (or `make verify`)
- Restore goldens if interrupted: `SEED=42 python3 run_all_verification.py --restore-only`

## Notes

- Dependencies may not be installed in the active environment; `pip install -r requirements.txt` before verification if requested.
- Follow all verification guards: `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`.

## Handoff provenance

- Created: `2026-11-06T15:00:15Z`
- Durable location: `handoff/handoff_2026-11-06T15-00-15Z_INITIAL_TASK.md`
- Supersedes: `handoff/handoff_2026-11-06T14-57-46Z_INITIAL_TASK.md`