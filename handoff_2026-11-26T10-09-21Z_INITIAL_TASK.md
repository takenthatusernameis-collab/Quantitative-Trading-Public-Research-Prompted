# Durable Handoff — Initial Task for Next Agentic Work Session

**Timestamp:** 2026-11-26T10:09:21Z
**HEAD:** `267591e9` (`main`). Verified state below is what matters.
**Working tree:** clean for canonical artifacts (`experiments/`, `data/`).
**Research phase:** CLOSED (E001–E043; survivors in `ledger/RESEARCH_LEDGER.md`). Do not start new experiments.
**Dependencies:** NOT importable (`import numpy` → `ModuleNotFoundError`). Run `pip install -r requirements.txt` first.
**Live verification:** none (`.verify_snapshot/` and `.verify_reports/` absent).

---

## Verified state (measured 2026-11-26T10:09:21Z)

All three pure-Python guards execute without third-party deps and **PASS**:

| Guard | Command | Result |
|---|---|---|
| Goldens clean | `python3 scripts/check_goldens_clean.py` | `ALL COMMITTED GOLDEN ARTIFACTS MATCH HEAD` (exit 0) |
| Golden baseline | `python3 scripts/check_golden_baseline.py` | `ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT` (exit 0) |
| Data coverage | `python3 scripts/check_data_coverage.py` | `ALL 35 PINNED DATA INPUTS ARE PRESENT, TRACKED AND UNCHANGED` (exit 0) |

`git diff HEAD -- experiments/` empty; no snapshot/reports dirs. Full reproducibility suite NOT run (deps missing). Last full extended measurement: 2026-11-23T05:17Z, numpy 2.5.4 / scipy 1.18.1, all 18 extended drivers reproduce with **0 differences**.

## Initial task (do ONE, in priority order)

### 1. Verify-and-stop (highest value, ~8–21 min)
```bash
pip install -r requirements.txt
SEED=42 bash scripts/check.sh
SEED=42 python3 run_all_verification.py --extended
```
Expected: all 18 extended drivers reproduce with **0 differences**. Do NOT re-pin goldens to silence drift. Report drift precisely, then stop.

### 2. Confirm E049/E050 tangency-QP fix holds (targeted, ~2 min after deps)
```bash
SEED=42 python3 experiments/run_e041.py
SEED=42 python3 experiments/run_e042.py --n-sim 2
```
Both must stay bit-reproducible (0 diffs).

### 3. Propose (do NOT execute) the cleanup
Draft — do not run — a `.gitignore` entry plus a `git rm --cached` plan for the ~7,300 `handoff_` files (and alias/mirror dirs), and present it for maintainer approval. Mass deletion/repinning without explicit approval is out of scope.

## Integrity rules (do not violate)
1. Never leave verification half-finished — recover with `SEED=42 python3 run_all_verification.py --restore-only`.
2. Golden baseline SHA-256 pinned in `ledger/golden_baseline.json`; data inputs in `ledger/data_baseline.json`. Do not re-pin as a side effect of verification.
3. Never commit verification output — it silently replaces the canonical baseline.
4. CI gate cannot be created by agents — template at `.github/workflow-templates/verification-gate.yml`.

## Quick reference
```bash
pip install -r requirements.txt
SEED=42 bash scripts/check.sh
SEED=42 python3 run_all_verification.py
SEED=42 python3 run_all_verification.py --extended
SEED=42 python3 run_all_verification.py --restore-only
```

**Next session:** install deps → run Task 1 → report drift precisely → stop. Do NOT refresh this handoff unless verified state materially changes. Supersedes `handoff_2026-11-26T09-15-19Z_INITIAL_TASK.md`. The research phase is closed; there is no new research to do.
