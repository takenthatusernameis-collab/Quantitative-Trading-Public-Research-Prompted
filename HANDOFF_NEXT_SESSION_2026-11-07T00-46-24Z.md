# DURABLE HANDOFF — Next Agentic Session

**Timestamp (UTC):** 2026-11-07T00:46:24Z
**Repo:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Branch:** main
**HEAD:** 6d96895 chore(kilo): checkpoint agent session
**State:** Research phase complete (E001–E043; E044–E050 closed). **No open task in queue.**

## Initial task message for the next agentic work session

> **START HERE — WAIT FOR EXPLICIT USER INSTRUCTIONS.**
> The baseline is closed and verified by policy; there is currently no open task in the queue. Do **not** invent new tasks, re-run verification "just to be sure", create additional handoffs unprompted, modify experiments/goldens/baselines, or re-open closed items. Follow all standing constraints in `AGENTS.md`. Act only on an explicit user request.

## Current state (observed at handoff time)

- `git status --short`: 12 modified tracked `__pycache__/*.cpython-312.pyc` files under `scripts/__pycache__/`, `src/__pycache__/`, `tests/__pycache__/` only. **Harmless bytecode drift; not experiment goldens.** No source, test, experiment JSON, or ledger changes. Clean with `git checkout -- scripts/__pycache__ src/__pycache__ tests/__pycache__` if desired.
- `.verify_snapshot/`: absent — no live/pending verification run.
- `experiments/*.json` goldens: not modified in working tree (pycache only). Canonical baseline remains pinned by `ledger/golden_baseline.json` / `ledger/data_baseline.json`.
- Known closed items (do not re-open): E049/E050 optimizer determinism + exact KKT enumeration; E041/E042 ill-conditioned QP drift (1e-5 scale, 1-ulp sensitivity). E029/E030 offline-reproducible via pinned caches.
- Dependencies may not be installed in the active environment; run `pip install -r requirements.txt` before any verification.

## Standing constraints (must follow)

- **Never commit verification output.** If a run is interrupted, restore goldens first: `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/` only when HEAD is known-good vs pinned baseline).
- **Golden files (`experiments/*.json`) are canonical.** Never re-pin artifacts to silence numeric drift from verification runs. Re-pinning requires explicit justification and `python3 scripts/check_golden_baseline.py --update` (diff-visible, intentional).
- **Honor pinned caches/vintages:** `data/vintages.json`, `data/fundamentals_vintages.json`, `ledger/data_baseline.json`. Verification uses `QUANT_RESEARCH_OFFLINE=1`; unpinned inputs fail hard.
- **Do not change** gate logic, sensitivity grids, pre-registered outcomes, or validated constructions without explicit justification and a ledger entry.
- **Follow repo conventions** in `AGENTS.md` (SEED=42, close-to-close primary, offline verification, multiple-testing discipline).
- **Do not create/modify GitHub workflows** (`.github/workflows/` is controller-managed; template at `.github/workflow-templates/verification-gate.yml`).

## Quick Start for next session

1. `git log -1 --oneline && git status --short`
2. Read `AGENTS.md` (baseline integrity, verification rules, constraints).
3. Read `ledger/RESEARCH_LEDGER.md` for context if needed.
4. **Do not run verification** unless explicitly requested by the user.
5. Wait for explicit user task/instructions.

## Verify commands (only if explicitly requested)

- Fast check: `SEED=42 bash scripts/check.sh` or `make check`
- Quick: `SEED=42 python3 run_all_verification.py` or `make verify-quick`
- Extended: `SEED=42 python3 run_all_verification.py --extended` or `make verify-extended`
- Full: `SEED=42 python3 run_all_verification.py --full` or `make verify-full`
- Convention only: `SEED=42 python3 verify_convention_robustness.py` or `make verify`
- Restore after interruption: `SEED=42 python3 run_all_verification.py --restore-only`

## Guardrails

- Do not modify `experiments/*.json` as a side effect of verification without the re-pinning process; the committed golden is authoritative.
- Follow guards: `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`.
- Do not create unprompted handoffs or re-open closed items.
- Pre-registration, multiple-testing discipline, and falsification expectations remain in force if new experiments are ever requested.
