# Durable Handoff — Next Agentic Work Session

**Timestamp (UTC):** 2026-11-16T05:51:23Z
**Canonical artifact:** `handoff_2026-11-16T05-51-23Z_INITIAL_TASK.md`
**HEAD:** `4e27f7fab83726ef5e7e718d7ccfc24333a0a2a6` (`main`, in sync with `origin/main`, 0 ahead / 0 behind)
**Supersedes:** `handoff_2026-11-16T05-50-27Z_INITIAL_TASK.md` (retained for history)

## Repository state (as of this handoff)
- Research phase **complete (E001–E043/E051 context)**; surviving validated strategies and dispositions are in `ledger/RESEARCH_LEDGER.md`. No new research performed in this session.
- Working tree: only pre-existing tracked `__pycache__/*.pyc` modifications present (gitignored-pattern files but currently tracked/modified in this checkout). **Do not commit `__pycache__` churn.**
- The two most recent commits (`2a911499`, `4e27f7fa`) are `chore(kilo): checkpoint agent session` — they contain only handoff symlink repointing + new handoff files, no code/data changes.
- No `.verify_snapshot/` or `.verify_reports/` present; no interrupted verification run detected.
- Canonical golden artifacts: `experiments/*.json` (pinned in `ledger/golden_baseline.json`); data inputs pinned in `ledger/data_baseline.json` / `data/vintages.json` / `data/fundamentals_vintages.json`.

## Integrity / guardrails (must preserve)
- `SEED=42` for all verification/reproduction runs.
- **Never leave verification half-finished.** Suite backs up goldens to `.verify_snapshot/` and restores them; if interrupted run `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned artifact from baseline commit, not blindly from a contaminated HEAD).
- **Never re-pin goldens/baselines** (`ledger/golden_baseline.json`, `ledger/data_baseline.json`) as a side effect of verification.
- Do not commit verification output, `.verify_reports/`, `.verify_snapshot/`, `__pycache__`, or captured artifact drift as a new baseline.
- `check_goldens_clean.py` catches working-tree vs HEAD drift and stale snapshots; `check_golden_baseline.py` catches committed baseline replacement — treat failures as blockers before commit.
- Optimizer determinism (ledger E049): validate solutions on constraints, not solver exit status; E041/E042 grid artifacts have known 1-ulp sensitivity (do not re-pin to silence).

## Quick reproduction / verification commands
```bash
SEED=42 bash scripts/check.sh            # fast offline guards (~seconds)
SEED=42 python3 run_all_verification.py  # verify-quick (~8 min)
SEED=42 python3 run_all_verification.py --extended
SEED=42 python3 run_all_verification.py --full
SEED=42 python3 run_all_verification.py --restore-only  # recovery only
```

## Clear initial task for next session
1. **Baseline health (read-only first):** run `SEED=42 bash scripts/check.sh`. If it fails, resolve the reported guard failure without re-pinning baselines or committing verification artifacts; if it reports a golden mismatch, restore the pinned baseline per AGENTS.md before any other work.
2. **If a substantive change is requested:** confirm scope, run the appropriate verification tier for touched areas (`check.sh` minimum; `verify-quick`/`--extended`/`--full` as warranted), and ensure `experiments/` goldens and baseline pins remain unchanged unless there is an explicit, reviewed re-pin with evidence.
3. **Handoff hygiene:** at session end, refresh this durable handoff (new UTC-stamped file + `python3 scripts/repoint_handoff.py <file>`), record HEAD/actions/results/constraints, and leave the tree free of stale `.verify_snapshot/` and uncommitted verification output.

**Default posture:** maintenance/verification only unless explicitly directed otherwise. Preserve pre-registration, gates, falsification expectations, sensitivity discipline, and validated constructions.