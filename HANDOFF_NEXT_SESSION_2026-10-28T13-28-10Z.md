# HANDOFF: Next Agentic Work Session

**Timestamp:** 2026-10-28T13:28:10Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** see git status
**State:** Research phase complete (E001–E043). Surviving strategies documented in `ledger/RESEARCH_LEDGER.md`.

## INITIAL TASK (CLEAR)
**Objective:** Establish a clean baseline and pick up the highest-priority actionable item from the research ledger.

## IMMEDIATE ACTIONS (do in order)
1. **Verify repo integrity**
   `SEED=42 bash scripts/check.sh`
   (checks goldens clean vs HEAD, golden baseline pin, data coverage, py_compile, tests). If it reports a golden mismatch, do **not** commit — restore first.
2. **Restore if needed**
   If verification left artifacts modified, run `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/` as a last resort). Ensure no stale `.verify_snapshot/ACTIVE.json`.
3. **Read the ledger**
   Read `ledger/RESEARCH_LEDGER.md` top-to-bottom. Identify the highest-priority open item (look for "OPEN", "IN PROGRESS", or items marked as next). Follow its exact gates/falsification expectations.
4. **Execute next step**
   Only act on what the ledger specifies. Do not re-run full verification unless explicitly requested by the ledger item. Respect baseline integrity rules in `AGENTS.md`.

## CONSTRAINTS / NOTES
- **Goldens are authoritative:** `experiments/*.json` committed are the record. Never re-pin to silence numeric drift from ill-conditioned solvers (see E049). Use `scripts/check_golden_baseline.py --update` only if explicitly changing the baseline with justification.
- **Offline-first:** Many drivers use pinned caches/vintages/fundamentals. `QUANT_RESEARCH_OFFLINE=1` is used by verification; missing cache entries fail hard.
- **Determinism:** Always use `SEED=42`. Follow pre-registration/multiple-testing discipline.
- **No half-finished verification:** If starting verification, ensure snapshot backup exists or use `--restore-only`. Check `scripts/check_goldens_clean.py` first.

## ARTIFACTS TO CHECK
- `ledger/RESEARCH_LEDGER.md` (source of truth for next work)
- `AGENTS.md` (commands, baseline integrity, reproducibility)
- `ledger/golden_baseline.json`, `ledger/data_baseline.json`
- `.verify_snapshot/` (should not have ACTIVE.json if clean)

**End of handoff. Proceed with step 1.**
