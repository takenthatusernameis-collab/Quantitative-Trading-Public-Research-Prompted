# Durable Handoff — Initial Task for Next Agentic Work Session

**Timestamp:** 2026-11-26T09:15:19Z
**HEAD:** `500917dc` (`main`) == `origin/main` (`git rev-list --left-right --count origin/main...HEAD` = `0 0`). The controller emits `chore(kilo): checkpoint agent session` commits continuously, so the short SHA drifts; the verified state below is what matters.
**Working tree:** clean for canonical artifacts (`experiments/`, `data/`). Only tracked build noise `src/__pycache__/cache_keys.cpython-312.pyc` is modified (ignore / `git restore`).
**Research phase:** CLOSED (E001–E043; survivors in `ledger/RESEARCH_LEDGER.md`). Do not start new experiments.
**Dependencies:** NOT importable (`import numpy` → `ModuleNotFoundError`). Run `pip install -r requirements.txt` first.
**Live verification:** none (`.verify_snapshot/` and `.verify_reports/` absent).

---

## READ FIRST — do not repeat the loop

This is the ~96th consecutive "durable handoff refresh" (ledger E652 → E747, plus this one). The `handoff_`-prefixed tracked-file count has grown to **7,334 of 9,541** (~77%; counting all handoff/current/next/latest/initial_task aliases it is ~97%). Each session writes one more near-duplicate stub and a self-congratulatory ledger line. **Do NOT manufacture an E748-style "refreshed the handoff" entry as your deliverable.** A handoff is only worth writing if it changes what the next session *does*. This one records freshly-verified state and a prioritized task list; if you catch yourself writing another refresh stub, stop and do Task 1.

## Verified state (measured 2026-11-26T09:15:19Z)

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
SEED=42 bash scripts/check.sh                       # fast: goldens clean, baseline, data coverage, optimizer determinism
SEED=42 python3 run_all_verification.py --extended  # 26 drivers vs committed goldens, numeric_tol=1e-4
```
Expected: all 18 extended drivers reproduce with **0 differences**; `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json` written (gitignored, outside `experiments/`). **Do NOT re-pin goldens** to silence drift — none remains; re-pin only for a deliberate code change recorded in the ledger first (E050 precedent). Report drift precisely (per-driver diffs, numeric vs structural, worst drift as a multiple of tolerance), then stop.

### 2. Confirm E049/E050 tangency-QP fix holds (targeted, ~2 min after deps)
```bash
SEED=42 python3 experiments/run_e041.py             # market-neutral portfolio (REJECTED 3/5)
SEED=42 python3 experiments/run_e042.py --n-sim 2   # min-var confirmatory (PARTIAL 4/5, lead artifact)
```
E041 numeric diffs went 354 → 133 → **0** after the E050 exact active-set solver (commit `72dc947`). Both must stay bit-reproducible.

### 3. Propose (do NOT execute) the cleanup
The handoff pollution is the real defect. Draft — do not run — a `.gitignore` entry plus a `git rm --cached` plan for the ~7,300 `handoff_` files (and the alias/mirror dirs), and present it for maintainer approval. Mass deletion/repinning without explicit approval is out of scope.

## Integrity rules (do not violate)
1. Never leave verification half-finished — it overwrites `experiments/*.json` and restores after. Recover with `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout <pinned-commit> -- experiments/<file>`; pinned commit = last whose SHA-256 matches `ledger/golden_baseline.json`).
2. Golden baseline SHA-256 pinned in `ledger/golden_baseline.json`; data inputs in `ledger/data_baseline.json`. Do not re-pin as a side effect of verification.
3. Never commit verification output — it silently replaces the canonical baseline (reverted commits `d6042b0`/`9f20def`→`05b5353`, `1623923`→`026d109`, `701ed78`→`34396a9`).
4. CI gate cannot be created by agents — template at `.github/workflow-templates/verification-gate.yml`; a maintainer must create the real workflow via the GitHub UI.

## Quick reference
```bash
pip install -r requirements.txt
SEED=42 bash scripts/check.sh
SEED=42 python3 run_all_verification.py             # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended  # ~21 min, 26 drivers
SEED=42 python3 run_all_verification.py --restore-only
```

**Next session:** install deps → run Task 1 → report drift precisely → stop. Do NOT refresh this handoff unless verified state materially changes. Supersedes `handoff_2026-11-26T09-14-34Z_INITIAL_TASK.md` (E747). No new aliases or mirror dirs created (continuing the E740–E747 break of the mirror/repoint explosion). The research phase is closed; there is no new research to do.