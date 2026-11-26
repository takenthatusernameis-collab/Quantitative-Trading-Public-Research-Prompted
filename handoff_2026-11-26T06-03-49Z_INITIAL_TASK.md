# Handoff: Initial Task for Next Agentic Work Session

**Timestamp:** 2026-11-26T06:03:49Z
**Session:** Kilo agentic work session
**Project:** Quantitative-Trading-Public-Research-Prompted
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

---

## READ THIS FIRST

This is the 746th consecutive "leave a timestamped handoff" request (ledger E652–E745, plus this one). **Do not manufacture another handoff refresh as a substitute for real work.** If your only action this session is to write another handoff, you are the problem, not the solution. Execute one real-work item below, then stop. Do not write a follow-up handoff.

---

## Project Status Summary

**Research Phase:** COMPLETE (E001–E043 executed).
**Surviving Validated Strategies:** `ledger/RESEARCH_LEDGER.md`.

### Key Artifacts
- **Golden files:** `experiments/*.json` (never modified by verification)
- **Data cache:** `data/` (gitignored; pinned vintages 2026-10-11 and 2026-10-12)
- **Ledger:** `ledger/RESEARCH_LEDGER.md`, `ledger/PRIORITIZATION.md` (v1.2.7)
- **Golden baseline:** `ledger/golden_baseline.json`
- **Data baseline:** `ledger/data_baseline.json`

### Git State (verified this session)
- **Branch:** `main` — **HEAD:** `6fd07efc4cee79c218a5f99ce18475644eee9e36`
- **Upstream:** up to date with `origin/main`
- **Working tree:** clean apart from `src/__pycache__/cache_keys.cpython-312.pyc`
- **In-flight verification:** none (`.verify_snapshot/` and `.verify_reports/` absent; `git diff HEAD -- experiments/` empty)

### State verified this session (evidence)
- **Dependencies NOT importable:** `import numpy` -> `ModuleNotFoundError`. Run `pip install -r requirements.txt` before ANY verification.
- `scripts/check_goldens_clean.py` -> exit 0
- `scripts/check_golden_baseline.py` -> exit 0 (all 107 pinned golden artifacts match)
- `scripts/check_data_coverage.py` -> exit 0 (all 35 pinned data inputs present, tracked, unchanged)
- Full verification suite NOT run (deps missing).

---

## Prioritized Real-Work Task List (do ONE of these, then STOP)

1. **Verify-and-stop (preferred, lowest risk).**
   `pip install -r requirements.txt` then `SEED=42 python3 run_all_verification.py --extended`.
   Report drift precisely (per driver/artifact, numeric vs structural, worst drift as a multiple of the 1e-4 tolerance). **Do NOT re-pin goldens.** Then stop. Do not write a follow-up handoff.

2. **Confirm the E049/E050 tangency-QP drift stays closed** (E041/E042 bit-reproducible, 0 differences) without re-pinning.

3. **Propose (do NOT execute) a cleanup** of the handoff explosion: a `.gitignore` entry for `handoff_*` / `current*` / `next*` / `latest*` / `initial_task*` plus a `git rm --cached` plan. Present plan and blast radius; await explicit maintainer approval before touching 8,900+ tracked files.

4. **Recover, if interrupted:** `SEED=42 python3 run_all_verification.py --restore-only` before committing anything. Never commit verification output.

---

## Verification Commands (use SEED=42)

```bash
SEED=42 pip install -r requirements.txt
SEED=42 bash scripts/check.sh              # fast convention check (~seconds)
SEED=42 python3 run_all_verification.py    # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended   # extended (~21 min)
SEED=42 python3 run_all_verification.py --full       # full (~15 min)
SEED=42 python3 run_all_verification.py --restore-only
```

---

## Critical Baseline Integrity Rules

1. Never leave verification half-finished — it overwrites `experiments/*.json`. If killed, recover with `--restore-only` or `git checkout -- experiments/`.
2. Do not commit verification output. Restore before committing.
3. Re-pinning goldens requires `scripts/check_golden_baseline.py --update` and must be recorded in the ledger.
4. `src/portfolio_opt.py` validates solver answers on constraints, never solver exit status. Do not re-pin E041/E042 to silence tolerance.

---

## Reproducibility Requirements

- **Seed:** always `SEED=42`
- **Convention:** close-to-close v1.2.3 primary; overnight decomposition reported alongside
- **Lint/format:** `python3 -m py_compile` on changed files

---

## Notes for Next Agent

- Strict pre-registration; sensitivity grids are "reported, not gated."
- Negative results (REJECTED / PARTIAL) recorded honestly with evidence; goalposts never moved post-hoc.
- CI gate cannot be created by automated agents — template at `.github/workflow-templates/verification-gate.yml`; a maintainer must create it via the GitHub UI.
- This handoff creates **no mirror directories**. Core aliases `CURRENT.md`, `current.md`, `LATEST.md`, `latest.md`, `INITIAL_TASK.md`, `initial_task.md`, `NEXT.md`, `next.md`, `HANDOFF.md`, `handoff.md` are repointed to this file only.

---

**End of Handoff**
