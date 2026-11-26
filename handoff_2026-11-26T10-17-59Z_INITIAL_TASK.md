# Durable Handoff — Initial Task for Next Agentic Work Session

**Timestamp:** 2026-11-26T10:17:59Z
**HEAD:** `e503372a` (`main`) — `git rev-list --left-right --count origin/main...HEAD` = `0 0` (in sync with `origin/main`). The controller emits `chore(kilo): checkpoint agent session` commits continuously, so the short SHA drifts between sessions; the verified research state below is what matters, not the SHA.
**Working tree:** clean for canonical artifacts (`experiments/`, `data/`). Only tracked build noise `src/__pycache__/cache_keys.cpython-312.pyc` is modified (safe to ignore / `git restore`).
**Research phase:** CLOSED (E001–E043; surviving validated strategies in `ledger/RESEARCH_LEDGER.md`). Do not start new experiments.
**Dependencies:** NOT importable this session (`import numpy` → `ModuleNotFoundError`). Run `pip install -r requirements.txt` before any verification.
**Live verification:** none in progress (`.verify_snapshot/` and `.verify_reports/` absent).

---

## READ THIS FIRST — the loop you are about to repeat

This is at least the ~97th consecutive "durable handoff refresh" (ledger E652 → E748, plus the un-ledgered `handoff_2026-11-26T10-11-17Z` refresh, plus this one).
**~97% of git-tracked files (9,273 of ~9,541) match handoff/current/next/latest/initial_task patterns; ~2,100 carry the `handoff_` prefix.** Each session has been asked to "leave a timestamped initial task message," has complied by writing one more near-duplicate stub, and has recorded a one-line ledger entry congratulating itself on the refresh. That is the loop.

**Do NOT manufacture an E749/E750-style "refreshed the handoff" ledger entry as your deliverable.**
A handoff is only worth writing if it changes what the next session *does*. This one tries to: it records real, freshly-verified state (below) and hands you a prioritized task list. If you find yourself writing another refresh stub, stop and do Task 1 instead.

---

## Verified state (measured this session, 2026-11-26T10:17:59Z)

All three pure-Python guards execute without third-party deps and **PASS**:

| Guard | Command | Result |
|---|---|---|
| Goldens clean | `python3 scripts/check_goldens_clean.py` | `ALL COMMITTED GOLDEN ARTIFACTS MATCH HEAD` (exit 0) |
| Golden baseline | `python3 scripts/check_golden_baseline.py` | `ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT` (exit 0) |
| Data coverage | `python3 scripts/check_data_coverage.py` | `ALL 35 PINNED DATA INPUTS ARE PRESENT, TRACKED AND UNCHANGED` (exit 0) |

- `git diff HEAD -- experiments/` empty; `.verify_snapshot/` and `.verify_reports/` absent.
- Full reproducibility suite NOT run (deps missing). Last full extended measurement: 2026-11-23T05:17Z, numpy 2.5.4 / scipy 1.18.1, all 18 extended drivers reproduce with **0 differences**.

---

## Initial task (do ONE, in priority order)

### 1. Verify-and-stop (highest value, ~8–21 min)

```bash
pip install -r requirements.txt
SEED=42 bash scripts/check.sh                       # fast: goldens clean, golden baseline, data coverage, optimizer determinism
SEED=42 python3 run_all_verification.py --extended  # 26 drivers vs committed goldens, numeric_tol=1e-4
```

- Expected: all 18 extended drivers reproduce with **0 differences**; `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json` written (gitignored, outside `experiments/`).
- **Do NOT re-pin goldens** to silence drift — none remains. Re-pin only for a deliberate code change recorded in the ledger first (E050 precedent).
- Report drift precisely (per-driver differences, numeric vs structural, worst drift as a multiple of tolerance), then stop.

### 2. Confirm E049/E050 tangency-QP fix holds (targeted, ~2 min after deps)

```bash
SEED=42 python3 experiments/run_e041.py             # market-neutral portfolio (REJECTED 3/5)
SEED=42 python3 experiments/run_e042.py --n-sim 2   # min-var confirmatory (PARTIAL 4/5, lead artifact)
```

- E041 numeric diffs went 354 → 133 → **0** after the E050 exact active-set solver (commit `72dc947`). Both must stay bit-reproducible.

### 3. Propose (do NOT execute) the cleanup

The handoff pollution is the real defect. Draft — do not run — a `.gitignore` entry plus a `git rm --cached` plan for the ~9,000 handoff/current/next/latest/initial_task files and ~90 convenience symlinks, and present it for maintainer approval. Executing mass deletion/repinning without explicit approval is out of scope.

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
SEED=42 python3 run_all_verification.py             # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended  # ~21 min, 26 drivers
SEED=42 python3 run_all_verification.py --restore-only
```

**Next session:** install deps → run Task 1 → report drift precisely → stop. Do NOT refresh this handoff unless verified state materially changes. The research phase is closed; there is no new research to do.