# Durable Handoff — Initial Task for the Next Agentic Work Session

**Timestamp:** 2026-11-26T17:15:50Z
**HEAD:** `35046006` (`main`, in sync with `origin/main`; `git rev-list --left-right --count origin/main...HEAD` = `0 0`)
**Working tree:** clean except tracked build noise `src/__pycache__/cache_keys.cpython-312.pyc` (safe to ignore / `git restore`).
**Research phase:** CLOSED (E001–E043; surviving validated strategies in `ledger/RESEARCH_LEDGER.md`).
**Dependencies:** NOT importable this session (`import numpy` → `ModuleNotFoundError`). Run `pip install -r requirements.txt` before any verification.
**Live verification:** none in progress (`.verify_snapshot/` and `.verify_reports/` absent; `git diff HEAD -- experiments/` empty).

---

## Read this first — the repo is in a handoff loop

This file is the deliverable you asked for, but it is also unavoidably another entry in the
**E652–E750 runaway handoff-refresh loop** documented in `ledger/RESEARCH_LEDGER.md`.
Measured this session: **9,058 of 9,601 git-tracked files (≈94%) carry the `handoff_` prefix.**
The research itself has been closed since E043; everything after E051 is bookkeeping churn.

**Do NOT manufacture another handoff refresh as a substitute for real work.** If you catch
yourself writing a handoff file, stop — that is the loop, not progress. The single most
valuable action is one of the real-work items below, or *proposing* (not executing) the
cleanup that ends the loop.

To avoid feeding the explosion, this refresh **creates exactly one file and repoints only the
three pre-existing canonical symlinks** (`HANDOFF_CURRENT`, `HANDOFF_LATEST`, `HANDOFF_LATEST.md`).
No new alias symlinks and no mirror directories are created.

---

## Initial task message

You are resuming an independent, reproducible quantitative-strategy research repo
(2014–2026 US equities, futures, macro). **Research phase is COMPLETE (E001–E043)**;
surviving validated strategies are in `ledger/RESEARCH_LEDGER.md`. Your job is to
**preserve the verified baseline and only add pre-registered work** — never silently
mutate canonical artifacts.

Golden rule: `experiments/*.json` are the authoritative record. Re-pin a golden
(`scripts/check_golden_baseline.py --update`, `scripts/check_data_coverage.py --update`)
**only** for a deliberate, ledger-recorded code/data change — never as a side effect of
running verification, and never to silence a tolerance violation.

---

## Prioritized real-work task list (do ONE, in order — not another handoff)

### 1. Verify-and-stop (highest value, ~8–21 min)
```bash
pip install -r requirements.txt
SEED=42 bash scripts/check.sh                       # fast: goldens clean, golden baseline, data coverage, optimizer determinism
SEED=42 python3 run_all_verification.py --extended  # 26 drivers vs committed goldens, numeric_tol=1e-4
```
- Expected: all 18 extended drivers reproduce with **0 differences** (last measured 2026-11-23T05:17Z, numpy 2.5.4 / scipy 1.18.1).
- Writes `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json` (gitignored, outside `experiments/`).
- **Do NOT re-pin goldens** to silence drift — none remains. Re-pin only for a deliberate code change recorded in the ledger first (E050 precedent).

### 2. Confirm the E049/E050 tangency-QP fix holds (targeted, ~2 min after deps)
```bash
SEED=42 python3 experiments/run_e041.py            # market-neutral portfolio (REJECTED 3/5)
SEED=42 python3 experiments/run_e042.py --n-sim 2  # min-var confirmatory (PARTIAL 4/5, lead artifact)
```
- E041 numeric diffs went 354 → 133 → **0** after the E050 exact active-set solver (commit `72dc947`). Both must stay bit-reproducible.

### 3. If both pass, stop and report
- Report drift precisely (per-driver differences, numeric vs structural, worst drift as a multiple of the 1e-4 tolerance).
- No new research: the phase is closed. Do not start new experiments.

### 4. (Only if 1–3 are done) Propose — do not execute — the loop-ending cleanup
- A `.gitignore` entry for `handoff_*` / `*_LATEST*` / `*_CURRENT*` plus `git rm --cached` of the ~9,000 tracked handoff files, leaving canonical `experiments/`, `ledger/`, `src/`, `scripts/`, `data/` pins intact. Present the plan and wait for explicit approval.

---

## Integrity rules (do not violate)

1. Never leave verification half-finished — it overwrites `experiments/*.json` and restores after. Recover with `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout <pinned-commit> -- experiments/<file>`; the pinned commit is the last one whose SHA-256 matches `ledger/golden_baseline.json`).
2. Golden baseline SHA-256 is pinned in `ledger/golden_baseline.json`; data inputs in `ledger/data_baseline.json`. Do not re-pin as a side effect of verification.
3. Never commit verification output — it silently replaces the canonical baseline (see reverted commits `d6042b0`/`9f20def`→`05b5353`, `1623923`→`026d109`, `701ed78`→`34396a9`).
4. CI gate cannot be created by agents — template at `.github/workflow-templates/verification-gate.yml`; a maintainer must create the real workflow via the GitHub UI.

## Quick reference (SEED=42 always)
```bash
pip install -r requirements.txt
SEED=42 bash scripts/check.sh
SEED=42 python3 run_all_verification.py            # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended # ~21 min, 26 drivers
SEED=42 python3 run_all_verification.py --restore-only
```

**Next session:** install deps → run Task 1 → report drift precisely → stop. Do not write another handoff. Do not commit until `make check` is green and `experiments/` is unchanged.

(End of file)