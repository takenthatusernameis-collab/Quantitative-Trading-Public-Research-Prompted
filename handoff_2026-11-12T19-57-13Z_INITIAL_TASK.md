# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-12T19:57:13Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `46ae3d7027bfcaf21c95fe87312fecb985b1c03f` (`chore(kilo): checkpoint agent session`, 2026-11-12 19:55:54 +0000) — in sync with `origin/main`
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current state (verified at handoff time)

- **Working tree:** clean at handoff creation time (`git status --short --branch` → `## main...origin/main`, 0 modifications / 0 untracked).
- **`.verify_snapshot/`:** absent (no interrupted verification run pending).
- **Baselines (verified live this session):** 138 tracked `experiments/` artifacts (107 golden JSONs + 31 drivers); `python3 scripts/check_golden_baseline.py` → **ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT**; `python3 scripts/check_data_coverage.py` → **ALL 35 PINNED DATA INPUTS ARE PRESENT, TRACKED AND UNCHANGED**.
- **Research phase:** complete (E001–E043). Authoritative dispositions/evidence: `ledger/RESEARCH_LEDGER.md`; ranking: `ledger/PRIORITIZATION.md`. Last research entry E051; subsequent ledger entries are durable-handoff refreshes.
- **Closed/resolved — do not reopen:** E049/E050 (optimizer determinism + exact KKT enumeration) and residual E041/E042 ill-conditioned QP drift (~1-ulp, ~1e-05). Do **not** re-pin E041/E042 artifacts to silence drift.
- **Delta vs prior durable handoff (E177, HEAD `3888670c` → prior handoff at 2026-11-12T19:53:29Z):** HEAD advanced via one checkpoint commit. `git diff --name-only 3888670c..HEAD` → 550 paths: 546 generic canonical-pointer symlinks (repointed to this artifact), 1 `ledger/RESEARCH_LEDGER.md` entry (this E178 record), and timestamped handoff artifacts. Filtered for non-handoff content → **0 paths**; no `experiments/`, `data/`, `src/`, `tests/`, or research substance changed.

## Initial task for next session (CLEAR)

**Default: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change pre-registered gates/outcomes, or modify golden/baseline artifacts without explicit direction.

If work is requested, verify state first:
1. `git status --short --branch` — confirm HEAD/remote alignment and clean tree.
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
3. Re-run guards before substantive changes/commits:
   - `python3 scripts/check_golden_baseline.py`
   - `python3 scripts/check_data_coverage.py`
   - `SEED=42 bash scripts/check.sh` (or `make check`)

## Reproduction / verification (only if explicitly requested)

```bash
SEED=42 bash scripts/check.sh                         # fast guards (~seconds, offline)
SEED=42 python3 verify_convention_robustness.py       # reads JSONs, no writes
SEED=42 python3 scripts/check_golden_baseline.py      # 107 goldens vs ledger/golden_baseline.json
SEED=42 python3 scripts/check_data_coverage.py        # 35 pinned data inputs
SEED=42 python3 run_all_verification.py               # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended
SEED=42 python3 run_all_verification.py --full
SEED=42 python3 run_all_verification.py --restore-only
make check / make verify / make verify-quick / make verify-extended / make verify-full
```
> Full checks/tests/verification require scientific deps (`pip install -r requirements.txt`: numpy, pandas, scipy, statsmodels, yfinance). Missing deps in a sandbox are environmental, not a repo defect.

## Guardrails

- Always use **SEED=42** for reproducibility/verification runs.
- Never commit verification output over canonical goldens (`experiments/*.json`).
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction and ledger justification.
- Do not reopen closed E049/E050 or E041/E042 drift items; do not move pre-registered goalposts post-hoc.
- Do not create `.github/workflows/` CI gates as an automated agent (template: `.github/workflow-templates/verification-gate.yml`; maintainer action required).
- Never commit secrets/keys or log secrets.

## Handoff provenance

- **Durable artifact (this session):** `handoff_2026-11-12T19-57-13Z_INITIAL_TASK.md` (repo root).
- **Supersedes operationally:** `handoff_2026-11-12T19-53-29Z_INITIAL_TASK.md` and earlier timestamped handoffs (retained for history).
- Generic canonical handoff pointers repointed to this artifact via `scripts/repoint_handoff.py`. No code, experiments, ledgers, or baselines modified by this handoff creation.