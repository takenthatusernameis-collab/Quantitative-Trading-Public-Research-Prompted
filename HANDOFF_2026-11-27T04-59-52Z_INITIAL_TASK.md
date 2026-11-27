# Handoff — Next Agentic Work Session

**Timestamp:** 2026-11-27T04:59:52Z
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Durable artifact:** `HANDOFF_2026-11-27T04-59-52Z_INITIAL_TASK.md` (repo root)
**Latest pointer:** `current` -> `HANDOFF_2026-11-27T04-59-52Z_INITIAL_TASK.md`

> Prioritized backlog in this durable artifact: **(1)** verify working-tree cleanliness against HEAD (`git diff HEAD -- experiments/` empty), **(2)** provision deps (`pip install -r requirements.txt`), **(3)** run `scripts/check.sh` then `run_all_verification.py --extended`, report drift, do not re-pin. Then stop.

## Project Context

Independent reproducible quantitative-strategy research on 2014–2026 US equities,
futures, and macro data. Research phase complete (E001–E043). Surviving validated
strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Git State

- Branch: `main`; HEAD `27a6141fe74afe166516b8912b7e6197dfab8df2` == `origin/main`.
- Working tree clean for canonical artifacts (`experiments/`, `data/`, `ledger/`).
- `git diff HEAD -- experiments/` empty; `.verify_snapshot/` and `.verify_reports/` absent.

## Quick Commands

```bash
SEED=42 bash scripts/check.sh                    # fast convention-robustness + template validation (offline)
SEED=42 python3 run_all_verification.py          # quick full verification (~8 min)
SEED=42 python3 run_all_verification.py --extended   # +18 more drivers, structural match (~21 min)
SEED=42 python3 run_all_verification.py --restore-only  # recover goldens after an interrupted run
```

## Key Notes

- **Seed**: always `SEED=42` (walk-forward + placebo RNG).
- **Golden files**: `experiments/*.json` are canonical — never commit verification output over them.
- **Recovery**: `SEED=42 python3 run_all_verification.py --restore-only` if interrupted (or `git checkout <pinned-commit> -- experiments/<file>`).
- **Dependencies**: NOT provisioned this session; run `pip install -r requirements.txt` first.
- **Optimizer determinism**: E050 exact KKT active-set solver (commit `72dc947`) made E041/E042 bit-reproducible; do not re-pin to silence a tolerance violation — none remains.
- **Offline mode**: `QUANT_RESEARCH_OFFLINE=1` enforced during verification; unpinned input fails hard.

## Last Verification Status

Baseline last verified clean at 2026-11-26T19:17:39Z (goldens clean, 107 pinned goldens match baseline, 35 pinned data inputs present/tracked/unchanged). No tracked source changes since. Not re-run this session (deps not yet confirmed provisioned).

## Prior Handoffs

Current durable artifact: `HANDOFF_2026-11-27T04-59-52Z_INITIAL_TASK.md` (supersedes `HANDOFF_2026-11-27T04-55-11Z_INITIAL_TASK.md`).
