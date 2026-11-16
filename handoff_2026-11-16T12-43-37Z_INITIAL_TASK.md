# INITIAL TASK — Durable Handoff for the Next Agentic Work Session

**Timestamp (UTC):** 2026-11-16T12:43:37Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main...origin/main` @ `aaf55a4848957e53d52c55c8bd478add11ab1ae1` ("chore(kilo): checkpoint agent session")
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current state (observed)

- **Working tree:** no source/content changes. Tracked modifications are limited to `__pycache__/*.pyc` under `scripts/`, `src/`, and `tests/` (build/import noise) — **do not commit**; restore/discard if needed before committing other work.
- **Interrupted verification:** `.verify_snapshot/` and `.verify_reports/` absent (no pending recovery).
- **Canonical baselines/artifacts:** `experiments/` (goldens), `ledger/` (`RESEARCH_LEDGER.md`, `PRIORITIZATION.md`, `golden_baseline.json`, `data_baseline.json`), and pinned `data/` inputs show no content modifications in this session. Do not overwrite goldens with verification output.
- **Research phase:** complete (E001–E043). Authoritative dispositions/open items: `ledger/RESEARCH_LEDGER.md`; ranking: `ledger/PRIORITIZATION.md`.
- **Closed/resolved — do not reopen:** E049/E050 (optimizer determinism + exact KKT enumeration) and E041/E042 residual ~1-ulp/ill-conditioned QP drift (~1e-05). Do **not** re-pin E041/E042 artifacts to silence drift.

## Baseline integrity

- Most recent recorded green check (`handoff_2026-11-16T12-38-14Z_INITIAL_TASK.md`): `SEED=42 bash scripts/check.sh` → exit 0 (`=== All checks passed ===`, 2026-11-16T12:36Z). No source/ledger/experiment/data edits made in this session.
- **Before substantive work or commit, re-verify:**
  1. `git status --short --branch` — confirm HEAD/alignment; handle tracked `__pycache__` diffs explicitly.
  2. Confirm `.verify_snapshot/` absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`).
  3. `SEED=42 bash scripts/check.sh` (or `make check`) — must pass.

## Initial task for next session (CLEAR)

**Default: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts without explicit direction.

**If the user requests work:**
1. Verify state (status, no `.verify_snapshot/`, `SEED=42 bash scripts/check.sh`).
2. Execute only the explicitly requested task within existing pre-registered scope and guardrails.
3. If verification is requested, use `SEED=42`; **never commit driver verification output** over `experiments/*.json`; restore after any interruption. Do not re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` to silence mismatches — restore or justify per ledger/`AGENTS.md`.

## Reproduction / verification commands (run only if explicitly requested)

```bash
SEED=42 bash scripts/check.sh                         # fast guards (~seconds, offline)
SEED=42 python3 verify_convention_robustness.py       # reads JSONs, no writes
SEED=42 python3 run_all_verification.py               # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended    # quick + 18 committed drivers (~21 min)
SEED=42 python3 run_all_verification.py --full        # E042 n_sim=50 + 96-config grid (~15 min)
SEED=42 python3 run_all_verification.py --restore-only
SEED=42 python3 run_all_verification.py --skip-slow   # convention only
make check / make verify / make verify-quick / make verify-extended / make verify-full
```

## Guardrails

- Always use **SEED=42** for reproducibility/verification. Primary convention: close-to-close v1.2.3 (overnight reported alongside).
- Never commit verification output over canonical goldens (`experiments/*.json`).
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction and ledger justification.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (template: `.github/workflow-templates/verification-gate.yml`; maintainer action required).
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and a ledger update.
- Verification runs offline (`QUANT_RESEARCH_OFFLINE=1`); missing pinned caches must fail hard. Never commit secrets/keys.

## Handoff provenance

- **Durable artifact (this session):** `handoff_2026-11-16T12-43-37Z_INITIAL_TASK.md` (repo root). Generic pointer aliases repointed to this file.
- **Supersedes operationally:** `handoff_2026-11-16T12-38-14Z_INITIAL_TASK.md` and earlier timestamped handoffs (retained for history).
- This session created this durable handoff only; no code, experiments, ledgers, or baselines were modified.
