# Durable Handoff — Next Agentic Work Session

**Timestamp:** 2026-10-31T03:12:19Z
**Branch:** `main`
**HEAD:** `f689232`
**Working tree:** baseline restored (3 goldens match pinned fingerprint); only `__pycache__` artifacts modified (untracked noise).
**Verification snapshot:** none active (`.verify_snapshot/` absent)

---

## INITIAL TASK (do first)

**Confirm baseline integrity before making any changes or running verification.**

1. Run `SEED=42 bash scripts/check.sh` — expect exit 0.
2. If `check_goldens_clean` reports the 3 restored goldens differing from HEAD, that is expected: HEAD is a checkpoint commit; the pinned baseline in `ledger/golden_baseline.json` is authoritative. Do NOT `git checkout -- experiments/`.
3. If any pinned artifact differs from its fingerprint, restore from the matching commit; never re-pin without explicit justification.
4. After green checks, idle awaiting explicit user direction. Do not modify goldens, re-pin baselines, or run extended/full verification without explicit instruction.

---

## Current state

- 3 goldens restored to pinned baseline: `experiments/cointegration_large_liquid.json`, `experiments/dollar_neutral_lowbeta_large_liquid.json`, `experiments/pairs_large_liquid.json`.
- Manifests untouched (`ledger/golden_baseline.json`, `ledger/data_baseline.json`).
- No source or data changes.
