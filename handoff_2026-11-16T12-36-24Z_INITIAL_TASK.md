# INITIAL TASK — Durable Handoff for the Next Agentic Work Session

**Timestamp (UTC):** 2026-11-16T12:36:24Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `2cee60327b73ac5f15b2a6a2044e638a7be6618a` ("chore(kilo): checkpoint agent session"), in sync with `origin/main` (`git rev-list --left-right --count origin/main...HEAD` → `0 0`)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current state (verified at this handoff)

- **Working tree:** no source/content changes. Tracked modifications are limited to `__pycache__/*.pyc` under `scripts/`, `src/`, and `tests/` — build noise; do not commit.
- **`.verify_snapshot/` / `.verify_reports/`:** absent — no interrupted verification run pending.
- **Canonical artifacts/baselines:** `experiments/` (107 JSON goldens), `ledger/` (`RESEARCH_LEDGER.md`, `PRIORITIZATION.md`, `golden_baseline.json`, `data_baseline.json`), and `data/` show no modifications. Baseline/ledger files intact.
- **Research phase:** complete (E001–E043). Authoritative dispositions and open items: `ledger/RESEARCH_LEDGER.md`; ranking: `ledger/PRIORITIZATION.md`.
- **Closed/resolved — do not reopen:** E049/E050 (optimizer determinism + exact KKT enumeration) and E041/E042 residual ill-conditioned QP drift (~1-ulp, ~1e-05). Do **not** re-pin E041/E042 artifacts to silence drift.

## Baseline integrity (re-verified this session)

`SEED=42 bash scripts/check.sh` → exit 0, `=== All checks passed ===` (run 2026-11-16T12:36Z). Green across the board: JSON parse, golden-vs-HEAD, pinned golden fingerprints, pinned data-input coverage, guard unit-test modules, `verify_convention_robustness.py`, `validate_template.py`, and `check_experiment_imports.py` (all 26 drivers).

**Dependency note:** if a fresh sandbox lacks the scientific stack, install before `check.sh` will run:
`python3 -m pip install --break-system-packages -r requirements.txt`

## Initial task for next session (CLEAR)

**Default: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts without explicit direction.

**If the user requests work, verify state first:**
1. `git status --short --branch` — confirm HEAD/remote alignment; handle tracked `__pycache__` modifications explicitly (restore/discard, do not commit).
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
3. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing any substantive change.

**If asked to run verification:** always use `SEED=42`; **never commit verification output** over `experiments/*.json`; restore goldens after any interrupted run. If guards report golden/baseline mismatch, fix or restore before committing — do not re-pin to silence it.

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

- Always use **SEED=42** for reproducibility/verification runs. Primary convention: close-to-close v1.2.3 (overnight reported alongside).
- Never commit driver verification output over canonical goldens (`experiments/*.json`).
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction and ledger justification.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (template: `.github/workflow-templates/verification-gate.yml`; maintainer action required).
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and a ledger update.
- Verification runs offline (`QUANT_RESEARCH_OFFLINE=1`); missing pinned caches must fail hard. Never commit secrets/keys; never log secrets.

## Handoff provenance

- **Durable artifact (this session):** `handoff_2026-11-16T12-36-24Z_INITIAL_TASK.md` (repo root; generic pointer aliases repointed via `scripts/repoint_handoff.py`).
- **Supersedes operationally:** `handoff_2026-11-16T11-41-23Z_INITIAL_TASK.md`, `HANDOFF-2026-11-16T12-33-56Z.md`, and earlier timestamped handoffs (retained for history).
- This session verified state (`scripts/check.sh` green) and created this durable handoff only; no code, experiments, ledgers, or baselines were modified.