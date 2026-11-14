# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-14T05:37:35Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `eef30ac6` ("chore(kilo): checkpoint agent session"), in sync with `origin/main` (`0 0`)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current state (verified at this handoff)

- **Working tree:** clean at start of this handoff session (`git status --short --branch` → `## main...origin/main`, no substantive uncommitted changes). After this handoff is written, only the new durable handoff and repointed generic symlinks will be present as changes.
- **Delta vs prior durable handoff:** prior handoff `handoff_2026-11-14T05-36-27Z_INITIAL_TASK.md` recorded HEAD `eef30ac6`. No commits added since then. Non-handoff research substance (`experiments/`, `data/`, `src/`, `scripts/`, `tests/`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`) unchanged.
- **`.verify_snapshot/` / `.verify_reports/`:** absent — no interrupted verification run pending.
- **Research phase:** complete (E001–E051). Surviving validated strategies/dispositions: `ledger/RESEARCH_LEDGER.md`. Last research entry is **E051**; later ledger entries are handoff/bookkeeping refreshes. No actionable `OPEN`/`PENDING`/`BLOCKED`/`TODO` markers.
- **Closed/resolved — do not reopen:** E049/E050 (optimizer determinism + exact KKT enumeration) and E041/E042 residual ill-conditioned QP drift (~1-ulp, ~1e-05). Do **not** re-pin E041/E042 artifacts to silence drift.

## Initial task for next session (CLEAR)

**Default: await explicit user instructions.** Do not invent experiments, run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts without explicit direction. Routine work is handoff refresh or explicitly requested maintenance/verification only.

### Before any substantive work (if requested)

1. `git status --short --branch` — confirm HEAD/remote alignment and inspect pending handoff/symlink changes from this session.
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
3. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing any substantive change. Install deps if needed: `pip install -r requirements.txt`.

### If verification / reproduction is requested

- Always use **`SEED=42`**.
- Scopes: `make check` / `SEED=42 bash scripts/check.sh` (fast guards), `SEED=42 python3 verify_convention_robustness.py` (read-only), `SEED=42 python3 run_all_verification.py` (quick ~8m), `--extended` (~21m), `--full` (~15m), `--skip-slow`.
- Verification overwrites and restores `experiments/*.json`; **never leave a run half-finished** and **never commit verification output** over goldens. Restore if interrupted: `SEED=42 python3 run_all_verification.py --restore-only`.
- Do **not** re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` to silence drift. Re-pin only with explicit direction, deliberate update commands, and ledger justification.

## Reproduction / verification commands (run only if explicitly requested)

```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 verify_convention_robustness.py
SEED=42 python3 run_all_verification.py
SEED=42 python3 run_all_verification.py --extended
SEED=42 python3 run_all_verification.py --full
SEED=42 python3 run_all_verification.py --restore-only
SEED=42 python3 run_all_verification.py --skip-slow
make check / make verify / make verify-quick / make verify-extended / make verify-full
```

## Guardrails

- Always use **SEED=42** for reproducibility/verification runs.
- Never commit driver verification output over canonical goldens (`experiments/*.json`).
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction and ledger justification.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (template: `.github/workflow-templates/verification-gate.yml`; maintainer action required).
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and a ledger update.
- Never commit secrets/keys; never log secrets.

## Key references

- `AGENTS.md` — commands, reproducibility, baseline/guard invariants
- `ledger/RESEARCH_LEDGER.md` — dispositions and open items
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints
- `experiments/*.json` — canonical research artifacts
- `scripts/check.sh`, `run_all_verification.py`, `scripts/repoint_handoff.py`

## Handoff provenance

- **Durable artifact (this session):** `handoff_2026-11-14T05-37-35Z_INITIAL_TASK.md` (repo root).
- **Operational pointers:** repointed to this artifact with `python3 scripts/repoint_handoff.py handoff_2026-11-14T05-37-35Z_INITIAL_TASK.md`.
- **Supersedes operationally:** prior durable handoffs and generic pointers (retained for history), including `handoff_2026-11-14T05-36-27Z_INITIAL_TASK.md`.
- This session verified state only (timestamp, HEAD, prior handoff delta, absence of `.verify_snapshot`/`.verify_reports`) and created/repointed this durable handoff; no experiments, ledgers, baselines, or source files were modified.
