# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-18T19:23:36Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch / HEAD:** `main` @ `c239e328` (0 ahead / 0 behind `origin/main` at handoff time)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current state (verified at handoff)

- **Research phase:** complete (E001–E051). Authoritative dispositions and surviving
  validated strategies are in `ledger/RESEARCH_LEDGER.md`. No open research task is pending.
- **Working tree:** clean; `git diff --name-only HEAD -- experiments/` is empty.
- **Verification state:** no `.verify_snapshot/` and no `.verify_reports/` — i.e. no
  interrupted verification run is pending recovery.
- **Canonical artifacts intact:** `experiments/*.json`, `ledger/golden_baseline.json`,
  `ledger/data_baseline.json`, pinned `data/` and `data/fundamentals/` inputs unchanged.
- **Environment note (this runner):** bare `/usr/bin/python3` (3.12.3) with **no** core deps
  (`import pandas` → `ModuleNotFoundError`). Install before running any gate:
  `python3 -m pip install -r requirements.txt`.
- **Closed — do not reopen:** E049/E050 (optimizer determinism, exact KKT enumeration) and
  the E041/E042 residual ill-conditioned-QP drift (~1 ulp → ~1e-05). Do **not** re-pin
  E041/E042 artifacts to silence that drift.

## Initial task for the next session (CLEAR)

**Default: await explicit user instructions.** Do not invent experiments, run the full
verification suite unprompted, or change pre-registered gates, sensitivity grids,
falsification expectations, outcomes, or golden/data baselines.

### Mandatory preflight (do this first, even before a small change)

1. `git status --short --branch` — confirm HEAD/remote alignment and list uncommitted files.
2. Confirm `.verify_snapshot/` is absent. If a stale snapshot (`ACTIVE.json`) exists:
   `SEED=42 python3 run_all_verification.py --restore-only` **before** any other work.
   Never leave a verification run half-finished.
3. `python3 -m pip install -r requirements.txt` if deps are missing on this runner.
4. `SEED=42 bash scripts/check.sh` (== `make check`) — fast integrity gate: py_compile,
   convention robustness, template validation, `tests/test_portfolio_opt.py`,
   `check_goldens_clean.py`, `check_golden_baseline.py`, `check_data_coverage.py`.
   It must pass before any commit.

### If verification / reproduction is explicitly requested

- Always use **`SEED=42`**.
- Scopes: `make check` (fast guards) → `SEED=42 python3 verify_convention_robustness.py`
  (read-only) → `SEED=42 python3 run_all_verification.py` (quick, ~8 min) →
  `--extended` (~21 min) → `--full` (~15 min).
- Verification overwrites then restores `experiments/*.json`. **Never commit verification
  output over the goldens.** If interrupted: `SEED=42 python3 run_all_verification.py --restore-only`
  or restore the pinned artifact from the commit whose SHA-256 matches `ledger/golden_baseline.json`.
- Re-pin baselines only with explicit direction, using the deliberate `--update` commands,
  plus a ledger justification.

### Known-good dispositions (reference, not work items)

| Item | State |
| --- | --- |
| E029 fundamentals | Offline-reproducible; snapshot pinned in `data/fundamentals/` |
| E030 16-ETF panel | 0 differences since panel committed (E048) |
| E041 optimizer | Root-caused and fixed (E049); 133 residual numeric (1-ulp QP) diffs remain, expected |
| E042 min-var | PARTIAL; grid drift expected, do not re-pin |
| CI gate | Cannot be created by an agent; template at `.github/workflow-templates/verification-gate.yml`, maintainer must add the workflow |

## Guardrails

- Always `SEED=42`.
- Never commit driver verification output over canonical goldens.
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit,
  intentional re-baseline instruction and a ledger entry.
- Do not modify `.github/workflows/` from an automated session.
- Do not generate new `handoff_*.md` artifacts beyond the one this session created, and do
  not delete historical handoffs.
- Never commit secrets or keys; never log them.

## Key references

- `AGENTS.md` — commands, reproducibility contract, baseline/guard invariants
- `ledger/RESEARCH_LEDGER.md` — dispositions and open items
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints
- `experiments/*.json` — canonical research artifacts
- `scripts/check.sh`, `run_all_verification.py`, `scripts/repoint_handoff.py`

## Handoff provenance

- **Durable artifact (this session):** `handoff_2026-11-18T19-23-36Z_INITIAL_TASK.md` (repo root).
- **Supersedes operationally:** `handoff_2026-11-18T19:19:56Z_INITIAL_TASK.md` and
  `HANDOFF_NEXT_SESSION_2026-11-18T19-22-30Z_INITIAL_TASK.md` (both retained for history).
- **Generic pointers:** repointed via `python3 scripts/repoint_handoff.py handoff_2026-11-18T19-23-36Z_INITIAL_TASK.md`
  (`handoff_CURRENT`, `latest`, `.kilo/HANDOFF.md`, `handoff/CURRENT`, …).
- **Scope of this session:** durable handoff only — no code, experiment, ledger-disposition,
  data, or baseline change was made beyond the ledger provenance entry for this refresh.
