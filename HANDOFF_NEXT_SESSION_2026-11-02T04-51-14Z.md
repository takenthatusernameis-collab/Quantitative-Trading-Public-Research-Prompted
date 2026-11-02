# Handoff: Next Agentic Work Session
**Timestamp (UTC):** 2026-11-02T04:51:14Z
**Handoff from:** current session
**Repo:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Initial Task (Start Here)
**PRIMARY: Verify baseline integrity before doing any new work.**

1. Ensure a clean, recoverable state:
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   - This runs py_compile, tests, `check_goldens_clean.py`, `check_golden_baseline.py`, and convention checks.
   - If it reports a golden mismatch, **do not commit**. Restore per AGENTS.md: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/` (only if HEAD matches the pinned baseline; otherwise restore from the commit that matches `ledger/golden_baseline.json`).
   - If a stale snapshot is pending, recover it first.

2. Confirm working tree is clean and baselines match:
   ```bash
   git status --short
   SEED=42 python3 scripts/check_golden_baseline.py
   SEED=42 python3 scripts/check_data_coverage.py
   git log -1 --oneline
   ```

## Context
- **Research phase complete (E001–E043).** Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.
- **Canonical artifacts:** `experiments/*.json` are goldens. The verification suite backs up/restores them and must never be left half-finished (`.verify_snapshot/` with `ACTIVE.json` is used for recovery).
- **Data:** Pinned vintages in `data/vintages.json` and `data/fundamentals_vintages.json`. Many caches are gitignored except pinned files. Offline reproduction is enforced via `QUANT_RESEARCH_OFFLINE=1` in verification.
- **Known gotchas:** Optimizer determinism (E049) means some grids may still show numeric drift; do **not** re-pin goldens to silence it. E029/E030 reproductions are sensitive to pinned inputs/snapshots.

## Next Suggested Steps
1. **Integrity check** (above) — block on any failure.
2. **Review ledger** for open items: read `ledger/RESEARCH_LEDGER.md` (look for `OPEN`, `TODO`, or items marked needing follow-up). Pay particular attention to E041/E042 numeric drift and any unpinned data asks.
3. **Only after clean state:** propose a concrete, pre-registered next task (experiment/fix/refactor) before writing code. If the task would change goldens, follow the re-pinning rules in AGENTS.md explicitly.

## Critical Rules
- Always use `SEED=42`.
- Never leave `run_all_verification.py` interrupted. Use `--restore-only` if needed.
- Never re-pin goldens as a side effect of running verification. Re-pinning requires `python3 scripts/check_golden_baseline.py --update` and should be intentional.
- Follow pre-registration, multiple-testing discipline ("reported, not gated"), and falsification expectations.
- Run `python3 -m py_compile` on changed files; run lint/typecheck if the repo provides commands.

## Quick Reference Commands
```bash
# Fast checks
SEED=42 bash scripts/check.sh
SEED=42 python3 verify_convention_robustness.py

# Verification
SEED=42 python3 run_all_verification.py        # quick
SEED=42 python3 run_all_verification.py --extended
SEED=42 python3 run_all_verification.py --full

# Recovery
SEED=42 python3 run_all_verification.py --restore-only
```
