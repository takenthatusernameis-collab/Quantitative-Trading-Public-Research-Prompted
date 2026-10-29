# HANDOFF: Next Agentic Work Session

**Created:** 2026-10-29T22:38:39Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**State:** Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`
**Verification:** Goldens are protected. Baseline integrity guards are enforced.

## Initial Task (Start Here)

Do **not** jump straight to new experiments. Verify the baseline is clean first.

### 1) Verify baseline integrity (MANDATORY)
```bash
SEED=42 bash scripts/check.sh
```
This runs: `py_compile`, `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `tests/test_portfolio_opt.py`, and convention-robustness checks. All must pass with no golden diffs.

### 2) Confirm a clean git state
```bash
git status --short
git diff --name-only
```
If `experiments/*.json` are modified but `scripts/check.sh` did not just run a verification, or if the tree is dirty from an interrupted run, **restore before committing**:

```bash
SEED=42 python3 run_all_verification.py --restore-only
# or: git checkout -- experiments/
```

If `check_goldens_clean.py` reports a stale snapshot owned by another PID or a pending `.verify_snapshot/ACTIVE.json`, do not delete it blindly. Follow the recovery guidance in `AGENTS.md`.

## Known Open Items (Do Not "Fix" By Re-Pinning)

- **E041 numeric drift (open):** Optimizer determinism issue (ledger E049) fixed gating on solver status, but the tangency QP remains ill-conditioned. Extended verification still reports ~133 numeric differences for E041; **do not re-pin `experiments/e041_*.json`** to silence this. See `ledger/RESEARCH_LEDGER.md` (E049).
- **E042 grid artifacts:** Similar 1-ulp sensitivity can appear in the E042 sensitivity grid. Do not re-pin goldens to force a match.
- **Data coverage:** Inputs must remain tracked and pinned in `ledger/data_baseline.json`. If adding a new data file, commit it and run `python3 scripts/check_data_coverage.py --update` deliberately (never as a side-effect of `run_all_verification.py`).
- **Pinned fundamentals/vintages:** `data/fundamentals/` (per `data/fundamentals_vintages.json`) and `data/vintages.json` are part of reproducibility. Treat as canonical.

## Read These First
- `AGENTS.md` — commands, baseline integrity rules, verification modes, drift notes
- `ledger/RESEARCH_LEDGER.md` — decisions, gates, falsification, and open items
- `ledger/golden_baseline.json` — pinned SHA-256s for canonical artifacts
- `run_all_verification.py` — how the suite backs up/restores goldens

## Useful Commands
```bash
# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py

# Convention robustness only (offline)
SEED=42 python3 verify_convention_robustness.py

# Extended (more drivers, still restores goldens)
SEED=42 python3 run_all_verification.py --extended

# Full (heavier)
SEED=42 python3 run_all_verification.py --full
```

## Goal For This Session
Keep the committed goldens authoritative. If you need to change an experiment's canonical artifact, you must justify it against the research process (and explicitly re-pin via the guard scripts) — never by letting the verification suite overwrite and commit the new run. Focus on reading/validating rather than re-baselining unless there is a documented, justified reason.
