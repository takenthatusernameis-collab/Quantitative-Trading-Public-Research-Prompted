# INITIAL TASK HANDOFF

**Timestamp:** 2026-11-03T22:07:47Z
**From:** Current agentic work session
**To:** Next agentic work session
**Repository:** Quantitative-Trading-Public-Research-Prompted

---

## Context

This repository contains independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data.

- **Research phase:** Complete (E001–E043)
- **Surviving validated strategies:** Documented in `ledger/RESEARCH_LEDGER.md`
- **Golden artifacts:** `experiments/*.json` are the canonical research artifacts. The verification suite backs them up and restores them - they must never be left modified.

---

## Primary Goal

Verify repository integrity and confirm the baseline is clean before starting any new work. Follow all conventions in `AGENTS.md`.

---

## Recommended Initial Tasks (In Order)

### 1) Verify Baseline Integrity
Run the fast convention-robustness check first:
```bash
SEED=42 bash scripts/check.sh
# or
make check
```

This runs py_compile, golden cleanliness checks, data coverage, and convention robustness. Pay attention to any failures - especially around stale snapshots or golden mismatches.

### 2) If Clean, Run Quick Verification (Optional but Recommended)
To fully validate the reproduction pipeline:
```bash
SEED=42 python3 run_all_verification.py
# or
make verify-quick
```
(~8 min). This re-runs the 8 drivers in the quick block and restores goldens afterwards.

### 3) Review Research State
- Read `ledger/RESEARCH_LEDGER.md` for current status of experiments and any open items (e.g. E041 numeric drift noted in AGENTS.md).
- Review `ledger/golden_baseline.json` to understand the pinned baseline.
- Check `.verify_snapshot/` - if a stale snapshot exists with no live run, recover with `SEED=42 python3 run_all_verification.py --restore-only`.

---

## Key Files & References
- **AGENTS.md** - Full commands, conventions, and critical notes about baseline integrity
- **ledger/RESEARCH_LEDGER.md** - Experiment results and promotion decisions
- **scripts/check.sh** - Main verification/check script
- **run_all_verification.py** - Full verification suite with backup/restore
- **ledger/golden_baseline.json** - Pinned hashes of canonical artifacts
- **ledger/data_baseline.json** - Pinned hashes of required data files

---

## Important Reminders
- Always use `SEED=42`
- Never modify `experiments/*.json` as a side effect of verification - the suite handles backup/restore
- If `check.sh` reports golden mismatches, fix before committing (see AGENTS.md for recovery procedures)
- `QUANT_RESEARCH_OFFLINE=1` is used during verification - ensure data coverage is intact
- Follow the pre-registration, multiple-testing discipline, and negative results recording conventions

---

**Ready to proceed. Start with step 1 (baseline integrity check).**
