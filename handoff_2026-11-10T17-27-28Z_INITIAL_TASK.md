# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-10T17:27:28Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `83874abebb836297c1e6cf49257bb5aa880b0788` (`chore(kilo): checkpoint agent session`)
**Remote:** `origin/main` in sync (verified)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current State (verified at handoff)

- `git status --short --branch`: `## main...origin/main` with one pre-existing unstaged change: `M src/__pycache__/cache_keys.cpython-312.pyc` (bytecode mtime/mode drift; not a source/baseline change).
- `.verify_snapshot/`: **absent** (no interrupted verification run to recover).
- Tracked canonical baselines/goldens remain authoritative: `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`, pinned data under `data/`.
- Research phase **complete (E001–E043)**. Authoritative dispositions/history: `ledger/RESEARCH_LEDGER.md`.
- **Closed/resolved — do not reopen:** E049/E050 (optimizer determinism + exact KKT enumeration) and E041/E042 residual ill-conditioned QP drift (~1-ulp sensitivity). **Do not re-pin** E041/E042 artifacts to silence drift.
- Known note: some pinned data (e.g. `data/panel.parquet`) may be gitignored/absent in a fresh tree; verification enforces `QUANT_RESEARCH_OFFLINE=1` so missing pinned cache fails hard rather than downloading.

## Initial Task for Next Session (CLEAR)

**Default action: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts without explicit direction.

### If the user requests work, verify state first
1. `git status --short --branch` — confirm source state and HEAD/remote alignment; ignore unrelated `__pycache__` changes unless asked.
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
3. Review `AGENTS.md`, `ledger/RESEARCH_LEDGER.md`, and relevant `experiments/*.json` / experiment driver before changes.
4. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing any substantive change.

### If asked to run verification
- Use standard commands with `SEED=42` (see below).
- **Never commit verification output** over canonical `experiments/*.json` goldens.
- Restore goldens after any interrupted run.
- If guards report a golden/baseline mismatch, fix/restore before committing; do not re-pin to silence drift without explicit, intentional re-baseline instruction and ledger-consistent justification.

## Reproduction / Verification Commands (only if explicitly requested)

```bash
SEED=42 bash scripts/check.sh                         # fast guards (~seconds, offline)
SEED=42 python3 verify_convention_robustness.py       # reads JSONs, no writes
SEED=42 python3 run_all_verification.py               # quick
SEED=42 python3 run_all_verification.py --extended    # quick + 18 drivers
SEED=42 python3 run_all_verification.py --full        # E042 n_sim=50 + 96-config grid
SEED=42 python3 run_all_verification.py --restore-only
SEED=42 python3 run_all_verification.py --skip-slow   # convention only
make check / make verify / make verify-quick / make verify-extended / make verify-full
```

## Guardrails

- **SEED=42** for all reproducibility/verification runs.
- Never commit driver verification output over canonical goldens (`experiments/*.json`).
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction and ledger-consistent justification.
- Do not reopen closed E049/E050 or E041/E042 residual-drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (maintainer action; template: `.github/workflow-templates/verification-gate.yml`).
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and a ledger update.
- Never commit secrets/keys or add logging of secrets.
- Do not stage/commit bytecode artifacts (`__pycache__/*.pyc`) unless explicitly instructed.

## Handoff Provenance

- **Durable artifact (this session):** `handoff_2026-11-10T17-27-28Z_INITIAL_TASK.md` (root).
- **Supersedes (operationally):** `handoff_2026-11-10T17-22-46Z_INITIAL_TASK.md` and earlier timestamped handoffs (retained as history).
