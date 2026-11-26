# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-26T15:20:45Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `7e22eba3`
**Remote sync:** `origin/main` aligned with local `main`
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

---

## 0. Read this first — the loop warning

This repo is in a documented handoff-refresh loop. The prior session warned that writing another handoff is itself an instance of the loop. **This file was written only because the user explicitly requested it.** Do not manufacture another refresh as a substitute for real work. The highest-value action for the next session is to execute step 1 or 2 below, or confirm-and-stop.

---

## 1. Current state (verified at handoff)

- **Research phase:** complete (E001–E043). Dispositions and surviving validated strategies are in `ledger/RESEARCH_LEDGER.md`. No open/pending/blocked research items.
- **Working tree:** clean except `src/__pycache__/cache_keys.cpython-312.pyc` (pre-existing build noise) and this uncommitted handoff artifact. No `experiments/`, `data/`, `src/` source, `scripts/`, `tests/`, ledger, or baseline files changed.
- **`git diff HEAD -- experiments/`:** empty (canonical goldens intact).
- **Verification snapshot:** `.verify_snapshot/` and `.verify_reports/` are absent (no interrupted verification pending; no `ACTIVE.json` marker).
- **Canonical baselines/artifacts:** `experiments/*.json`, `ledger/golden_baseline.json` (107 pinned artifacts), and `ledger/data_baseline.json` (35 pinned data inputs) are unchanged.
- **Dependencies:** NOT importable this session (`import numpy` → `ModuleNotFoundError`). Run `pip install -r requirements.txt` before any verification. Full verification suite was **not** run.
- **Closed — do not reopen:** E049/E050 (optimizer determinism + exact KKT active-set enumeration, commit `72dc947`) and E041/E042 residual ill-conditioned-QP drift (~1-ulp, ~1e-05). Do **not** re-pin E041/E042 artifacts to silence drift.

---

## 2. Initial task for the next session (CLEAR, prioritized)

**Default: await explicit user instructions.** Do not invent new experiments, run verification unprompted, move pre-registered gates/outcomes, or modify golden/baseline/canonical artifacts without explicit direction.

If you must act autonomously, work in order and stop when the step is done:

1. **Verify and stop.** Confirm HEAD/remote alignment (`git status --short --branch`, `git rev-list --left-right --count HEAD...origin/main`) and that `git diff HEAD -- experiments/` is empty. If clean, run the three hashlib-only guards (`scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`) and report state and stop — that is a complete, correct outcome.
2. **Reproduce (real work, not a handoff refresh).** `pip install -r requirements.txt`, then `SEED=42 python3 run_all_verification.py --extended` (~21 min). Report per-driver drift precisely; do **not** re-pin artifacts to make a tolerance violation disappear. A run must never be left half-finished — recovery is `SEED=42 python3 run_all_verification.py --restore-only`.
3. **Pre-registered research** only if the user explicitly requests it — with a `pre_registered` block, falsification expectations, and sensitivity grid stated before execution.

---

## 3. Guardrails

- Always use **SEED=42** for reproducibility/verification runs.
- Never commit driver verification output over canonical goldens (`experiments/*.json`). Restore if interrupted: `SEED=42 python3 run_all_verification.py --restore-only`.
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction and ledger justification.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (maintainer action via GitHub UI).
- Never commit secrets/keys; never log secrets.

---

## 4. Key references

- `AGENTS.md` — commands, reproducibility, baseline/guard invariants
- `ledger/RESEARCH_LEDGER.md` — dispositions and open items
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints
- `experiments/*.json` — canonical research artifacts
- `scripts/check.sh`, `run_all_verification.py`

---

## 5. Handoff provenance

- **Durable artifact (this session):** `handoff_2026-11-26T15-20-45Z_INITIAL_TASK.md` (repo root)
- Generic symlinks (`CURRENT`, `LATEST`, `INITIAL_TASK`, `HANDOFF`, `NEXT_SESSION`) repointed to this file.
- Supersedes operationally: prior handoff artifacts (retained for history), including `handoff_2026-11-26T15-19-16Z_INITIAL_TASK.md` and earlier.
- This session created this durable handoff only. No code, experiments, ledgers, baselines, or canonical artifacts were modified. No commit was made.
- Handoff written by agent at 2026-11-26T15:20:45Z.
