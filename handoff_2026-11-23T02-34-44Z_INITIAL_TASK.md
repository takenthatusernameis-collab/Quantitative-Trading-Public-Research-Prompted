# Agentic Work Session Handoff

**Timestamp**: 2026-11-23T02-34-44Z
**Workspace**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

---

## >>> INITIAL TASK MESSAGE FOR THE NEXT SESSION <<<

Do **not** spend this session only writing another `handoff_*_INITIAL_TASK.md`. This repo is in a handoff-refresh loop (ledger E652–E720; thousands of tracked handoff files). Break it by doing substantive work.

In priority order:

1. **Provision dependencies and run the real verification suite.** `pypi.org` is reachable; `python3 -m pip` 24.0 available.
   ```bash
   python3 -m pip install -r requirements.txt
   SEED=42 python3 run_all_verification.py --extended
   ```
   Report exactly which drivers reproduce with 0 differences and which drift (numeric vs structural). Do **not** re-pin any golden to silence drift.

2. **Address E041/E042 ill-conditioned-QP drift** (E041: 133 numeric diffs; E042: ~1e-05 tangency-QP drift on 1-ulp perturbation). The optimizer exit-status rule is pinned by `tests/test_portfolio_opt.py`. Remaining drift is inherent ill-conditioning — document or fix the root cause; do **not** re-pin artifacts to hide it.

3. **Only if explicitly requested by the user**: new pre-registered research (a new E-numbered driver with `pre_registered` block, gates, falsification expectation). Goalposts are never moved post-hoc.

4. **If none of the above is possible**, *propose* (do not execute) a `.gitignore` + `git rm --cached` cleanup of the historical handoff clutter, and stop. Do not silently delete tracked history.

End your turn with real work done, not a refreshed handoff.

---

## Project Context

Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. Research phase complete (E001–E043). Strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Quick Start

```bash
SEED=42 bash scripts/check.sh          # convention check (~seconds, offline)
SEED=42 python3 run_all_verification.py --extended   # ~21 min
```

## Baseline Integrity

`experiments/*.json` are canonical artifacts; the suite overwrites then restores them. Never leave a run half-finished. Recovery: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`. Never re-pin goldens as a side effect of the suite.

## State verified at handoff time

- HEAD `fce096c2 chore(kilo): checkpoint agent session` on `main`; `origin/main...HEAD` = `0  0`.
- `git diff HEAD -- experiments/` empty; no golden/data artifacts modified.
- Only modified tracked files: `**/__pycache__/*.pyc` (bytecode churn, not artifacts).
- Guards not re-run this session (hashlib-only); full verification suite NOT yet run after dependency provisioning.

## Constraints honored by this handoff

No golden/data baseline re-pinned, no verification output committed, no new research performed, no commit made.
