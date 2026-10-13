# Handoff for Next Agent (Post Data-Vintage Freeze Verification + E042b Lead Confirmatory)

## Session Summary

**Date**: 2026-10-13
**Goal**: Execute/verify the prior agent's assigned task (freeze the data vintage for
calendar-independent reproduction) and, since the prior agent declared the research
archive "closed," run the strongest documented lead through the full gate set to test
that closure claim against real evidence rather than trusting it.

**Bottom line**: The data-vintage freeze is **implemented and verified to work
end-to-end** (offline, calendar-independent with `SEED=42`). The full reproduction
suite (`run_all_verification.py --full`) **passes with exact golden match** on all
4 checks. The market-neutral-total-portfolio line is **confirmed closed**: the
strongest non-primary sensitivity-grid lead fails the G2 placebo-significance gate.

---

## What Changed This Session

The prior agent's working-tree changes (staged, **not committed** — see
"Durability note" below) were **verified**, not authored, by me. I made two
additions:

1. **`experiments/run_e042_lead.py`** (new) — a faithful, reusable driver that
   reuses `experiments/run_e042.py`'s exact component builders, blend evaluator,
   walk-forward cadence, and the matched G2 beta-constrained placebo null, applied
   to a single pre-specified sensitivity-grid lead config. No reimplementation of
   the strategy/backtest layer.
2. **`experiments/e042_lead_config_confirmatory.json`** (new, generated) —
   machine-readable gate results for the lead config.
3. **`ledger/RESEARCH_LEDGER.md`** — appended `§E042b` (unstaged) documenting the
   confirmatory run in the established ledger format.

I did **not** modify any committed golden experiment JSON, `src/data.py`,
`src/portfolio_opt.py`, or the strategy/backtest layer.

---

## What Was Actually Verified (evidence, not claims)

I do **not** trust the prior agent's "ALL CHECKS PASSED" / "no code changes
required" text (the prior agent's own `src/data.py` diff shows 47 insertions
that ARE the freeze, contradicting its "no code changes" line). I ran everything:

| Check | Command | Result |
|-------|---------|--------|
| Vintage resolution | `SEED=42 python3 -c "data._resolve_end_date()"` | `2026-10-13` (from `data/vintages.json`) ✓ |
| Cache hit (offline) | `data_cache_ok()` (large_liquid parquet) | EXISTS, no network needed ✓ |
| Fast convention check | `verify_convention_robustness.py` | exit 0, all 7 asserts PASS ✓ |
| **Quick end-to-end** | `run_all_verification.py` (n_sim=2) | **ALL 4 PASS** ✓ |
| **Full end-to-end** | `run_all_verification.py --full` (n_sim=50) | **ALL 4 PASS** ✓ |
| E042 deterministic goldens | deep-compare (excl. timestamp) | `e042_minvar_market_neutral.json` EXACT, `e042_sensitivity_grid.json` EXACT ✓ |
| E042 primary placebo | fresh n_sim=50 run | z=1.95 (FAIL), β=+0.094, 4/5 PARTIAL — matches committed golden ✓ |
| batch_run / validate | fresh vs golden (`*_large_liquid.json`, `validation_summary.json`) | EXACT match (excl. timestamp) ✓ |
| **E042b lead confirmatory** | `python3 experiments/run_e042_lead.py` | 4/5 gates, G2 z=**1.50** FAIL, REJECTED ✓ |

Reproduction commands (require the cached `data/*.parquet` vintage + `SEED=42`):
```bash
SEED=42 python3 run_all_verification.py        # quick  (~12s)
SEED=42 python3 run_all_verification.py --full # full  (~100s)
SEED=42 python3 experiments/run_e042_lead.py   # confirmatory (~10s)
```
All runs hit the local parquet cache (verified cache-present); the FRED/yfinance
download path exists as a fallback but was not exercised.

### Note on a real discrepancy
The prior agent's `verify_convention_robustness.py` asserts `abs(overnight - 1.289) < 0.01`
for DN Low-Beta (E013), but the committed JSON holds `1.287`. It passes only on the
`0.01` tolerance (off by 0.002). This is a latent fragility in the verification
script's tolerance, not a strategy error — recorded here for the next agent; do
**not** loosen it silently.

---

## What Remains Unresolved

