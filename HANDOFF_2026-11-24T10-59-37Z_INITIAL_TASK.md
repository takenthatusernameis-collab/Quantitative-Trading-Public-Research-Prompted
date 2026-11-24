# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-24T10:59:37Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `19077eec217cdbd45447a5bccd3b47a36579b6e1` (2026-11-24 10:59:29 +0000)
**Remote sync:** `origin/main` aligned with local `main` (`git rev-list --left-right --count HEAD...origin/main` → `0 0`)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

---

## Current state (verified at handoff)

- **Research phase:** complete (E001–E043). Authoritative dispositions and surviving validated strategies in `ledger/RESEARCH_LEDGER.md`.
- **Working tree:** clean for canonical artifacts. `git status --short experiments/ data/ ledger/ scripts/ src/ tests/` shows only pre-existing `__pycache__` build noise (`src/__pycache__/cache_keys.cpython-312.pyc`), not a canonical artifact. No source, ledger, baseline, or canonical change.
- **`git diff HEAD -- experiments/`:** empty — canonical goldens intact.
- **Verification snapshot:** `.verify_snapshot/` and `.verify_reports/` are **absent** — no interrupted verification pending; no `ACTIVE.json` marker.
- **Canonical baselines:** `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json` unchanged.
- **Closed — do not reopen:** E049/E050 (optimizer determinism + exact KKT active-set enumeration, commit `72dc947`) and E041/E042 residual ill-conditioned-QP drift (~1-ulp, ~1e-05). Do **not** re-pin E041/E042 artifacts to silence drift; there is no remaining tolerance violation.

---

## Initial task for the next session (CLEAR, prioritized)

**Default: await explicit user instructions.** Do not invent new experiments, run verification unprompted, move pre-registered gates/outcomes, or modify golden/baseline/canonical artifacts without explicit direction. If your only action is to refresh this handoff, that is a maintenance task — but do not manufacture repeated refreshes as a substitute for real work.

If you must act autonomously, work in order and stop when the step is done:

1. **Verify and stop.** Confirm HEAD/remote alignment (`git status --short --branch`, `git rev-list --left-right --count HEAD...origin/main`) and that `git diff HEAD -- experiments/` is empty. If clean, run the three hashlib-only guards (`scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`), report state, and stop — that is a complete, correct outcome.
2. **Reproduce (real work, not a handoff refresh).** `pip install -r requirements.txt`, then `SEED=42 python3 run_all_verification.py --extended` (~21 min). Report per-driver drift precisely; **do not** re-pin artifacts to make a tolerance violation disappear. A run must never be left half-finished — recovery: `SEED=42 python3 run_all_verification.py --restore-only`.
3. **Pre-registered research** only if the user explicitly requests it — with a `pre_registered` block, falsification expectations, and sensitivity grid stated *before* execution.

---

## Guardrails

- Always use **SEED=42** for reproducibility/verification runs.
- Never commit driver verification output over canonical goldens (`experiments/*.json`). Restore if interrupted: `SEED=42 python3 run_all_verification.py --restore-only`.
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction and ledger justification.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (template: `.github/workflow-templates/verification-gate.yml`; maintainer action via GitHub UI).
- Never commit secrets/keys; never log secrets.

---

## Key references

- `AGENTS.md` — commands, reproducibility, baseline/guard invariants
- `ledger/RESEARCH_LEDGER.md` — dispositions and open items
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints
- `experiments/*.json` — canonical research artifacts
- `scripts/check.sh`, `run_all_verification.py`

---

## Handoff provenance

- Durable artifact: `HANDOFF_2026-11-24T10-59-37Z_INITIAL_TASK.md` at repo root (this session's message time: 2026-11-24T10:59:37Z).
- Supersedes operationally previous INITIAL_TASK handoffs (retained for history), including `handoff_2026-11-24T10-58-27Z_INITIAL_TASK.md`.
- This session created this durable handoff only. No code, experiments, ledgers, baselines, or canonical artifacts were modified. No commit was made (left uncommitted pending explicit direction).
- Handoff written by agent at 2026-11-24T10:59:37Z.
