# Durable Handoff — Initial Task Message

**Timestamp (UTC):** 2026-11-13T00:50:24Z
**To:** Next Agentic Work Session
**From:** Session at HEAD `33be527e` (Kilo)
**Artifact:** `handoff_2026-11-13T00-50-24Z_INITIAL_TASK.md`

---

## 1. Purpose

This is a timestamped, durable handoff for the next agentic work session. It
records the verified repository state at handoff time so the next session can
resume without re-deriving it. It is written outside `experiments/` and never
captures verification output.

## 2. Verified State at Handoff

- **Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
- **HEAD:** `33be527e23645d7d47543fc8c297214f3a99cc21` — `chore(kilo): checkpoint agent session` (2026-11-13 00:49:57 +0000) on `main`, in sync with `origin/main` (`+0 -0`).
- **Working tree:** 1 modification only — `src/__pycache__/cache_keys.cpython-312.pyc` (tracked binary bytecode, 3462 bytes). This is a stale `__pycache__` build artifact, not research/source substance. `.verify_snapshot/` absent → no interrupted verification to recover.
- **Experiments inventory:** `git ls-files experiments/` → 138 tracked entries (107 goldens + 31 drivers).
- **Baseline guards (re-run this session):**
  - `python3 scripts/check_golden_baseline.py` → **ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT**
  - `python3 scripts/check_data_coverage.py` → **ALL 35 PINNED DATA INPUTS ARE PRESENT, TRACKED AND UNCHANGED**
  - `git diff --name-only d04d0e50..HEAD -- experiments/ data/ src/ tests/` → **empty**.

## 3. Delta vs Prior Durable Handoff

- Prior handoff: E193, HEAD `d04d0e50`, artifact `handoff_2026-11-13T00-49-31Z_INITIAL_TASK.md` (read and superseded).
- `git diff --name-only d04d0e50..HEAD` → generic canonical handoff-pointer aliases plus `ledger/RESEARCH_LEDGER.md` (handoff bookkeeping) only.
- `git diff --name-only d04d0e50..HEAD -- experiments/ data/ src/ tests/` → **0 paths**.
- **Conclusion:** no research, source, data, experiment, or baseline substance changed since the prior handoff.

## 4. Project Status

- **Research phase complete** (E001–E043). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.
- **Last substantive research entry:** E051. Entries E052 onward are durable-handoff refreshes only.
- This handoff corresponds to ledger entry **E194** (durable-handoff refresh).

## 5. Instructions for the Next Session

1. **Do not start substantive work until the user gives explicit direction.** Read `AGENTS.md`, `ledger/RESEARCH_LEDGER.md` (especially the latest entries), and this handoff.
2. Confirm the guards above still pass before any work:
   ```bash
   SEED=42 python3 scripts/check_golden_baseline.py
   SEED=42 python3 scripts/check_data_coverage.py
   ```
   Environment note: this container may lack dependencies (e.g. `pandas`); install `pip install -r requirements.txt` before relying on the full fast-check result. If a real mismatch is reported, stop and do not commit.
3. If a concrete task is assigned, follow project conventions in `AGENTS.md` (pre-registration, multiple-testing discipline, golden-file integrity, `SEED=42`).
4. If reproduction/verification is explicitly requested, use the suites below; never leave a run half-finished. Do not commit verification output; if a run is interrupted, restore with `SEED=42 python3 run_all_verification.py --restore-only`.
5. If no task is assigned, await further instructions. Do not invent experiments, run verification unprompted, change pre-registered gates/outcomes, or modify golden/baseline artifacts.

## 6. Reproduction / Verification Commands (run only if explicitly requested)

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
- `experiments/*.json` are canonical; never replace/re-pin goldens as a side effect of verification. E041/E042 grid artifacts have documented 1-ulp/ill-conditioned optimizer sensitivity — do not re-pin to silence.
- Never commit verification output or `src/__pycache__/` bytecode; never commit or log secrets/keys.
- Do not create `.github/workflows/` CI gates as an automated agent (template: `.github/workflow-templates/verification-gate.yml`; maintainer action required).
- Keep this handoff outside `experiments/`.

---

*Durable handoff created at session start for continuity. Timestamp 2026-11-13T00:50:24Z.*