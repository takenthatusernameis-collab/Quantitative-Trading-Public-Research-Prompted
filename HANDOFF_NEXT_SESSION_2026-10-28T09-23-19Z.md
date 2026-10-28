# HANDOFF_NEXT_SESSION_2026-10-28T09-23-19Z

**Timestamp (UTC):** 2026-10-28T09:23:19Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Working tree:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**HEAD:** 5fbf51f114ceda56998c03f381bc7bbc4974e15f (chore(kilo): checkpoint agent session)
**Working tree:** clean
**.verify_snapshot:** absent (no live/stale verification run)

## INITIAL TASK (START HERE)

1. **Verify baseline integrity (MANDATORY — do this before anything else)**
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   Runs convention checks, `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, and tests. All must pass. Confirms `experiments/` goldens match HEAD and are pinned in `ledger/golden_baseline.json`.

2. **Confirm no live/stale verification snapshot**
   - If `.verify_snapshot/ACTIVE.json` exists, a run may be live or stale.
     - Live: do **not** kill it unless necessary; wait for completion.
     - Stale: recover canonical goldens:
       ```bash
       SEED=42 python3 run_all_verification.py --restore-only
       # fallback
       git checkout -- experiments/
       ```

3. **Decide next action**
   Once baseline is clean, read `ledger/RESEARCH_LEDGER.md` for standing open items and pick the highest-priority task. Research phase complete (E001–E043); surviving validated strategies are documented in the ledger. Do not re-run the full verification suite unless explicitly needed.

## CURRENT CONTEXT

- **Phase:** Research complete (E001–E043). Surviving validated strategies in `ledger/RESEARCH_LEDGER.md`.
- **Goldens are canonical:** `experiments/*.json` must stay consistent with `ledger/golden_baseline.json`. Never re-pin as a side effect of running verification.
- **Baseline guards (enforced):** `check_goldens_clean.py` (working tree vs HEAD) and `check_golden_baseline.py` (tracked artifacts vs pinned SHA-256). Both run in `scripts/check.sh`.
- **Optimizer determinism (E049):** `src/portfolio_opt.py` validates solver answers against problem constraints, not exit status. Ill-conditioned tangency QP still causes numeric drift in E041/E042 grids. **Do not re-pin to silence drift.**
- **Data coverage:** Enforced by `scripts/check_data_coverage.py` + `ledger/data_baseline.json`; fails hard under `QUANT_RESEARCH_OFFLINE=1` for missing caches. E029 fundamentals pinned in `data/fundamentals/`; E030 panel committed.
- **Verification modes:** `make verify-quick` (~8 min), `make verify-extended` (~21 min), `make verify-full` (longer). Extended drift report: `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json` (gitignored).
- **CI:** Cannot be created by agents; template at `.github/workflow-templates/verification-gate.yml`.

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

- Always use `SEED=42` for reproducibility (walk-forward + placebo RNG).
- Follow cost model (tc=0.5bps + slippage=0.2bps) and next-day open execution.
- Do not commit verification output or modify golden files without justification.
- Run `SEED=42 bash scripts/check.sh` before committing.
- If adding new data inputs, commit files and re-pin via `scripts/check_data_coverage.py --update`.
- Pre-registration + multiple-testing discipline: sensitivity grids are "reported, not gated"; a config clearing gates needs a dedicated pre-registered confirmatory run with full placebo before promotion.