- **Market-neutral total portfolio: CLOSED (now doubly confirmed).**
  - Primary min_var (β≤0.05): z=1.95, 4/5 — fails G2 (E042 committed golden).
  - Strongest non-primary sensitivity-grid lead (max_sharpe, β≤0.1, 63d,
    macro_inclusive_3): z=**1.50**, 4/5 — fails G2 (this session's E042b).
  Both fail **only** on G2 placebo significance; G1/G3/G4/G5 pass. No blend of
  the validated components is simultaneously market-neutral and significant.
- **Free public data sources are exhausted** (yfinance price/volume/dividends,
  FRED macro; fundamentals/options/earnings are data-infeasible — E029/E031/E032/E033).
- **All equity strategies are overnight-concentrated** (E024 audit); futures are
  balanced; macro is overnight-dominated.
- The prior agent's `RELEASE_NOTES.md` lists "Freeze the data vintage" as an
  *optional follow-up*, contradicting its own `HANDOFF.md` claiming it is done.
  **Ground truth: the freeze IS implemented** in `src/data.py` (`_resolve_end_date`
  → `data/vintages.json` when `SEED` set, priority: explicit `end` > `END_DATE` env >
  `vintages.json` > `utcnow`) and **verified working**. The RELEASE_NOTES note is
  stale; no further freeze work is needed.

---

## Approaches Already Failed and Why

- **E041** max_sharpe market-neutral blend: REJECTED (β 0.173 > 0.10; G2 z=-1.29).
- **E042** min_var market-neutral blend (primary confirmatory): PARTIAL 4/5 — G2
  placebo z=1.95 < 3.0 (n_grid=50, SEED=42). Not promoted. (See erratum at
  ledger §E042: an earlier transcription used the n_grid=2000 diagnostic numbers.)
- **E042b** (this session) strongest sensitivity-grid lead — max_sharpe β≤0.1 63d
  macro_inclusive_3: REJECTED 4/5 — G2 placebo z=1.50 < 3.0. Confirms closure.
- Testing the remaining 7 market-neutral grid configs is **not pursued**: it would be
  post-hoc multiple-testing/data-snooping; the single strongest pre-specified lead
  failing G2 is the principled, sufficient falsification. FE2 is also falsified for
  the lead (variance ratio 0.976 > 0.90), an independent signal.
- 11 prior rejected families (stat-arb, equity carry, IVOL, crypto, multi-asset TSM,
  liquidity, realized-vol, extended macro, etc.) are recorded in RELEASE_NOTES §
  "Rejected Families" and ledger §per-experiment. No new free-data angle is viable.

---

## One Precise Next Task (for the following agent)

**Finalize and persist the v1.2.3 release artifact** (the verified baseline currently
exists **only in the working tree, staged/unstaged — not committed**, so it is at risk).

Concrete, bounded steps:
1. **Persist**: commit the staged working-tree changes (the data-vintage freeze in
   `src/data.py`, `data/vintages.json`, `requirements.txt`, `run_all_verification.py`,
   `RELEASE_NOTES.md`, the prior agent's `README.md`/`HANDOFF.md`/ledger edits)
   **plus** my two new files (`experiments/run_e042_lead.py`,
   `experiments/e042_lead_config_confirmatory.json`) and the unstaged `§E042b`
   ledger entry, as a single coherent `v1.2.3` release commit.
2. **Tag**: `git tag v1.2.3` and (optionally) attach `experiments/*.json` as release
   artifacts so the golden baseline is versioned alongside the code.
3. **Lock the release**: resolve the stale `RELEASE_NOTES.md` "optional follow-up:
   Freeze the data vintage" line — replace it with a one-line confirmation that the
   freeze is implemented in `src/data.py` and verified. Fix the `1.287` vs `1.289`
   DN-Low-Beta tolerance fragility (align the asserted target to the committed
   value `1.287`, or widen the tolerance explicitly) so `verify_convention_robustness.py`
   is not latently broken.
4. **Gate**: re-run `SEED=42 python3 run_all_verification.py --full` after the tag.
   Completion criterion: exit 0 with all 4 checks PASS and exact golden match.

**Prerequisite**: this requires commit/tag permission (the repo workflow rules require
explicit user authorization for commits). If a research extension is mandated instead,
the only viable paths are paid/proprietary data (fundamentals, options, earnings,
microstructure) or new instrument classes (crypto/international/fixed-income) — all
outside the free-public-data scope this repository has now fully exhausted.

### Evidence artifacts for the next agent
- `experiments/e042_lead_config_confirmatory.json` — lead-config gates (G2 z=1.50).
- `/tmp/verify_full.log` — full `--full` run output (all PASS).
- `ledger/RESEARCH_LEDGER.md §E042b` — confirmatory record.
- `README.md` §"Market-Neutral Total Portfolio: CLOSED" is **strengthened** by this
  session (now confirmed against the strongest residual lead, not just the primary).

---

## Key Files
- `src/data.py:44-54` — `_resolve_end_date` vintage-pinning priority chain (verified).
- `data/vintages.json` — `default_end_date: "2026-10-13"`.
- `run_all_verification.py` — master driver (snapshot → run → deep-compare → restore).
- `verify_convention_robustness.py` — fast JSON-only convention asserts.
- `experiments/run_e042.py` — primary market-neutral driver; `experiments/run_e042_lead.py`
  reuses its functions for the single-config confirmatory run.
- `experiments/e042_lead_config_confirmatory.json` — new confirmatory result artifact.
