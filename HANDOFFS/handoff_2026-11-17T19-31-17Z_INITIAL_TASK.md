# Durable Handoff — Initial Task Message (Next Agentic Work Session)

**Timestamp (UTC):** 2026-11-17T19:31:17Z
**HEAD:** `f9c080dd8d887b835e788c5d7ae56cc43978ec8a` (`chore(kilo): checkpoint agent session`)
**Branch:** `main` (in sync with `origin/main`, 0/0)
**Prior handoff:** `handoff_2026-11-17T19-28-37Z_INITIAL_TASK.md` (E465) — superseded by this file.

## Repository state (at capture)

- **Research phase:** COMPLETE. Experiments E001–E051 recorded in `ledger/RESEARCH_LEDGER.md`; durable handoff refreshes through E465.
- **Working tree:** clean (no tracked/untracked changes observed at capture except this handoff work in progress). No `.verify_snapshot/` or `.verify_reports/` present; no interrupted verification run.
- **Canonical artifacts:** `experiments/*.json` are goldens — never overwrite/commit verification output. If a run is interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/` (only safe if HEAD still holds the pinned baseline; see AGENTS.md).
- **Known open items (not blockers, per ledger):**
  - **E049:** E041/E042 grid artifacts remain 1-ulp sensitive under ill-conditioned tangency QP (optimizer constraint-validation defect fixed; 133 numeric diffs remain in E041 extended comparison). Do **not** re-pin to silence drift.
  - CI workflow gate cannot be pushed by agents; see `.github/workflow-templates/verification-gate.yml` and `VERIFICATION_GATE_TEMPLATE.md`.

## Reproduction / verification (read before running)

```bash
# Fast convention-robustness + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh
# or: make check

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py
# Extended (~21 min, includes 18-driver structural compare + drift report)
SEED=42 python3 run_all_verification.py --extended
# Full (~15 min, E042 n_sim=50 + sensitivity grid)
SEED=42 python3 run_all_verification.py --full
```

Always use `SEED=42`. Verification overwrites `experiments/*.json` during runs and restores them; do not leave half-finished. Re-pin goldens/data baselines only via explicit `--update` scripts and never as a side effect of verification.

## Initial task for next session

1. **Orient:** read this handoff and `AGENTS.md`; confirm `git status` is clean (aside from `__pycache__` noise if any) and no `.verify_snapshot/` exists.
2. **Integrity check (recommended before new work):** run `SEED=42 bash scripts/check.sh` (and/or `make verify-quick`) to reconfirm goldens, baselines, and offline reproducibility. If any golden mismatch is reported, restore per AGENTS.md before proceeding.
3. **If a new user request arrives:** follow it within project conventions (pre-registration, no goalpost changes, no golden re-pins without deliberate update flow, no committing verification output). Research program is closed per ledger; avoid speculative new strategy exploration unless explicitly directed and pre-registered.
4. **On completion of any session:** leave a new timestamped durable handoff and repoint canonical aliases via `python3 scripts/repoint_handoff.py <new_handoff_file>`; update `ledger/RESEARCH_LEDGER.md` with a brief entry if material work was performed.

_No pending implementation tasks carried forward from this handoff._
