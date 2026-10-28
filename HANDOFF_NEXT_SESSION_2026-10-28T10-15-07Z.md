# HANDOFF_NEXT_SESSION_2026-10-28T10-15-07Z

**Timestamp (UTC):** 2026-10-28T10:15:07Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Working tree:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**HEAD:** 14748a4

## INITIAL TASK (START HERE)

1. **Verify baseline integrity (MANDATORY)**
   Before making any changes, confirm golden files match HEAD and are pinned correctly:
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   This runs convention checks, `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, and tests. All must pass.

2. **Check for in-progress verification**
   If `.verify_snapshot/ACTIVE.json` exists, a verification run may be live or stale.
   - If live: do **not** kill it unless necessary; wait for completion.
   - If stale: recover the canonical goldens before proceeding.
   ```bash
   SEED=42 python3 run_all_verification.py --restore-only
   git checkout -- experiments/  # fallback if needed
   ```

3. **Decide next action based on state**
   After baseline is clean, read `ledger/RESEARCH_LEDGER.md` for current standing items and pick the highest-priority open task. Do not re-run the full verification suite unless explicitly needed.

## CURRENT CONTEXT

- **Phase:** Research complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- **Goldens are canonical:** `experiments/*.json` must remain consistent with `ledger/golden_baseline.json`. Never re-pin as a side effect of running verification.
- **Baseline guards (enforced):** `scripts/check_goldens_clean.py` (working tree vs HEAD) and `scripts/check_golden_baseline.py` (tracked artifacts vs pinned SHA-256). Both run in `scripts/check.sh`.
- **Optimizer determinism (E049):** `src/portfolio_opt.py` validates against problem constraints (not solver exit status). Ill-conditioned tangency QP still causes numeric drift in E041/E042 grids. **Do not re-pin these to silence drift.**
- **Data coverage:** Enforced by `scripts/check_data_coverage.py` + `ledger/data_baseline.json`. E029 fundamentals pinned in `data/fundamentals/`. E030 panel pinned (committed). Missing/unpinned inputs will fail hard under `QUANT_RESEARCH_OFFLINE=1`.
- **Verification modes:** `make verify-quick` (~8 min), `make verify-extended` (~21 min), `make verify-full` (longer). Extended drift report goes to `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json` (gitignored).
- **CI:** Workflow cannot be created by agents; template at `.github/workflow-templates/verification-gate.yml`.

## QUICK REFERENCE COMMANDS

```bash
# Integrity
SEED=42 bash scripts/check.sh

# Verification
SEED=42 python3 run_all_verification.py                # quick
SEED=42 python3 run_all_verification.py --extended     # extended
SEED=42 python3 run_all_verification.py --full         # full

# Recovery
SEED=42 python3 run_all_verification.py --restore-only

# Individual drivers (examples)
SEED=42 python3 src/batch_run.py --universe large_liquid
SEED=42 python3 src/validate.py  --universe large_liquid
SEED=42 python3 experiments/run_e042.py --n-sim 50
```

## NOTES FOR NEXT AGENT

- **Strictly follow AGENTS.md** on baseline integrity. A checkpoint commit that replaces goldens is a known failure mode - guard against it.
- **Do not commit verification outputs.** If interrupted mid-run, restore goldens before committing.
- **Respect "reported not gated"** for sensitivity grids. Promotion requires dedicated pre-registered confirmatory run with full placebo.
- **Negative results are valid.** REJECTED/PARTIAL are recorded honestly.
- **Conventions:** Close-to-close v1.2.3 primary; overnight decomposition reported alongside.
- **Lint/typecheck:** If you change Python files, run `python3 -m py_compile` on them. No separate linter configured.
- **Seed:** Always use `SEED=42`.
