# Agentic Work Session Handoff

**Timestamp**: 2026-11-21T18:04:44Z
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Project**: Quantitative Trading Public Research (2014–2026 US equities, futures, macro)
**Predecessor handoff**: `handoff_2026-11-21T18-04-15Z_INITIAL_TASK.md` (created by session checkpoint)

## Project State

- **Research Phase**: Complete (E001–E043). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.
- **Current Focus**: Reproducibility / verification integrity of committed golden artifacts.
- **Working tree**: Clean (only the handoff files change between sessions).

## Quick Commands

```bash
# Fast convention-robustness + golden-clean check (~seconds, offline)
SEED=42 bash scripts/check.sh          # or: make check

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py           # or: make verify-quick

# Extended verification (~21 min; re-runs 18 more drivers, drift report only)
SEED=42 python3 run_all_verification.py --extended # or: make verify-extended

# Full verification (~15 min; E042 n_sim=50 + 96-config grid)
SEED=42 python3 run_all_verification.py --full     # or: make verify-full

# Recover golden artifacts if a verification run was interrupted
SEED=42 python3 run_all_verification.py --restore-only
```

## Non-Negotiable Guardrails (from AGENTS.md)

1. **`experiments/*.json` are the canonical golden baseline.** Never commit verification
   output over them. The suite backs them up to `.verify_snapshot/` and restores them; a
   run must never be left half-finished. If `scripts/check.sh` reports a golden mismatch,
   fix it **before** committing.
2. **Never re-pin a golden artifact to silence drift.** The committed golden is the
   authoritative record, not the latest re-run. Re-pinning requires an explicit, justified
   `--update` that shows up in the diff.
3. **Seed is always `SEED=42`** (walk-forward + placebo RNG).
4. **Offline reproducibility**: the verification suite runs drivers with
   `QUANT_RESEARCH_OFFLINE=1`. Every `data.download()` input must be committed and pinned
   in `ledger/data_baseline.json` (enforced by `scripts/check_data_coverage.py`). E029
   fundamentals are separately pinned under `data/fundamentals/` per
   `data/fundamentals_vintages.json`.
5. **Optimizer determinism (ledger E049)**: `src/portfolio_opt.py` validates solver answers
   on problem constraints, not on solver exit status. The tangency QP is ill-conditioned
   (~1-ulp input sensitivity moves `min_var` answers ~1e-05); do **not** re-pin E041/E042
   to hide this.

## Open Items (from ledger)

- **E041**: optimizer fault fixed; 133 numeric differences remain (ill-conditioned QP). Still
  drifts past the 1e-4 tolerance — expected, not a regression.
- **E042**: grid artifacts drift by 29–133 differences (same root cause).
- See `ledger/RESEARCH_LEDGER.md` entries **E045, E048, E049** for full detail.
- **CI gate**: `.github/workflows/verification-gate.yml` cannot be created by agents
  (GITHUB_TOKEN lacks `workflows` push permission). A maintainer must create it from
  `.github/workflow-templates/verification-gate.yml` (see `VERIFICATION_GATE_TEMPLATE.md`).

## Initial Task for the Next Session

1. Run `SEED=42 bash scripts/check.sh` first (fast, seconds) to confirm the goldens are
   clean and conventions hold. If it reports a golden mismatch, **stop and fix** before
   doing anything else; recover with
   `SEED=42 python3 run_all_verification.py --restore-only` if a prior run was interrupted.
2. Then run `SEED=42 python3 run_all_verification.py --extended` (~21 min) and inspect
   `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json`. Confirm that **E030 and E029
   reproduce with 0 differences** and that only **E041** (and, if present, E042) drift for
   the known ill-conditioned-QP reasons above. Any *new* driver drift or any structural
   (non-numeric) difference is a real regression — investigate it, do not re-pin.
3. Record the outcome as a ledger note if anything changed, then leave the working tree
   clean (goldens restored) before finishing.

Do not modify golden artifacts, do not re-pin them to silence drift, and do not commit
verification output.

(End of file)