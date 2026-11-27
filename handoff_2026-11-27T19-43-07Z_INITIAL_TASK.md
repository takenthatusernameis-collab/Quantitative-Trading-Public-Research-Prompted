# Durable Handoff — Initial Task for Next Agentic Work Session

**Timestamp:** 2026-11-27T19:43:07Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Working dir:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**HEAD:** `7b143b12` (`chore(kilo): checkpoint agent session`); `git rev-list --left-right --count origin/main...HEAD` = `0 0` (in sync with origin/main).
**Working tree:** clean except untracked `__pycache__/*.pyc` build noise (safe to ignore / `git restore`).
**Research phase:** CLOSED (E001–E043; surviving validated strategies in `ledger/RESEARCH_LEDGER.md`).
**Supersedes:** handoff_2026-11-27T19-38-01Z / CURRENT (19:38:40Z).

---

## READ FIRST — this is NOT a clean baseline (differs from prior handoffs)

Prior handoffs claimed "all guards pass." **That is no longer true.** This session the
golden-baseline guard FAILS:

```
python3 scripts/check_golden_baseline.py   -> EXIT 1
FAIL 5 pinned artifact(s) differ from the pinned baseline
```

The working tree matches HEAD (`check_goldens_clean.py` = PASS), but **HEAD itself
carries 5 artifacts that differ from the SHA-256 pinned in `ledger/golden_baseline.json`.**
This is exactly the "a checkpoint commit replaced the canonical baseline" failure
AGENTS.md warns about (precedent: `d6042b0`/`9f20def`→`05b5353`, `1623923`→`026d109`,
`701ed78`→`34396a9`). The culprit is checkpoint commit **`8cd55e5e`**, which last
touched all 5 files with verification output; the baseline was never re-pinned.

### The 5 drifted artifacts and the last commit whose blob matches the pinned SHA-256

| Artifact | Pinned SHA-256 (prefix) | Last matching commit |
|---|---|---|
| `experiments/cointegration_large_liquid.json` | `a41182528234…` | `da00bd0d` |
| `experiments/dollar_neutral_lowbeta_large_liquid.json` | `c657c3afc38a…` | `bf429169` |
| `experiments/e037_portfolio.json` | `dcaeb797e112…` | `c5038332` |
| `experiments/e042_lead_config_confirmatory.json` | `fa06eeb8403d…` | `c5038332` |
| `experiments/pairs_large_liquid.json` | `5ab39998fc4b…` | `da00bd0d` |

(Recovery commits found by hashing `git show <commit>:<path>` and matching the pin.)

---

## Initial task (do ONE, in priority order)

### 1. Restore the 5 goldens to their pinned baseline (highest value, ~1 min, no deps)
The committed goldens are authoritative; the working tree/HEAD copies are the captured
run. Restore each from the last matching commit above:

```bash
git checkout da00bd0d -- experiments/cointegration_large_liquid.json experiments/pairs_large_liquid.json
git checkout bf429169 -- experiments/dollar_neutral_lowbeta_large_liquid.json
git checkout c5038332 -- experiments/e037_portfolio.json experiments/e042_lead_config_confirmatory.json
python3 scripts/check_golden_baseline.py    # MUST now exit 0 (ALL PINNED ARTIFACTS MATCH)
```
- Do **NOT** run `check_golden_baseline.py --update` to "fix" this — that would re-pin
  the captured run as the new baseline, which is the exact mistake the ledger warns against.
- After restoring, `git diff --stat HEAD -- experiments/` will show these 5 files; that
  diff is the intended repair. Commit only on explicit user direction.

### 2. Provision deps and run extended verification (~21 min)
```bash
pip install -r requirements.txt
SEED=42 bash scripts/check.sh                       # fast guards
SEED=42 python3 run_all_verification.py --extended  # 26 drivers vs committed goldens, numeric_tol=1e-4
```
- Expected after restore: all 18 extended drivers reproduce with 0 differences
  (last clean measurement 2026-11-23T05:17Z, numpy 2.5.4 / scipy 1.18.1).
- Writes `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json` (gitignored, outside `experiments/`).
- **If the suite is interrupted**, recover with `SEED=42 python3 run_all_verification.py --restore-only`
  (or re-run the `git checkout <commit> -- experiments/<file>` commands above). Never leave it half-finished.

### 3. Confirm E041/E042 tangency-QP drift stays closed (targeted, ~2 min)
```bash
SEED=42 python3 experiments/run_e041.py            # REJECTED 3/5
SEED=42 python3 experiments/run_e042.py --n-sim 2  # PARTIAL 4/5, lead artifact
```
- E041 numeric diffs went 354 → 133 → 0 after the E050 exact KKT active-set solver
  (commit `72dc947`). Must stay bit-reproducible. Do **not** re-pin to silence drift.

### 4. Only if 1–3 pass: stop and report
- Report per-driver differences (numeric vs structural, worst drift as multiple of tolerance).
- No new research — the phase is closed. Do not start new experiments.
- Do NOT manufacture another handoff refresh as a substitute for work (see loop note below).

---

## The runaway handoff loop (do not feed it)

This repo is ~94% `handoff`-prefixed files (thousands in root + mirror dirs under `.kilo/`).
Handoff refreshes run E652–E775. **This handoff is itself an instance of that loop.** It is
justified only because the baseline is genuinely broken this session (real finding, not
bookkeeping). Do NOT write an E776-style refresh unless state materially changes again.
A handoff-file cleanup is *proposed* (not executed) as task 4 in prior handoffs; it still
needs explicit user approval before deleting anything.

## Integrity rules (do not violate)

1. `experiments/*.json` are canonical goldens — never commit verification output over them.
2. Golden SHA-256 pinned in `ledger/golden_baseline.json`; data inputs in `ledger/data_baseline.json`. Never re-pin as a side effect of verification.
3. Cache coverage enforced: every `data.download()` call site needs a pinned, git-tracked cache entry.
4. CI gate cannot be created by agents — template at `.github/workflow-templates/verification-gate.yml`; a maintainer must create the real workflow via the GitHub UI.
5. Always run with `SEED=42`. `python3 -m py_compile` any changed Python file. `cvxpy`/`cvxopt` optional (scipy fallback).

## Quick reference
```bash
pip install -r requirements.txt
SEED=42 bash scripts/check.sh
SEED=42 python3 run_all_verification.py            # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended # ~21 min, 26 drivers
SEED=42 python3 run_all_verification.py --restore-only
python3 scripts/check_golden_baseline.py           # currently FAILS until task 1 is done
```

**Next session:** do Task 1 first (restore the 5 goldens — the baseline is broken), then
Task 2/3, report drift precisely, stop. Do not refresh this handoff unless state materially changes.

(End of file)