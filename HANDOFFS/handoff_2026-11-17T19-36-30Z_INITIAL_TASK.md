# Durable Handoff — Initial Task Message (Next Agentic Work Session)

**Timestamp (UTC):** 2026-11-17T19:36:30Z
**HEAD:** `a451782115f366b200ea8414ad1844d4693b2061` (`main`)
**Branch:** `main` (in sync with `origin/main`, 0/0)
**Prior handoff:** `handoff_2026-11-17T19-35-34Z_INITIAL_TASK.md` — superseded by this file.

## Repository state (at capture)

- **Research phase:** COMPLETE. Experiments E001–E051 are recorded in `ledger/RESEARCH_LEDGER.md`; durable handoff refreshes are maintained through this session (no new research performed).
- **Working tree:** clean at source level; only tracked `__pycache__/*.pyc` build artifacts are modified (regenerated, not source). `experiments/`, `data/`, `src/`, `scripts/`, `tests/`, `research_state/`, and ledger sources show no pending material changes. No `.verify_snapshot/` or `.verify_reports/` present; no interrupted verification run.
- **Delta vs prior durable handoff (`handoff_2026-11-17T19-35-34Z_INITIAL_TASK.md`, HEAD `97225bb4`):** checkpoint/bookkeeping commits only (`97225bb4` → `a4517821`); no changes to `experiments/`, `data/`, `src/`, `scripts/`, `tests/`, or `research_state/`. Prior state adopted.
- **Canonical artifacts:** `experiments/*.json` are goldens — never overwrite or commit verification output. If a run is interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/` only when HEAD still holds the pinned baseline (see `AGENTS.md`).

## Known open items (not blockers, per ledger)

- **E049:** E041/E042 grid artifacts remain 1-ulp sensitive under the ill-conditioned tangency QP (optimizer constraint-validation defect fixed; numeric drift remains in extended comparison). Do **not** re-pin to silence drift.
- CI verification workflow cannot be pushed by agents; maintainer action required per `.github/workflow-templates/verification-gate.yml` and `VERIFICATION_GATE_TEMPLATE.md`.

## Reproduction / verification (read before running)

Always use `SEED=42`. Verification overwrites `experiments/*.json` during runs and restores them — do not leave a run half-finished.

```bash
# Fast convention-robustness + template/guard validation (~seconds, offline)
SEED=42 bash scripts/check.sh
# or: make check

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py
# Extended (~21 min)
SEED=42 python3 run_all_verification.py --extended
# Full (~15 min)
SEED=42 python3 run_all_verification.py --full
```

Re-pin goldens/data baselines only via explicit `--update` flows documented in `AGENTS.md`, never as a side effect of verification.

## Initial task for next session

1. **Orient:** read this handoff and `AGENTS.md`; confirm `git status` is clean except for possible regenerated `__pycache__/*.pyc` noise and that no `.verify_snapshot/` exists.
2. **Integrity check (recommended before new work):** run `SEED=42 bash scripts/check.sh` to reconfirm goldens, baselines, and offline reproducibility. If a golden mismatch is reported, restore per `AGENTS.md` before proceeding. Escalate to `make verify-quick`/`--extended` only if needed.
3. **If a new user request arrives:** follow it within project conventions (pre-registration, no goalpost changes, no golden/data re-pins without deliberate update flow, no committing verification output). The research program is closed per ledger; avoid speculative new strategy exploration unless explicitly directed and pre-registered.
4. **On completion of any material session work:** leave a new timestamped durable handoff, mirror/repin canonical aliases via `python3 scripts/repoint_handoff.py <new_handoff_file>`, and update `ledger/RESEARCH_LEDGER.md` with a brief entry if appropriate. Do not commit `__pycache__` artifacts.

_No pending implementation tasks carried forward from this handoff._
