# DURABLE HANDOFF — Next Agentic Session (Initial Task)

**Timestamp (UTC):** 2026-11-06T18:49:46Z
**Repo:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Branch:** main
**HEAD:** 6b5c6c0 chore(kilo): checkpoint agent session
**Working tree:** clean (`git status --short` empty)
**State:** Research phase complete (E001–E043; E044–E050 closed). No open task in queue. No live verification snapshot (`.verify_snapshot/` absent).

## Initial task message for the next agentic work session

**START HERE — no open task assigned.** Wait for explicit user instructions before taking any action.

- Do **not** invent tasks, re-run verification "just to be sure", create additional handoffs unprompted, or re-open closed items.
- Read `AGENTS.md` and `ledger/RESEARCH_LEDGER.md` for context only if needed; follow all standing constraints.
- Committed golden artifacts and baselines are authoritative.

## Standing constraints

- Never commit verification output. If a run is interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`).
- `experiments/*.json` are canonical goldens. Never re-pin to silence numeric drift. Re-pinning requires explicit justification + `python3 scripts/check_golden_baseline.py --update`.
- Honor pinned inputs: `data/vintages.json`, `data/fundamentals_vintages.json`, `ledger/data_baseline.json`, `ledger/golden_baseline.json`. Verification runs with `QUANT_RESEARCH_OFFLINE=1`.
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or validated constructions without explicit justification and a ledger entry.
- Follow `AGENTS.md`: `SEED=42`, close-to-close primary convention, pre-registration/multiple-testing discipline.
- Do not create/modify `.github/workflows/` (controller-managed; template only at `.github/workflow-templates/verification-gate.yml`).

## Quick reference (run only if explicitly requested)

- `SEED=42 bash scripts/check.sh` (or `make check`)
- `SEED=42 python3 run_all_verification.py` (quick)
- `SEED=42 python3 run_all_verification.py --extended`
- `SEED=42 python3 run_all_verification.py --full`
- `SEED=42 python3 verify_convention_robustness.py`
- Restore after interruption: `SEED=42 python3 run_all_verification.py --restore-only`

## Known closed/guarded items

- E049/E050 optimizer determinism closed; E041/E042 ill-conditioned QP numeric drift (1e-5 scale) — do not re-pin.
- E029/E030 offline-reproducible via pinned caches.
- `.verify_snapshot/` absent (no pending recovery).

(End of file)