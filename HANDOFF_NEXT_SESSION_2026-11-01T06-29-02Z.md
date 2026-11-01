# DURABLE HANDOFF — Next Agentic Work Session

**Timestamp (UTC):** 2026-11-01T07:24:59Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Current State
- **Research phase:** Complete (E001–E043). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.
- **Canonical artifacts:** `experiments/*.json` are the committed goldens. The verification suite backs them up/restores them via `.verify_snapshot/` (gitignored) and will refuse to start if a live run owns it.
- **Baseline integrity is enforced:** `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, and `scripts/check_data_coverage.py` are first-class guards (also run by `scripts/check.sh`).
- **Offline reproducibility:** Data coverage is pinned in `ledger/data_baseline.json`. Pinned vintages exist in `data/vintages.json` and fundamentals in `data/fundamentals_vintages.json` / `data/fundamentals/`.

## Known Open Items (Do Not Ignore)
- **E049 — Optimizer determinism (ill-conditioned QP):** `src/portfolio_opt.py` now validates against constraints (not solver exit status). Tangency/min-var grids still show 1-ulp sensitivity. E041 currently reports ~133 numeric differences in `--extended` (structural diffs resolved). **Do not re-pin goldens/data to silence this drift.**
- **Extended verification drift reporting:** `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json` is gitignored and reporting-only. Treat it as diagnostic, not a reason to overwrite canonical artifacts.
- **CI:** The intended GitHub workflow cannot be created by agents. Use local equivalents (`make check` / `make verify-*`).

## Immediate Initial Task (For Next Session)
1. **Verify clean baseline.** Run `SEED=42 bash scripts/check.sh`. It must pass with no golden/data coverage mismatches.
2. **If dirty from a previous interrupted run:** Restore before doing anything else — `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/` only if HEAD is known-good). If `check_goldens_clean.py` reports a *live* verification run, do not force-kill blindly — recover first.
3. **Review ledger open items.** Read `ledger/RESEARCH_LEDGER.md` for any "OPEN" follow-ups (focus on E049 and related). Decide next action based on that review, not by re-running verification to "refresh" goldens.
4. **Only proceed if clean.** Do not re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` as a side effect of running the verification suite.

## Guardrails
- **Never leave verification half-finished.** The backup lives in `.verify_snapshot/` with `ACTIVE.json`. If interrupted, recover with `--restore-only`.
- **Goldens are authoritative.** Replacing artifacts requires explicit re-pinning (`python3 scripts/check_golden_baseline.py --update` / `python3 scripts/check_data_coverage.py --update`) and must be intentional.
- **Pre-registration discipline.** Do not move goalposts post-hoc. Sensitivity grids are reported, not gated.
- **Offline-safe.** The suite runs drivers with `QUANT_RESEARCH_OFFLINE=1`. Unpinned inputs will fail hard by design.
- **Seeds.** Always use `SEED=42`.

## Quick Commands
```bash
# Baseline integrity (fast)
SEED=42 bash scripts/check.sh

# Verification
SEED=42 python3 run_all_verification.py --quick      # ~8 min
SEED=42 python3 run_all_verification.py --extended   # ~21 min
SEED=42 python3 run_all_verification.py --full       # ~15 min

# Recovery
SEED=42 python3 run_all_verification.py --restore-only

# Targeted checks
SEED=42 python3 verify_convention_robustness.py
SEED=42 python3 scripts/check_golden_baseline.py
SEED=42 python3 scripts/check_data_coverage.py
```