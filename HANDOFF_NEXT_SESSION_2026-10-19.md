# Session Handoff: E022 placebo-z vintage drift disposition recorded

## What changed (this session)
- **`ledger/RESEARCH_LEDGER.md`** — Added explicit "Placebo z-score vintage drift (verification)" note under E022's Data integrity section documenting the regenerated placebo values (mean -0.136, std 0.296, z 1.909) vs committed (mean -0.187, std 0.308, z 2.00), attributed to FRED 2026-10-12 cache vintage and 5-core-theme restriction affecting RNG sequencing. Also clarified the discretion line noting the golden is retained and goalposts/tolerances were not weakened.
- Verified Python files compile (`experiments/run_e022.py`, `run_all_verification.py`).

## What was actually verified (evidence)
- `SEED=42 python3 verify_convention_robustness.py` → **ALL VERIFICATIONS PASSED** (107/107 artifacts, all strategy checks pass; E042 remains PARTIAL as recorded due to placebo gate).
- `SEED=42 bash scripts/check.sh` → **All checks passed** (golden integrity guard, imports, etc.).
- `experiments/e022_macro_momentum.json` confirmed in clean git state (no diffs) with placebo values matching the regenerated state from prior fix (z=1.909). The committed golden artifact remains unchanged.

## What remains unresolved
- Extended verification (`run_all_verification.py --extended`) has 3 failures documented as pre-existing environmental drift (per prior handoffs):
  1. **E022**: placebo block fields differ beyond `numeric_tol=1e-4` (documented vintage drift; accepted)
  2. **E030**: numeric drift (all < ~3e-3), no structural changes — pre-existing FRED/cache/vintage drift
  3. **E041**: structural + numeric drift (e.g. `n_market_neutral_and_sharpe_gte_0.8: 8->7` in some cases) — pre-existing
- CI workflow `.github/workflows/verification-gate.yml` still requires maintainer creation via GitHub UI (template exists). This is a repo/process constraint, not a code issue.

## Which approaches have already failed and why
- Attempting to "fix" vintage drift by regenerating the E022 golden would change a committed result (placebo z 2.00→1.909) — forbidden without pre-registered confirmatory run + placebo; correctly rejected.
- Weakening tolerances was considered and rejected; structural match is preserved.

## One precise next task
Investigate E030 and E041 extended-verification drift with minimal scope. For each, extract the exact field-level diffs vs committed goldens (focus on structural keys first, then numeric beyond tolerance), determine if drift is purely numeric (FP/cache/vintage) or structural, and produce a concrete recommendation (accept as documented drift with evidence, or identify a minimal fix that does not alter promotion gates/committed results). Do not regenerate goldens or weaken global tolerances unless a specific, evidence-based justification is written to the ledger. Target: bounded 15-30 min analysis producing a written recommendation in next handoff.
