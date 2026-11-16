# Durable Handoff — Next Agentic Work Session

**Timestamp (UTC):** 2026-11-16T11:33:13Z
**Workspace:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Project state:** Research phase complete (E001–E043). Canonical artifacts in `experiments/*.json`; baselines pinned in `ledger/golden_baseline.json` and `ledger/data_baseline.json`. See `ledger/RESEARCH_LEDGER.md` and `AGENTS.md`.

## Initial task (start here)

1. **Establish baseline before any change**
   - `git status --short`
   - `git log -1 --oneline`
   - `SEED=42 bash scripts/check.sh`
   - Expect: exit 0 (py_compile, goldens clean vs HEAD, pinned golden/baseline match, data coverage, portfolio_opt tests, convention robustness, template validation, experiment-script imports).

2. **If integrity checks fail, recover first (do not proceed on a dirty/broken baseline)**
   - Goldens differ from HEAD or stale `.verify_snapshot/ACTIVE.json`: `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`; if HEAD itself is bad, restore pinned artifacts per `AGENTS.md`).
   - Do **not** re-pin `ledger/golden_baseline.json` / `ledger/data_baseline.json` to silence drift; re-pinning requires explicit justification and `--update` in a deliberate diff.

3. **Await explicit user direction before source/artifact changes**
   - Do not run verification modes that rewrite goldens (`run_all_verification.py` quick/extended/full) unless explicitly requested.
   - Do not modify `experiments/*.json`, baselines, or commit changes without explicit instruction.

## Known context / constraints

- `AGENTS.md`: golden artifacts are authoritative; interrupted verification can leave driver output in the worktree—restore before committing.
- Optimizer 1-ulp numeric sensitivity (ledger E049): E041/E042 grid artifacts may drift in extended checks; **do not re-pin to silence**.
- E029/E030 inputs are pinned for offline reproducibility; verification runs drivers with `QUANT_RESEARCH_OFFLINE=1`.
- CI workflow creation requires maintainer action (template: `.github/workflow-templates/verification-gate.yml`).

## Useful commands

```bash
SEED=42 bash scripts/check.sh
python3 scripts/check_golden_baseline.py
python3 scripts/check_data_coverage.py
SEED=42 python3 run_all_verification.py --restore-only
# only if explicitly requested:
# SEED=42 python3 run_all_verification.py
# SEED=42 python3 run_all_verification.py --extended
```

**Ready state:** begin at step 1; report check results and stop for user direction.