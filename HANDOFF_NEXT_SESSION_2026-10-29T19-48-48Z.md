# HANDOFF — Next Agentic Work Session

**Timestamp (UTC):** 2026-10-29T19-48-48Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Working directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Initial Task (clear)
**Primary objective:** Establish a clean baseline and be ready to work from the committed canonical state before making any changes.

1. **Verify repo state** (read-only)
   - `git status --short && git log -1 --oneline`
   - Confirm no in-progress verification (check `.verify_snapshot/ACTIVE.json` if present)

2. **Enforce baseline integrity** (required)
   - Run `SEED=42 bash scripts/check.sh`
   - Must pass all steps: py_compile, golden cleanliness, golden baseline pinning, data coverage, tests (including portfolio optimizer determinism), convention robustness, batch run/validate quick checks.
   - If it reports golden mismatches: **do not commit**. Follow AGENTS.md recovery (restore via `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/` as appropriate). If HEAD already contains a captured run, restore from the pinned commit per `ledger/golden_baseline.json`.

3. **Orient on scope**
   - Read `ledger/RESEARCH_LEDGER.md` for current disposition (research phase complete E001–E043; surviving strategies documented).
   - Note open item: E041 optimizer drift (133 numeric diffs) is accepted for now — **do not re-pin goldens to silence it**.

## Current Known State
- **Canonical artifacts:** `experiments/*.json` are committed goldens. Verification backs up to gitignored `.verify_snapshot/` and restores after runs; never leave a run half-finished.
- **Data coverage:** Enforced via `scripts/check_data_coverage.py` (all downloads must have tracked/cache entries pinned in `ledger/data_baseline.json`). Re-pin only with `--update` when intentionally adding inputs.
- **Optimizer determinism:** `src/portfolio_opt.py` validates on constraints (not solver exit status). Pinned by `tests/test_portfolio_opt.py`.
- **Pinned vintages:** `data/vintages.json` (2026-10-12), 2026-10-11 committed for specific drivers, fundamentals pinned in `data/fundamentals/` per `data/fundamentals_vintages.json` for offline E029.

## Quick Commands
```bash
# Baseline check
SEED=42 bash scripts/check.sh

# Quick/full verification (only if needed)
SEED=42 python3 run_all_verification.py        # ~8 min
SEED=42 python3 run_all_verification.py --extended  # ~21 min
SEED=42 python3 run_all_verification.py --full       # ~15 min

# Recovery if interrupted
SEED=42 python3 run_all_verification.py --restore-only
```

## Guardrails
- Always use `SEED=42`
- Never re-pin goldens as a side effect of running verification
- Do not commit verification output if interrupted; restore first
- Follow `AGENTS.md` "Baseline Integrity" and "Do not commit verification output" strictly
- Offline mode enforced by verification (`QUANT_RESEARCH_OFFLINE=1`) — missing cache = hard failure

## Pointers
- `AGENTS.md` — full commands, conventions, guards
- `ledger/RESEARCH_LEDGER.md` — experiment dispositions
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinning
- `scripts/check.sh`, `run_all_verification.py` — verification flow
