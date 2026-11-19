# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-19T01-21-44Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `6a5b77a9` ("chore(kilo): checkpoint agent session", 2026-11-19T01:21:36Z)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current state (verified at handoff)

- **Research phase:** complete. Authoritative dispositions and surviving validated
  strategies are in `ledger/RESEARCH_LEDGER.md`. No actionable open/pending/blocked
  research item is indicated.
- **Verification snapshot:** `.verify_snapshot/` absent. `.verify_reports/` absent.
  No interrupted verification run to recover.
- **Working tree / remote:** `git status --short --branch` → `## main...origin/main`,
  no file changes at the start of this session. HEAD `6a5b77a9` == `origin/main`.
- **Canonical artifacts unchanged** by this handoff session:
  `git diff --name-only HEAD -- experiments/` → empty (0 files).
  `ledger/golden_baseline.json` and `ledger/data_baseline.json` present and parse.
- **Environment note (this runner):** bare `/usr/bin/python3` (3.12.3); core
  dependencies are **not** importable (`import pandas` → `ModuleNotFoundError`).
  Install before any verification: `python3 -m pip install -r requirements.txt`.
- **Closed — do not reopen:** E049/E050 (optimizer determinism + exact KKT
  enumeration) and the E041/E042 residual ill-conditioned QP drift (~1 ulp,
  ~1e-05). Do **not** re-pin E041/E042 artifacts to silence that drift.

## Initial task for the next session (CLEAR)

**Default: await explicit user instructions.** Do not invent new experiments, run
verification unprompted, change pre-registered gates/outcomes, or modify
golden/baseline artifacts without explicit direction.

### Ordered first steps (before any substantive work)

1. `git status --short --branch` — confirm HEAD/remote alignment and note any
   uncommitted files (this handoff is intentionally left uncommitted).
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted:
   `SEED=42 python3 run_all_verification.py --restore-only`, or restore pinned
   goldens per `AGENTS.md`, **before** other work.
3. Install deps if needed: `python3 -m pip install -r requirements.txt`
   (this runner has none installed).
4. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing any
   substantive change.

### If verification / reproduction is explicitly requested

- Always use **`SEED=42`** (the suite sets `QUANT_RESEARCH_OFFLINE=1`; a missing
  cache entry fails hard instead of downloading).
- Scopes (see `AGENTS.md`): `make check` (fast guards, ~seconds),
  `SEED=42 python3 verify_convention_robustness.py` (read-only),
  `SEED=42 python3 run_all_verification.py` (quick, ~8 min),
  `--extended` (~21 min), `--full` (~15 min).
- Verification overwrites and restores `experiments/*.json`; **never leave a run
  half-finished** and **never commit verification output** over the goldens.
  Restore if interrupted: `SEED=42 python3 run_all_verification.py --restore-only`.
- Do **not** re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json`
  to silence drift. Re-pin only with explicit direction, a deliberate `--update`
  run, and a ledger justification.

## Guardrails

- Always use **SEED=42** for reproducibility/verification runs.
- Never commit driver verification output over canonical goldens (`experiments/*.json`).
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without
  explicit, intentional re-baseline instruction and a ledger justification.
- Never commit `__pycache__/`, `.verify_snapshot/`, or `.verify_reports/`.
- Do not reopen closed E049/E050 or the E041/E042 ill-conditioned QP drift.
- Do not create `.github/workflows/` CI gates as an automated agent (template:
  `.github/workflow-templates/verification-gate.yml`; maintainer action required).
- Do not change pre-registered gates, sensitivity grids, falsification expectations,
  or outcomes without explicit justification and a ledger update.
- Never commit secrets/keys; never log secrets.

## Key references

- `AGENTS.md` — commands, reproducibility, baseline/data guard invariants
- `ledger/RESEARCH_LEDGER.md` — dispositions and open items
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned SHA-256 fingerprints
- `experiments/*.json` — canonical research artifacts
- `scripts/check.sh`, `run_all_verification.py`, `scripts/repoint_handoff.py`

## Handoff provenance

- **Durable artifact (this session):** `handoff_2026-11-19T01-21-44Z_INITIAL_TASK.md`
  (repo root), linked byte-identically from `handoff/`, `HANDOFFS/`, `.handoff/`,
  `.kilo/`, `.kilo/handoff/`.
- **Canonical pointers:** generic aliases (`HANDOFF.md`, `LATEST.md`,
  `HANDOFF_CURRENT.md`, `HANDOFF_LATEST.md`, `HANDOFF_NEXT_SESSION.md`,
  `INITIAL_TASK.md`, `NEXT_SESSION.md`, `handoff/CURRENT`, `.kilo/HANDOFF.md`, …)
  repointed via `python3 scripts/repoint_handoff.py handoff_2026-11-19T01-21-44Z_INITIAL_TASK.md`.
- **Supersedes operationally:** `handoff_2026-11-19T01-21-08Z_INITIAL_TASK.md`
  (previous handoff refresh, HEAD `0115b9e9`) and all prior `HANDOFF_*` /
  `handoff_*` artifacts, which are retained for history.
- This session created this durable handoff and a ledger record only. No code,
  experiments, baselines, or canonical artifacts were modified.
