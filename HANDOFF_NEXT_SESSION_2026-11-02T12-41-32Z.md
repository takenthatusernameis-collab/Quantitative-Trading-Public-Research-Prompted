# INITIAL TASK FOR NEXT AGENTIC SESSION

**Timestamp:** 2026-11-02T12:41:32Z
**Handoff Type:** Durable handoff (clear initial task)
**Origin Session:** Current agentic session

## Goal
Pick up from a known-good baseline and proceed with minimal drift. Preserve the canonical golden artifacts and follow the project's verification discipline.

## Project State
- **Repo:** Quantitative-Trading-Public-Research-Prompted
- **Phase:** Research complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`
- **Canon:** `experiments/*.json` are committed goldens. Do **not** overwrite them via ad-hoc runs.
- **Seeds:** Always use `SEED=42`
- **Mode:** Prefer offline verification (`QUANT_RESEARCH_OFFLINE=1` enforced)

## Known Open Items (watchlist)
- **E041 drift:** 133 numeric differences remain due to 1-ULP sensitivity in ill-conditioned tangency QP (optimizer determinism fixed per E049). Do **not** re-pin to silence. Extended verification will still report drift.
- **Data coverage:** Enforced by `scripts/check_data_coverage.py`. Any new data inputs must be committed and re-pinned.
- **Baseline guards:** `check_goldens_clean.py`, `check_golden_baseline.py`, and `check_data_coverage.py` are first-class.

## Immediate Actions (do first)
1. [ ] **Inspect state**: `git status --short && git log -1 --oneline`
2. [ ] **Check integrity**: `SEED=42 make check` (or `bash scripts/check.sh`)
3. [ ] **If clean**: Proceed to user's next request. If mismatch → follow `AGENTS.md` recovery rules. Never re-pin baseline as a side effect of verification.
4. [ ] **Review ledger**: Skim `ledger/RESEARCH_LEDGER.md` for items relevant to the incoming task.
5. [ ] **Plan**: Read the specific experiment spec/task file if work targets a known E0xx.

## Verification Commands (reference)
```bash
SEED=42 make check                # fast convention+template (~seconds)
SEED=42 make verify-quick         # ~8 min
SEED=42 make verify-extended      # ~21 min (includes drift report)
SEED=42 make verify-full          # ~15 min (E042 n_sim=50 + sensitivity grid)
SEED=42 python3 run_all_verification.py --restore-only  # recover goldens if interrupted
```

## Guardrails
- **Never commit verification output.** If interrupted, restore goldens before committing.
- **Pre-registration is binding.** Goalposts never moved post-hoc. Sensitivity grids are reported, not gated.
- **No silent baseline changes.** Re-pinning requires explicit justification and updating `ledger/golden_baseline.json` via `scripts/check_golden_baseline.py --update`.
- **Offline first.** Network downloads are only allowed if data is missing and not enforced by coverage (but coverage will fail if unpinned).

## Success Criteria
- Baseline integrity passes all guards
- Any changes are minimal, justified, and verified
- No canonical `experiments/*.json` modified without ledger justification
- Clear summary of actions/state for continuity
