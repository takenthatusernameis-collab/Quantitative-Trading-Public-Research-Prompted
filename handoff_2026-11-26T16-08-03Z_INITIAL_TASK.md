# Durable Handoff — Initial Task for Next Agentic Work Session

**Timestamp:** 2026-11-26T16:08:03Z
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Durable artifact:** `handoff_2026-11-26T16-08-03Z_INITIAL_TASK.md` (repo root)
**Supersedes:** `handoff_2026-11-26T15-19-16Z_INITIAL_TASK.md` (and `.handoff.md` prior target).

---

## Project Context

Independent reproducible quantitative-strategy research on 2014–2026 US equities,
futures, and macro data. Research phase complete (E001–E043). Surviving validated
strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Git State

- Branch: `main`
- Working tree: clean apart from tracked build noise `src/__pycache__/cache_keys.cpython-312.pyc` (modified, safe to ignore / `git restore`)
- No live verification run in progress (`.verify_snapshot/` and `.verify_reports/` absent)

## Quick Commands

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh
#   or
make check

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py
#   or
make verify-quick

# Extended verification (~21 min; 26 drivers vs committed goldens, numeric_tol=1e-4)
SEED=42 python3 run_all_verification.py --extended
#   or
make verify-extended

# Recover golden artifacts after an interrupted verification run
SEED=42 python3 run_all_verification.py --restore-only
```

## Key Notes

- **Seed**: Always use `SEED=42` (walk-forward + placebo RNG).
- **Golden files**: `experiments/*.json` are canonical artifacts — never commit verification output over them.
- **Recovery**: `SEED=42 python3 run_all_verification.py --restore-only` if interrupted (or `git checkout <pinned-commit> -- experiments/<file>`).
- **Dependencies**: NOT provisioned this session — run `pip install -r requirements.txt` first.
- **Optimizer determinism**: E050 exact KKT active-set solver (commit `72dc947`) made E041/E042 bit-reproducible; do not re-pin to silence a tolerance violation — none remains.

## Initial Task for Next Session

1. Verify working-tree cleanliness (`git status`).
2. Install deps: `pip install -r requirements.txt`.
3. Run `SEED=42 bash scripts/check.sh` (goldens clean, golden baseline, data coverage, optimizer determinism).
4. If clean, run `SEED=42 python3 run_all_verification.py --extended` and report any drift precisely (per-driver, numeric vs structural, worst drift as multiple of tolerance). Do NOT re-pin goldens.
5. If interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only` before committing anything.

Default if no explicit instruction: await explicit user instructions; otherwise perform Task 1 above.

## Integrity Rules

- Never leave verification half-finished; it overwrites `experiments/*.json` and restores afterward.
- Never re-pin goldens as a side effect of verification — re-pin only for a deliberate code change recorded in the ledger first.
- Never commit verification output; it silently replaces the canonical baseline.

---

**Next session:** install deps → run Task 1 → report drift → stop. Do not refresh this handoff unless verified state materially changes.