# HANDOFF: Next Agentic Work Session

**Created:** 2026-10-29T23:31:34Z (message time)
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Branch:** main @ `92b1583` (checkpoint commit; working tree clean of tracked source/data changes except `__pycache__/*.pyc`).

## State

Research phase complete (E001–E043). Surviving validated strategies documented in
`ledger/RESEARCH_LEDGER.md`. Baseline integrity guards enforced. No `.verify_snapshot/`
active; no interrupted run to recover.

## Initial Task (Start Here)

Verify the baseline is clean before any work.

1. Run `SEED=42 bash scripts/check.sh` — all guards must pass with no golden diffs.
2. Run `git status --short` / `git diff --name-only` — confirm clean tree.
3. If an interrupted verification left dirty `experiments/*.json`, restore:
   `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`).

Do not re-pin goldens to silence drift. Keep committed goldens authoritative.
Read `AGENTS.md` and `ledger/RESEARCH_LEDGER.md` first.

## Known Open Items (Do Not "Fix" By Re-Pinning)

- **E041 numeric drift (open):** ~133 numeric differences remain; do not re-pin
  `experiments/e041_*.json`. See `ledger/RESEARCH_LEDGER.md` (E049).
- **E042 grid artifacts:** 1-ulp sensitivity can appear; do not re-pin goldens.
- **E030:** numeric diffs on near-zero quantities (documented). Do not re-pin.
- **Data coverage:** Inputs must remain tracked and pinned in
  `ledger/data_baseline.json`. Never re-pin as a side-effect of verification.

## Quick Verification

```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 verify_convention_robustness.py
```
