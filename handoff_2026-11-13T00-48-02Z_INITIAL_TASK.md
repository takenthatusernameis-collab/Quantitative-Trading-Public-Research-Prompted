# Durable Handoff — Initial Task Message

**Timestamp (UTC):** 2026-11-13T00:48:02Z
**To:** Next Agentic Work Session
**From:** Session at HEAD `e8b70699` (Kilo)
**Artifact:** `handoff_2026-11-13T00-48-02Z_INITIAL_TASK.md`

---

## 1. Purpose

This is a timestamped, durable handoff for the next agentic work session. It
records the verified repository state at handoff time so the next session can
resume without re-deriving it. It is written outside `experiments/` and never
captures verification output.

## 2. Verified State at Handoff

- **Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
- **HEAD:** `e8b70699c1eae201e4ed1c3e4ff4b895d079b55c` — `chore(kilo): checkpoint agent session` (2026-11-13 00:47:54 +0000) on `main`, in sync with `origin/main` (`+0 -0`).
- **Working tree:** 1 modification only — `src/__pycache__/cache_keys.cpython-312.pyc` (tracked binary bytecode, 3462 bytes). This is a stale `__pycache__` build artifact, not research/source substance.
- **Interrupted verification:** none. `.verify_snapshot/` absent → no recovery needed.
- **Experiments inventory:** `git ls-files experiments/` → 138 tracked entries (107 goldens + 31 drivers).
- **Baseline guards (re-run this session):**
  - `python3 scripts/check_golden_baseline.py` → **ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT**
  - `python3 scripts/check_data_coverage.py` → **ALL 35 PINNED DATA INPUTS ARE PRESENT, TRACKED AND UNCHANGED**
  - `git diff HEAD -- experiments/ data/` → empty.

## 3. Delta vs Prior Durable Handoff

- Prior handoff: E192, HEAD `850a837b`, artifact `handoff_2026-11-13T00-47-20Z_INITIAL_TASK.md` (read and superseded).
- `git diff --name-only 850a837b..HEAD` → 1 path: `src/__pycache__/cache_keys.cpython-312.pyc` (stale bytecode only).
- `git diff --name-only 850a837b..HEAD -- experiments/ data/ src/ tests/` → **0 paths** (excludes `__pycache__`).
- **Conclusion:** no research, source, data, experiment, or baseline substance changed since the prior handoff.

## 4. Project Status

- **Research phase complete** (E001–E043). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.
- **Last substantive research entry:** E051. Entries E052 onward are durable-handoff refreshes only.
- This handoff corresponds to ledger entry **E193** (durable-handoff refresh).

## 5. Instructions for the Next Session

1. Read `ledger/RESEARCH_LEDGER.md` (especially the latest entries) and `AGENTS.md`.
2. Confirm the guards above still pass before any work:
   ```bash
   SEED=42 python3 scripts/check_golden_baseline.py
   SEED=42 python3 scripts/check_data_coverage.py
   ```
3. If a concrete task is assigned, follow project conventions in `AGENTS.md` (pre-registration, multiple-testing discipline, golden-file integrity, `SEED=42`).
4. Do not commit verification output; if a run is interrupted, restore with `SEED=42 python3 run_all_verification.py --restore-only`.
5. If no task is assigned, await further instructions.

## 6. Reproduction / Verification Commands

```bash
# Fast convention-robustness check + template validation (seconds, offline)
SEED=42 bash scripts/check.sh          # or: make check

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min; all committed drivers, structural match)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --full
```

## 7. Guardrails

- Use `SEED=42`. Never move pre-registered goalposts, gates, falsification expectations, or sensitivity grids.
- `experiments/*.json` are canonical; never re-pin goldens as a side effect of verification.
- Never commit verification output or `src/__pycache__/` bytecode.
- Keep this handoff outside `experiments/`.

---

*Durable handoff created at session start for continuity. Timestamp 2026-11-13T00:48:02Z.*