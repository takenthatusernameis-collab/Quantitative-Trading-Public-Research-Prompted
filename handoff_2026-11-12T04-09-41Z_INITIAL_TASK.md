# Agentic Handoff — Initial Task Message

**Created:** 2026-11-12T04:09:41Z (UTC)
**Repo:** `Quantitative-Trading-Public-Research-Prompted`
**HEAD:** `7fc43ca1 chore(kilo): checkpoint agent session` (research phase complete, E001–E043)

## Immediate first actions
1. Inspect workspace state: `git status --short` (note: `src/__pycache__/cache_keys.cpython-312.pyc` is currently modified in this snapshot; do not commit generated artifacts/pyc).
2. Confirm baseline/invariants before any edits: `SEED=42 bash scripts/check.sh` (or `make check`).
3. If `check.sh` reports golden mismatches under `experiments/`, restore/fix before committing — never commit verification output or leave a verification run half-finished. Recovery: `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/` only when HEAD holds the true golden).

## Repo context / conventions
- Canonical artifacts: `experiments/*.json` are committed goldens; verification runs overwrite then restore them.
- Reproducibility: always use `SEED=42`. Data inputs/caches are pinned; suite re-executes drivers with `QUANT_RESEARCH_OFFLINE=1`.
- Read `AGENTS.md` and `ledger/RESEARCH_LEDGER.md` for commands, guards, and experiment dispositions.
- No separate linter configured; run `python3 -m py_compile` on changed Python files. Follow existing code style; no comments/emojis unless requested. Do not commit secrets.

## Useful commands
- `SEED=42 bash scripts/check.sh` / `make check` — fast convention/baseline checks
- `SEED=42 python3 run_all_verification.py` — quick verification (~8 min)
- `SEED=42 python3 run_all_verification.py --extended` — extended (~21 min)
- `SEED=42 python3 run_all_verification.py --full` — full (~15 min)
- `SEED=42 python3 verify_convention_robustness.py` — convention robustness only

## Known open items (do not paper over)
- **E041:** 133 numeric diffs remain from 1-ulp QP sensitivity (ledger E049); extended verification still reports drift. Do **not** re-pin `experiments/e041*.json` to silence this.
- **E042:** min-var confirmatory is **PARTIAL**; confirmatory run with full placebo remains pending.
- **Process:** never re-pin golden/data baselines as a side effect of verification; baseline replacement requires explicit `--update` + review.

## Suggested next-session task
- Start with `git status --short` and `SEED=42 bash scripts/check.sh` to establish a clean, verified baseline.
- Address the E041/E042 open items only via pre-registered, evidence-backed work (see ledger entries E049 and E042); record outcomes in the ledger and keep dispositions honest (no post-hoc gate moving).
