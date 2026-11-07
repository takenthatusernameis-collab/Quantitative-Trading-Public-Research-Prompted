# INITIAL TASK — Handoff for Next Agent Session

**Timestamp (UTC):** 2026-11-07T14:31:25Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` — `91241992c14e8c6c2b382d2cfc782c7e4f0f20ff` (`chore(kilo): checkpoint agent session`, 2026-11-07 14:30:58 +0000)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current State (verified at handoff)

- `git status --short`: **clean** (no tracked/untracked changes observed).
- `git status --short experiments/ data/`: **clean** (no canonical artifact modifications).
- `.verify_snapshot/`: **absent** (no interrupted/pending verification restore).
- Research phase is complete (**E001–E043**). Dispositions and open/closed items live in `ledger/RESEARCH_LEDGER.md`.
- Canonical baselines are authoritative: `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`. **Do not modify or re-pin** as a side effect of routine verification.
- **Closed/resolved — do not reopen:** E049/E050 and E041/E042 residual ill-conditioned QP drift items. **Do not re-pin** E041/E042 artifacts to silence drift.

## Initial Task for Next Session (CLEAR)

**Default action: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts without explicit direction.

**If the user requests work, verify state first:**
1. `git status --short --branch` — confirm clean and `HEAD == origin/main` (or explain divergence).
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
3. Read `ledger/RESEARCH_LEDGER.md` for surviving validated strategies and any explicitly open items.
4. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing any substantive change.

**If asked to run verification:** use standard commands from `AGENTS.md`; **never commit verification output**. The suite backs up/restores `experiments/*.json`; if interrupted, restore before committing (`--restore-only` / `git checkout -- experiments/` per `AGENTS.md`).

## Reproduction / Verification Commands (only if explicitly requested)

```bash
SEED=42 bash scripts/check.sh                        # fast guards
SEED=42 python3 run_all_verification.py              # quick
SEED=42 python3 run_all_verification.py --extended   # quick + 18 drivers
SEED=42 python3 run_all_verification.py --full       # E042 n_sim=50 + 96-config grid
SEED=42 python3 run_all_verification.py --restore-only
SEED=42 python3 verify_convention_robustness.py      # reads JSONs, no writes
```

## Guardrails

- Never modify or re-pin canonical artifacts (`experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`) as a side effect of verification.
- Research phase is complete; wait for explicit user direction before new experiments or promotion-gate changes.
- Restore golden artifacts if any verification run is interrupted (`--restore-only`).
- Use `SEED=42` for reproducibility; follow pre-registration and multiple-testing discipline if any new experiment is explicitly requested.