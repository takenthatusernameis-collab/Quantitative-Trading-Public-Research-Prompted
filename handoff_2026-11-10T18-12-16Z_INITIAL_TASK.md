# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-10T18:12:16Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `a9859c9f8387c031ad0342b4f9f44c12c094ceea` (`chore(kilo): checkpoint agent session`)
**Remote:** `origin/main` in sync at handoff check.
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current State

- `git status --short --branch`: `## main...origin/main`; only pre-existing unstaged `M src/__pycache__/cache_keys.cpython-312.pyc` observed (bytecode/mtime drift; not a baseline or source change). No staged or other source changes.
- `.verify_snapshot/`: absent (no interrupted verification run to recover).
- Tracked golden artifacts under `experiments/` matched `HEAD` at last handoff context; do not assume after future edits — verify before commit.
- Research phase complete (E001–E043). Authoritative dispositions/history: `ledger/RESEARCH_LEDGER.md`. Canonical baselines remain authoritative: `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`, pinned data under `data/`.
- Closed/resolved — do not reopen: E049/E050. E041/E042 retain residual ill-conditioned QP drift (~1-ulp sensitivity, 29–133 numeric diffs in extended reporting); **do not re-pin** E041/E042 artifacts to silence drift.

## Initial Task for Next Session (CLEAR)

**Default:** wait for explicit user instructions. Do not invent experiments, run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts without explicit direction.

### Before any requested work
1. `git status --short --branch` — confirm state, note `HEAD` vs `origin/main`, and treat unrelated `__pycache__` changes as out of scope unless asked.
2. Confirm `.verify_snapshot/` is absent. If present/stale: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
3. Review `AGENTS.md`, `ledger/RESEARCH_LEDGER.md`, and relevant `experiments/*.json` / drivers before changing code or artifacts.
4. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing substantive changes.

### If verification is explicitly requested
- Use `SEED=42` with standard commands (`scripts/check.sh`, `verify_convention_robustness.py`, `run_all_verification.py [--extended|--full|--skip-slow|--restore-only]`, or `make check/verify/verify-quick/verify-extended/verify-full`) as appropriate.
- **Never commit verification output** over canonical `experiments/*.json` goldens. Restore goldens after any interrupted run.
- If guards report golden/baseline mismatch, restore/fix before committing; do not re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` to silence drift without explicit, intentional re-baseline instruction and ledger-consistent justification.

## Guardrails

- `SEED=42` for reproducibility/verification runs.
- Preserve pre-registered gates, sensitivity grids, falsification expectations, and recorded outcomes unless explicitly instructed with justification and ledger update.
- Do not create `.github/workflows/` CI gates as an automated agent (use `.github/workflow-templates/verification-gate.yml` / maintainer path).
- Never commit secrets/keys or add logging of secrets.
- Do not stage/commit bytecode artifacts (`__pycache__/*.pyc`) unless explicitly instructed.

## Handoff Provenance

- **This durable handoff:** `handoff_2026-11-10T18-12-16Z_INITIAL_TASK.md` (root).
- **Supersedes (operationally):** `handoff_2026-11-10T18-11-24Z_INITIAL_TASK.md` and earlier timestamped handoffs (retained for history).
