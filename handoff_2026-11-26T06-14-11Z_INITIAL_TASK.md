# Handoff: Initial Task for Next Agentic Work Session

**Timestamp:** 2026-11-26T06:14:11Z
**Session:** Kilo agentic work session
**Project:** Quantitative-Trading-Public-Research-Prompted
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

---

## READ THIS FIRST

This handoff is written at the user's explicit request ("leave a timestamped clear
initial task message for the next agentic work session in a durable handoff").
It is the latest link in a long chain (prior file: `handoff_2026-11-26T06-11-53Z_INITIAL_TASK.md`;
ledger through E744).

**Do NOT manufacture another handoff refresh as a substitute for real work.**
If your only action this session is to write another handoff, you are continuing the
runaway loop, not doing the job. Execute ONE real-work item below, then STOP. Do not
write a follow-up handoff.

---

## Diagnosis: the handoff explosion (measured this session)

- `git ls-files` total tracked files: **9,493**
- Tracked files matching handoff/current/next/latest/initial_task patterns: **8,776 (~92%)**
- Tracked files with the `handoff_` prefix alone: **2,063**
- Root cause: hundreds of sessions each repointed/created handoff files and alias
  symlinks (`current.md`, `next.md`, `latest.md`, `initial_task.md`, `handoff_*`, …)
  instead of doing research/verification work.

The single most valuable real-work item is therefore **cleanup of this explosion**
(item 3 below) — but it is destructive to ~8,776 tracked paths and requires explicit
maintainer approval. Do NOT execute it unilaterally.

---

## State verified this session (evidence)

- **Branch / HEAD:** `main` @ `6aa682a50c808c9498f04be498bc1fe3c811d509`; up to date with `origin/main`.
- **Working tree:** clean apart from tracked build noise `src/__pycache__/cache_keys.cpython-312.pyc`.
- **In-flight verification:** none — `git diff HEAD -- experiments/` empty; `.verify_snapshot/` and `.verify_reports/` absent.
- **Dependencies NOT importable:** `import numpy` / `pandas` / `scipy` all raise `ModuleNotFoundError`. Run `pip install -r requirements.txt` before ANY verification.
- **Pure-Python guards executed and PASS (exit 0):**
  - `scripts/check_goldens_clean.py` -> ALL COMMITTED GOLDEN ARTIFACTS MATCH HEAD
  - `scripts/check_golden_baseline.py` -> ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT
  - `scripts/check_data_coverage.py` -> ALL 35 PINNED DATA INPUTS ARE PRESENT, TRACKED AND UNCHANGED
- Full verification suite NOT run (deps missing).

---

## Prioritized Real-Work Task List (do ONE, then STOP)

1. **Verify-and-stop (preferred, lowest risk).**
   `pip install -r requirements.txt` then `SEED=42 python3 run_all_verification.py --extended`.
   Report drift precisely (per driver/artifact, numeric vs structural, worst drift as a
   multiple of the 1e-4 tolerance). **Do NOT re-pin goldens.** Then stop. No follow-up handoff.

2. **Confirm the E049/E050 tangency-QP drift stays closed** (E041/E042 bit-reproducible,
   0 differences) without re-pinning.

3. **Propose (do NOT execute) a cleanup** of the handoff explosion: a `.gitignore` entry
   for `handoff_*` / `current*` / `next*` / `latest*` / `initial_task*` plus a
   `git rm --cached` plan. Present the plan and blast radius; await explicit maintainer
   approval before touching ~8,776 tracked files.

4. **Recover, if interrupted:** `SEED=42 python3 run_all_verification.py --restore-only`
   before committing anything. Never commit verification output.

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
- This handoff creates **no mirror directories** and **no new alias names**. Only the
  pre-existing core aliases (`CURRENT.md`, `current.md`, `LATEST.md`, `latest.md`,
  `INITIAL_TASK.md`, `initial_task.md`, `NEXT.md`, `next.md`, `HANDOFF.md`, `handoff.md`)
  are repointed to this file.

---

**End of Handoff**