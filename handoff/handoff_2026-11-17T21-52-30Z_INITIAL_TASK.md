# Durable Handoff — Initial Task Message (Next Agentic Work Session)

**Timestamp (UTC):** 2026-11-17T21:52:30Z
**HEAD:** `0e5db02c3c234b11f48334a38dcfa054cdd4cbe8` (main, 2026-11-17 21:52:08 +0000) "chore(kilo): checkpoint agent session"
**Branch:** `main` (in sync with `origin/main`; `git rev-list --left-right --count origin/main...HEAD` → `0	0`)
**Prior handoff:** `handoff_2026-11-17T21-28-38Z_INITIAL_TASK.md` — superseded by this file.

## Repository state (at capture)

- **Research phase:** COMPLETE. Experiments E001–E051 recorded in `ledger/RESEARCH_LEDGER.md`; no new research performed in this session. Ledger tail confirms closure through E466 (2026-11-17T19:33:44Z); the last substantive research entries are E051 (Post-Closure Conformance Pass, 2026-11-02). All entries after E051 (E052–E466) are durable-handoff refreshes only.
- **Working tree:** source-clean. `git status` shows only 12 modified tracked `__pycache__/*.pyc` bytecode files under `scripts/__pycache__/`, `src/__pycache__/`, `tests/__pycache__/` (build artifacts — do not commit). No changes in `experiments/`, `data/`, `src/`, `scripts/`, `tests/`, `research_state/`, or ledger sources.
- **Golden baseline:** all tracked artifacts under `experiments/` match HEAD. `git diff --name-only HEAD -- experiments/ data/ ledger/ scripts/ src/ tests/` → empty (excluding the 12 pyc files).
- **Verification state:** no `.verify_snapshot/` and no `.verify_reports/` present; no interrupted verification run indicated; nothing to recover.
- **Ledger tail:** last entry E466 (Durable Handoff Refresh, HEAD `aa7b2e39`) at 2026-11-17T19:33:44Z; this durable-handoff refresh is recorded as E467. Research phase remains closed (E001–E051 research; durable-handoff refreshes continue). 0 actionable open items.

## Canonical invariants (do not violate)

- `experiments/*.json` are golden artifacts. Verification overwrites them during runs and restores them afterward — **never leave a run half-finished**.
- If interrupted or on golden mismatch: `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/` only when HEAD still holds the pinned baseline). See `AGENTS.md` "Baseline Integrity".
- Re-pin `experiments/` or `data/` baselines only via explicit documented `--update` flows (`python3 scripts/check_golden_baseline.py --update`, `python3 scripts/check_data_coverage.py --update`), never as a side effect of verification.
- Always use `SEED=42` for verification/reproduction commands.
- Do not commit `__pycache__/*.pyc` artifacts or verification output.

## Known open items (from ledger; not blockers)

- **E049/E050:** E041/E042 grid artifacts remain 1-ulp sensitive under the ill-conditioned tangency QP (optimizer constraint-validation defect fixed; exact KKT enumeration routes the QP per E050). Numeric drift remains in the extended comparison. Do **not** re-pin to silence drift.
- **E048:** data-cache coverage is an enforced invariant; `scripts/check_data_coverage.py` guards every `data.download()` call site. To add a data input, commit the file and re-pin via `--update`.
- CI verification workflow cannot be pushed by automated agents; maintainer action required per `.github/workflow-templates/verification-gate.yml` and `VERIFICATION_GATE_TEMPLATE.md`.

## Recommended next actions

1. **Orient:** read this handoff and `AGENTS.md`; confirm `git status` is clean aside from regenerated `__pycache__/*.pyc` noise and that no `.verify_snapshot/` exists.
2. **Integrity check (before new work):** run `SEED=42 bash scripts/check.sh` (or `make check`). If a golden/baseline mismatch is reported, restore per `AGENTS.md` before proceeding. Escalate to `SEED=42 python3 run_all_verification.py` / `--extended` only if required.
3. **Handle user requests:** follow project conventions (pre-registration, no goalpost changes, no committing verification output, no golden/data re-pins without deliberate update flow). Research program is closed per ledger (E001–E051); avoid speculative new strategy exploration unless explicitly directed and properly pre-registered.
4. **Session close-out (if material work is done):** create a new timestamped durable handoff, mirror it to `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/`, repoint canonical handoff aliases via `python3 scripts/repoint_handoff.py <new_handoff_file>`, update `ledger/RESEARCH_LEDGER.md` only if appropriate, and do not commit `__pycache__` artifacts.

## Quick commands

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full

# Convention robustness only (no writes)
SEED=42 python3 verify_convention_robustness.py

# Recover the golden artifacts after an interrupted verification run
SEED=42 python3 run_all_verification.py --restore-only
```

_This durable handoff records a refresh only — no new research is requested. Pending implementation tasks carried forward: none._