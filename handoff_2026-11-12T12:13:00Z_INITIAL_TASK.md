# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-12T12:13:00Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current State (verified at handoff)

- Research phase complete (E001–E043). Authoritative dispositions/history: `ledger/RESEARCH_LEDGER.md`.
- Canonical baselines are authoritative and must not be changed incidentally: `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`.
- **Closed/resolved — do not reopen:** E049/E050 (optimizer determinism + exact KKT enumeration) and E041/E042 residual ill-conditioned QP drift. Do **not** re-pin E041/E042 artifacts to silence drift.
- Working tree note: `src/__pycache__/cache_keys.cpython-312.pyc` is modified (unrelated bytecode artifact); do not commit it. No source, experiment, ledger, script, test, or baseline changes were made in this handoff session beyond this file and repointed generic handoff symlinks.
- Before substantive work, confirm `git status --short --branch`, `HEAD`/remote alignment, and absence of `.verify_snapshot/` (recover with `SEED=42 python3 run_all_verification.py --restore-only` if stale).

## Initial Task for the Next Session (CLEAR)

**Default action: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts without explicit direction.

**If the user requests work:**
1. Verify repo/baseline state as needed (`SEED=42 bash scripts/check.sh` or targeted guards).
2. Perform only the explicitly requested, in-scope changes while preserving pre-registration, multiple-testing discipline, and honest negative-result conventions.
3. If verification is explicitly requested, use documented commands and ensure canonical `experiments/*.json` baselines are restored/unchanged unless an intentional, explicit re-baseline is instructed (with deliberate `--update`/ledger re-pin where applicable).

## Verification / Reproduction (only if explicitly requested)

```bash
SEED=42 bash scripts/check.sh                         # fast guards (~seconds, offline)
SEED=42 python3 verify_convention_robustness.py       # reads JSONs, no writes
SEED=42 python3 run_all_verification.py               # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended    # quick + 18 committed drivers
SEED=42 python3 run_all_verification.py --full        # E042 n_sim=50 + 96-config grid
SEED=42 python3 run_all_verification.py --restore-only
SEED=42 python3 run_all_verification.py --skip-slow   # convention only
make check / make verify / make verify-quick / make verify-extended / make verify-full
```

## Guardrails

- Always use **SEED=42** for reproducibility/verification runs.
- Never commit driver verification output over canonical goldens (`experiments/*.json`); never leave a run half-finished with a pending `.verify_snapshot/`.
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (maintainer path: `.github/workflow-templates/verification-gate.yml`).
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and ledger update.
- Never commit secrets/keys or introduce secret logging.

## Handoff Provenance

- **Durable artifact (this session):** `handoff_2026-11-12T12:13:00Z_INITIAL_TASK.md`
- **Supersedes (operationally):** `handoff_2026-11-12T12:11:09Z_INITIAL_TASK.md` and earlier timestamped handoffs (retained as history).
- Generic convenience symlinks/pointers repointed to this file via `scripts/repoint_handoff.py`.
