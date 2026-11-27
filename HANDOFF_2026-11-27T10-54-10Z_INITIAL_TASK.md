# INITIAL TASK — Handoff for Next Agentic Work Session

**Timestamp (UTC): 2026-11-27T10:54:10Z**
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** main — `e5469ff94347577a58a9e4004c7e63bed9566596` (2026-11-27 10:52:44 +0000)
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## State at handoff (verified live, not assumed)

- **Interrupted verification run RECOVERED.** `.verify_snapshot/` held a stale
  `ACTIVE.json` (pid 124131, dead). Ran
  `SEED=42 python3 run_all_verification.py --restore-only`; snapshot removed.
  The snapshot restore produced 5 files differing from HEAD, so
  `git checkout -- experiments/` was run to return the tree to HEAD.
- **Working tree clean vs HEAD** for `experiments/`, `data/`, `ledger/`.
- **Goldens vs HEAD:** `scripts/check_goldens_clean.py` → ALL MATCH HEAD.
- **Data coverage:** `scripts/check_data_coverage.py` → all 35 pinned inputs
  present, tracked, unchanged.
- **PRE-EXISTING BASELINE MISMATCH (not caused this session):**
  `scripts/check_golden_baseline.py` reports 5 artifacts where HEAD differs
  from the SHA-256 pinned in `ledger/golden_baseline.json` — i.e. HEAD carries
  a captured run for these 5 files:
  - `experiments/cointegration_large_liquid.json`
  - `experiments/dollar_neutral_lowbeta_large_liquid.json`
  - `experiments/e037_portfolio.json`
  - `experiments/e042_lead_config_confirmatory.json`
  - `experiments/pairs_large_liquid.json`

## CLEAR INITIAL TASK (do this first, then stop and await direction)

1. **Do NOT re-pin or re-run verification as a side effect.** The committed
   golden is the authoritative record; re-pinning requires a deliberate,
   ledger-recorded change first (AGENTS.md).
2. **Resolve the 5-artifact baseline mismatch deliberately.** The pinned
   artifacts are recoverable from the last commit whose SHA-256 matches
   `ledger/golden_baseline.json` (per AGENTS.md recovery rule):
   - `cointegration_large_liquid.json`, `pairs_large_liquid.json` → `da00bd0d`
   - `dollar_neutral_lowbeta_large_liquid.json` → `bf429169`
   - `e037_portfolio.json`, `e042_lead_config_confirmatory.json` → `c5038332`
   Restore with `git checkout <commit> -- experiments/<file>` for each, then
   re-run `SEED=42 python3 scripts/check_golden_baseline.py` to confirm 0
   mismatches. Do NOT use `--update` unless the user explicitly approves a
   baseline change and it is recorded in the ledger first.
3. **Confirm clean state** — `git status --short experiments/ data/ ledger/`
   empty; `SEED=42 python3 scripts/check_goldens_clean.py` and
   `check_golden_baseline.py` both green.
4. **Optional fast sanity check** — `SEED=42 bash scripts/check.sh`
   (offline, seconds). Only run the full/extended suite if the user asks.
5. **Read `ledger/RESEARCH_LEDGER.md`** for surviving validated strategies and
   closed items (E049/E050 optimizer determinism + exact KKT enumeration;
   E041/E042 ill-conditioned-QP drift — all closed, artifacts reproduce 0
   diffs). Research phase E001–E043 is complete.
6. If this session hands off again, write its own timestamped durable handoff
   following this filename pattern and update `handoff_CURRENT` /
   `handoff_LATEST` symlinks.

## Key Constraints (from AGENTS.md)

- `experiments/*.json` are committed goldens; never commit verification output
  or leave a run half-finished. Recover with `--restore-only`.
- Golden baseline: `scripts/check_golden_baseline.py` vs
  `ledger/golden_baseline.json`. Data coverage: `scripts/check_data_coverage.py`
  vs `ledger/data_baseline.json`.
- Optimizer: validate on problem constraints, not solver exit status
  (`tests/test_portfolio_opt.py`, ledger E049/E050).
- Always `SEED=42`. Close-to-close is the v1.2.3 primary convention.
- CI workflow cannot be created by automated agents; use local
  `make check/verify/*`.

## Provenance

Supersedes prior INITIAL_TASK handoffs (most recent prior:
`handoff_2026-11-27T10-52-23Z_INITIAL_TASK.md`). This file is the authoritative
initial-task message for the next session. Written 2026-11-27T10:54:10Z.