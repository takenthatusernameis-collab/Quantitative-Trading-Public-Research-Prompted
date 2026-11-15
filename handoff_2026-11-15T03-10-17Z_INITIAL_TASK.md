# Durable Handoff — Next Agentic Work Session

**Created:** 2026-11-15T03:11:03Z
**Session:** main code agent (ending)
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Commit:** 4666edad chore(kilo): checkpoint agent session
**Branch:** main, up to date with origin/main

## Current state

- Working tree is clean except for `__pycache__/*.pyc` artifacts (from `py_compile` checks). No source or `experiments/*.json` modifications.
- `experiments/*.json` golden files are intact at HEAD; no verification run in progress (no `.verify_snapshot/ACTIVE.json`).
- Board is empty; no peer coordination in flight.
- Prior handoffs (HANDOFF_NEXT_SESSION_2026-11-15T03-10:37Z.md, handoff_2026-11-14T23:25:07Z_INITIAL_TASK.md) describe the same stable state; nothing material changed this turn.

## Recommended initial task for next session

Run the convention-robustness check first (fast, offline, seconds):

```bash
SEED=42 bash scripts/check.sh
# or: make check
```

If green, proceed to quick verification:

```bash
SEED=42 python3 run_all_verification.py --skip-slow
# or: make verify-quick
```

**Critical guard (per AGENTS.md):** never leave a verification run half-finished. If interrupted, recover with:

```bash
SEED=42 python3 run_all_verification.py --restore-only
# or: git checkout -- experiments/
```

Do not commit verification output or re-pin goldens as a side effect of running the suite.

## Known constraints (do not "fix" by re-pinning)

- **Canonical artifacts:** `experiments/*.json` are golden baselines; the suite overwrites then restores them. Re-pinning requires explicit `python3 scripts/check_golden_baseline.py --update`.
- **Seed:** always `SEED=42`. Data/fundamentals vintages and cache coverage are enforced (`ledger/data_baseline.json`, `data/vintages.json`, `data/fundamentals_vintages.json`, `scripts/check_data_coverage.py`). Runs use `QUANT_RESEARCH_OFFLINE=1` where applicable.
- **Extended drift (expected, reporting only):** 15/18 drivers 0-diff; **E041** has ~133 numeric diffs (1-ulp sensitivity of ill-conditioned QP; optimizer determinism fixed per ledger E049, decision REJECTED 3/5 unchanged) — still exceeds 1e-4 tolerance, **do not re-pin**. E029/E030 offline-reproducible with pinned snapshots. See `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json` (gitignored) after `--extended`.
- **Working tree note:** only `__pycache__/*.pyc` churn is present; treat as non-canonical noise.

## References

- `AGENTS.md` — project commands, baseline integrity, reproducibility rules.
- `scripts/check.sh` — convention-robustness + golden guards (0.5c, 0.5d).
- `ledger/RESEARCH_LEDGER.md` — surviving validated strategies (E001–E043 complete) and open items (E041/E042 QP conditioning).
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints.
- `.github/workflow-templates/verification-gate.yml` + `VERIFICATION_GATE_TEMPLATE.md` — CI template (maintainer-created only).