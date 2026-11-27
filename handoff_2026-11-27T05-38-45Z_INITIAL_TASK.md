# Handoff — Next Agentic Work Session

**Timestamp:** 2026-11-27T05:38:45Z
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**HEAD:** ac6cfe3c (main, in sync with origin/main)

## Current State (verified at handoff)

- **Research Phase:** Complete (E001–E043). Surviving validated strategies in `ledger/RESEARCH_LEDGER.md`.
- **Working tree:** Clean apart from untracked compiled-artifact noise (`src/__pycache__/`, `scripts/__pycache__/`). No source, `experiments/*.json`, ledger, baseline, or pinned-data changes.
- **Canonical baselines intact:** `git diff HEAD -- experiments/` empty; `.verify_snapshot/` and `.verify_reports/` absent (no interrupted verification snapshot pending).
- **Dependencies:** NOT importable this session (`numpy`/`pandas` -> `ModuleNotFoundError`). `pip install -r requirements.txt` required before any verification.
- **All three pure-Python guards PASS:** `check_goldens_clean.py` (all committed golden artifacts match HEAD, exit 0); `check_golden_baseline.py` (all 107 pinned golden artifacts match baseline fingerprint, exit 0); `check_data_coverage.py` (all 35 pinned data inputs present, tracked, unchanged, exit 0).
- **Full verification suite not run** (deps missing).

## Prioritized Real-Work Task List (for the next session)

1. **Provision dependencies:** `pip install -r requirements.txt`.
2. **Reproduce (real work, not a handoff refresh):** `SEED=42 python3 run_all_verification.py --extended` (~21 min). Report per-driver drift precisely; do **not** re-pin artifacts to make a tolerance violation disappear.
3. **Confirm E041/E042 tangency-QP drift stays closed** without re-pinning (E050 exact-solver precedent).
4. **Cleanup (propose only):** If the accumulated `handoff_*` file count is a problem, *propose* a `.gitignore` + `git rm --cached` cleanup plan; do **not** execute it without explicit direction.

## Constraints

- Do **not** start new research; the research phase is closed (E001–E043).
- Do **not** re-pin goldens/data baselines; do **not** commit verification output.
- Do **not** manufacture another handoff refresh as a substitute for work; leave your own timestamped handoff only when you finish real work, using the procedure below.
- Never leave a verification run half-finished: if interrupted, run `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`.
- No CI workflow can be created by agents; a maintainer must create it via the GitHub UI using the template at `.github/workflow-templates/verification-gate.yml`.

## Quick Commands Reference

```bash
SEED=42 bash scripts/check.sh          # or make check
SEED=42 python3 run_all_verification.py   # or make verify-quick (~8 min)
SEED=42 python3 run_all_verification.py --extended  # or make verify-extended (~21 min)
SEED=42 python3 run_all_verification.py --full  # or make verify-full
SEED=42 python3 verify_convention_robustness.py     # or make verify
```

## Key Artifacts

- **Golden files:** `experiments/*.json` (canonical research artifacts; committed baseline is authoritative).
- **Ledger:** `ledger/RESEARCH_LEDGER.md` (dispositions E001–E043 + handoff refreshes through E770).
- **Data cache:** `data/` (gitignored except pinned vintages; cache coverage enforced by `scripts/check_data_coverage.py`).
- **Backup location:** `.verify_snapshot/` (gitignored, with ACTIVE.json marker).

## Durable Artifact (this session)

`handoff_2026-11-27T05-38-45Z_INITIAL_TASK.md` (repo root). Existing generic aliases repointed via `scripts/repoint_handoff.py` (expect `bad=0`); no new mirror directories or alias names created (continuing the E740–E770 deliberate break of the mirror/repoint explosion). Supersedes `handoff_2026-11-27T05-37-21Z_INITIAL_TASK.md` (E771).

This session created this durable handoff only. No code, experiments, ledgers, baselines, or canonical artifacts were modified, and no commit was made (left uncommitted pending explicit direction).

## Handoff Procedure (how this artifact was produced)

1. Write `handoff_<UTC-TIMESTAMP>Z_INITIAL_TASK.md` at the repo root (`YYYY-MM-DDTHH-MM-SSZ`, colons in the time replaced by hyphens).
2. Repoint the stable aliases: `python3 scripts/repoint_handoff.py handoff_<UTC-TIMESTAMP>Z_INITIAL_TASK.md` (expect `bad=0`); then `python3 scripts/repair_broken_handoff.py <new-file>` if needed.
3. Append a short `## E<next> — Durable handoff refresh (<timestamp>)` entry to `ledger/RESEARCH_LEDGER.md`.

(End of file - total 58 lines)