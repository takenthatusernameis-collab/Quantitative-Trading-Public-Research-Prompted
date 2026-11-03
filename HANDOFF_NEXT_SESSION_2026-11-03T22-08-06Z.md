# HANDOFF_NEXT_SESSION_2026-11-03T22-08-06Z

**Session Context:** Research phase complete (E001–E049). Surviving validated strategies documented in ledger/RESEARCH_LEDGER.md. Verification baseline integrity guards in place. Repository verified stable as of this handoff.

> **START HERE:** A clear initial task has been left below for the next agentic work session. Read all constraints in AGENTS.md before taking any action.

## Initial Task for Next Session
**CLEAR INITIAL TASK:** *Execute the following objective as specified.*

**Objective:** Verify repository integrity and confirm the baseline is clean before starting any new work. Follow all conventions in AGENTS.md.

**Instructions:**
1. Run the fast convention-robustness check: `SEED=42 bash scripts/check.sh` (or `make check`).
2. If clean, optionally run quick verification: `SEED=42 python3 run_all_verification.py` (or `make verify-quick`).
3. Review `ledger/RESEARCH_LEDGER.md` and `ledger/golden_baseline.json` for research context.
4. Await the user's next requested change; do not take unprompted actions that modify canonical artifacts.

**Acceptance Criteria:**
- Baseline integrity check passes (`scripts/check.sh` green).
- `experiments/` and `ledger/` baselines remain unmodified (no verification output committed).
- `SEED=42` used for all verification runs.

## Current State (verified at handoff time)
- **Git HEAD:** 804e37a chore(kilo): checkpoint agent session
- **Working tree:** clean of tracked source changes
- **Verification baseline:** intact; golden artifacts under `experiments/` match committed state per `ledger/golden_baseline.json` and `ledger/data_baseline.json`
- **No live verification snapshot:** `.verify_snapshot/` absent / no ACTIVE marker
- **Research status:** E001–E049 complete; surviving strategies documented in `ledger/RESEARCH_LEDGER.md`. Closed/known items: E049/E050 (optimizer determinism), E041/E042 (ill-conditioned QP drift) — do not re-pin to silence drift.

## Quick Start For Next Session
1. Confirm state: `git log -1 --oneline` and `git status --short`
2. Read AGENTS.md (baseline integrity, verification rules, constraints)
3. Read `ledger/RESEARCH_LEDGER.md` for context if needed
4. Execute the "Initial Task for Next Session" above
5. Follow all guardrails strictly

## Notes & Guardrails
- Never modify `experiments/*.json` as a side effect of verification without following the re-pinning process (`python3 scripts/check_golden_baseline.py --update`); the committed golden is authoritative.
- Follow all verification guards: `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`.
- Do not create unprompted handoffs or re-open closed items.
- Pre-registration, multiple-testing discipline, and falsification expectations remain in force if new experiments are ever requested.

**Handoff created:** 2026-11-03T22-08-06Z (UTC)
**Previous handoff:** HANDOFF_NEXT_SESSION_2026-11-03T22-06-18Z.md
