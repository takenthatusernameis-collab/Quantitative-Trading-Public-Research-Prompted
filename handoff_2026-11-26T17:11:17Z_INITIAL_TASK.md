# Durable Handoff — Initial Task for Next Agentic Work Session

**Timestamp:** 2026-11-26T17:11:17Z
**HEAD:** `2590aef0` (`main`, tracking `origin/main`)
**Working tree:** clean except tracked build noise `src/__pycache__/cache_keys.cpython-312.pyc` (safe to ignore / `git restore`).
**Research phase:** CLOSED (E001–E043; surviving validated strategies in `ledger/RESEARCH_LEDGER.md`).
**Dependencies:** NOT importable this session (`import numpy` → `ModuleNotFoundError`). Run `pip install -r requirements.txt` before any verification.
**Live verification:** none in progress (`.verify_snapshot/` and `.verify_reports/` absent).

---

## Initial task (do ONE, in priority order)

### 1. Verify-and-stop (highest value, ~8–21 min)
```bash
pip install -r requirements.txt
SEED=42 bash scripts/check.sh                      # fast: goldens clean, golden baseline, data coverage, optimizer determinism
SEED=42 python3 run_all_verification.py --extended # 26 drivers vs committed goldens, numeric_tol=1e-4
```
- Expected: all 18 extended drivers reproduce with **0 differences** (last measured 2026-11-23T05:17Z, numpy 2.5.4 / scipy 1.18.1).
- Writes `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json` (gitignored, outside `experiments/`).
- **Do NOT re-pin goldens** to silence drift — none remains. Re-pin only for a deliberate code change recorded in the ledger first (E050 precedent).

### 2. Confirm E049/E050 tangency-QP fix holds (targeted, ~2 min after deps)
```bash
SEED=42 python3 experiments/run_e041.py            # market-neutral portfolio (REJECTED 3/5)
SEED=42 python3 experiments/run_e042.py --n-sim 2  # min-var confirmatory (PARTIAL 4/5, lead artifact)
```
- E041 numeric diffs went 354 → 133 → **0** after the E050 exact active-set solver (commit `72dc947`). Both must stay bit-reproducible.

### 3. If both pass, stop and report
- Report drift precisely (per-driver differences, numeric vs structural, worst drift as multiple of tolerance).
- No new research: the phase is closed. Do not start new experiments.

---

## Integrity rules (do not violate)

1. Never leave verification half-finished — it overwrites `experiments/*.json` and restores after. Recover with `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout <pinned-commit> -- experiments/<file>`; the pinned commit is the last one whose SHA-256 matches `ledger/golden_baseline.json`).
2. Golden baseline SHA-256 is pinned in `ledger/golden_baseline.json`; data inputs in `ledger/data_baseline.json`. Do not re-pin as a side effect of verification.
3. Never commit verification output — it silently replaces the canonical baseline (see reverted commits `d6042b0`/`9f20def`→`05b5353`, `1623923`→`026d109`, `701ed78`→`34396a9`).
4. CI gate cannot be created by agents — template at `.github/workflow-templates/verification-gate.yml`; a maintainer must create the real workflow via the GitHub UI.

## Quick reference
```bash
pip install -r requirements.txt
SEED=42 bash scripts/check.sh
SEED=42 python3 run_all_verification.py            # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended # ~21 min, 26 drivers
SEED=42 python3 run_all_verification.py --restore-only
```

**Next session:** install deps → run Task 1 → report drift precisely → stop. Do not refresh this handoff unless the state materially changes.

(End of file)
