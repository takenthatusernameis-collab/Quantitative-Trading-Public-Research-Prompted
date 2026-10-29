# HANDOFF: Next Agentic Work Session

**Created:** $(date -u +%Y-%m-%dT%H:%M:%SZ) (message time)
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Branch:** main @ `$(git rev-parse --short HEAD)` $(git status --short | wc -l | xargs test 0 -eq && echo "(clean)" || echo "(dirty)"), up to date with `origin/$(git rev-parse --abbrev-ref HEAD 2>/dev/null || echo main)`

## State

Research phase complete (E001–E043). Surviving validated strategies documented in
`ledger/RESEARCH_LEDGER.md`. Baseline integrity guards enforced. Working tree
clean of tracked source/data changes except `__pycache__/*.pyc` (force-tracked,
pre-existing, out of scope). No `.verify_snapshot/` active; no interrupted run to recover.

## Initial Task (Start Here)

Verify the baseline is clean before any work.

1. Run `SEED=42 bash scripts/check.sh` — all guards must pass with no golden diffs.
2. Run `git status --short` / `git diff --name-only` — confirm clean tree.
3. If an interrupted verification left dirty `experiments/*.json`, restore:
   `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`).

Do not re-pin goldens to silence drift. Keep committed goldens authoritative.
Read `AGENTS.md` and `ledger/RESEARCH_LEDGER.md` first.

## Known Open Items (Do Not "Fix" By Re-Pinning)

- **E041 numeric drift (open):** Optimizer determinism issue (ledger E049) fixed
  gating on solver status, but the tangency QP remains ill-conditioned. Extended
  verification still reports ~133 numeric differences for E041; **do not re-pin
  `experiments/e041_*.json`**. See `ledger/RESEARCH_LEDGER.md` (E049).
- **E042 grid artifacts:** Similar 1-ulp sensitivity can appear in the E042
  sensitivity grid. Do not re-pin goldens to force a match.
- **E030:** numeric diffs on near-zero quantities (documented). Do not re-pin.
- **Data coverage:** Inputs must remain tracked and pinned in
  `ledger/data_baseline.json`. If adding a new data file, commit it and run
  `python3 scripts/check_data_coverage.py --update` deliberately (never as a
  side-effect of `run_all_verification.py`).
- **Pinned fundamentals/vintages:** `data/fundamentals/` (per
  `data/fundamentals_vintages.json`) and vintage pins in `data/vintages.json`
  are authoritative for reproducibility.

## Quick Verification

```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 verify_convention_robustness.py
```
