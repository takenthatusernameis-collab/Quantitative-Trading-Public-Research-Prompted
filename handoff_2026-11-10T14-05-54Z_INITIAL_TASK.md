# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-10T14:05:54Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `39cded7e` (`chore(kilo): checkpoint agent session`) — in sync with `origin/main` at handoff.
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current State (verified at handoff)

- `git status --short --branch`: `## main...origin/main` (clean working tree; no staged/unstaged tracked changes observed).
- `.verify_snapshot/`: **absent** (no interrupted verification run to recover).
- No source, experiment, ledger, script, test, or canonical baseline artifact changes made in this session.
- **Research phase complete (E001–E043).** Authoritative dispositions and history: `ledger/RESEARCH_LEDGER.md`.
- Canonical baselines are authoritative and must not be casually modified: `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`.
- **Closed/resolved — do not reopen:** E049/E050 (optimizer determinism + exact KKT enumeration) and E041/E042 residual ill-conditioned QP drift (~1-ulp sensitivity). **Do not re-pin** E041/E042 artifacts to silence drift.
- Data note: some pinned cache files (e.g. `data/panel.parquet`) may be missing from a fresh/gitignored working tree; with `QUANT_RESEARCH_OFFLINE=1` enforced during verification, missing pinned cache entries fail hard.

## Initial Task for the Next Session (CLEAR)

**Default action: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts without explicit direction.

**If the user requests work, verify state first:**
1. `git status --short --branch` — confirm clean/dirty state and `HEAD`/remote alignment.
2. Confirm `.verify_snapshot/` is absent. If present/stale: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** any other work.
3. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing any substantive change.

**If asked to run verification (use `SEED=42`, only when explicitly requested):**
- Fast guards: `SEED=42 bash scripts/check.sh` / `make check`
- Convention only: `SEED=42 python3 verify_convention_robustness.py` or `SEED=42 python3 run_all_verification.py --skip-slow`
- Quick/full: `SEED=42 python3 run_all_verification.py` / `--extended` / `--full`
- Recovery: `SEED=42 python3 run_all_verification.py --restore-only`

**Never commit verification output** over `experiments/*.json`. If guards report golden/baseline mismatch, restore/fix before committing; do not re-pin to silence it.

## Guardrails

- **SEED=42** for all reproducibility/verification runs.
- Never commit driver verification output over canonical goldens; never leave `.verify_snapshot/` pending.
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (use `.github/workflow-templates/verification-gate.yml`; maintainer action required).
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and a ledger update.
- Never commit secrets/keys or introduce secret logging.
- Do not stage/commit bytecode (`__pycache__/*.pyc`) unless explicitly instructed.

## Handoff Provenance

- **Durable artifact (this session):** `handoff_2026-11-10T14-05-54Z_INITIAL_TASK.md` (root).
- **Operational supersedes:** `handoff_2026-11-10T13-21-49Z_INITIAL_TASK.md` and earlier timestamped handoffs (retained as history).
