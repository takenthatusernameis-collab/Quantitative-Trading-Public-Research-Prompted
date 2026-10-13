# Handoff: CI gate created locally; full verification passes; awaiting maintainer persistence

## What changed (this session)
- **Created `.github/workflows/verification-gate.yml`** (CI gate workflow) — copied
  from the template at `.github/workflow-templates/verification-gate.yml`, YAML-validated.
  Committed locally as `12293a0`.
- **Aligned Python version** in the workflow, template, and instructions from
  `3.11` → `3.12` to match `requirements.txt` ("Verified… on Python 3.12.3").
  Committed locally as `f359af6`.
- **Created `AGENTS.md`** at repo root documenting all verification commands,
  conventions, and dependencies. This file was referenced in the Kilo environment
  config but did not previously exist. Committed locally as `ebb123f`.
- No changes to core research code, experiments, goldens, or data.

## What was actually verified
- `SEED=42 python3 run_all_verification.py --full` → **ALL CHECKS PASSED** (4/4):
  1. `verify_convention_robustness.py` — PASS (15 strategies asserted; E042 PARTIAL 4/5)
  2. `src/batch_run.py --universe large_liquid` — PASS (15/15 golden JSONs EXACT match)
  3. `src/validate.py --universe large_liquid` — PASS (validation_summary.json EXACT match)
  4. `experiments/run_e042.py --n-sim 50` — PASS (e042_minvar_market_neutral.json + e042_sensitivity_grid.json EXACT match)
- E042 result confirmed: OOS Sharpe 0.979 (PASS G1), β 0.094 (PASS G3), bear +1.967 (PASS G4), turnover 0.0043 (PASS G5); placebo z 2.11 (FAIL G2) → PARTIAL 4/5, not promoted. Market-neutral-total-portfolio line CLOSED (per v1.2.7).
- `python3 scripts/validate_template.py` → OK
- `python3 -c "import yaml; yaml.safe_load(...)"` on both workflow files → valid
- `SEED=42 bash scripts/check.sh` → OK
- `python3 -m py_compile` on all experiment drivers and src modules → clean

## What remains unresolved
- **The CI gate workflow commit (12293a0, f359af6) is local-only and will be reverted
  by the controller at the next CI checkpoint.** The controller
  (`.github/scripts/kilo-controller.sh`) runs
  `git restore --source="$WORKFLOW_BASE_SHA" -- .github/workflows` and
  `git clean -fd -- .github/workflows` before every checkpoint, and staging
  explicitly excludes `.github/workflows/**`.
- **GITHUB_TOKEN lacks the `workflows` permission**, so pushing the workflow file
  to GitHub is rejected with: "refusing to allow a GitHub App to create or update
  workflow `.github/workflows/verification-gate.yml` without `workflows` permission".
- The workflow has NOT been pushed to the remote and is NOT visible in GitHub Actions.

## Which approaches have already failed and why
- **Directly creating `.github/workflows/verification-gate.yml`** → cleaned by the
  controller at CI session checkpoints (by design).
- **Committing the workflow locally** → the commit persists locally but the
  controller reverts `.github/workflows/` to `WORKFLOW_BASE_SHA` at the next
  checkpoint, so the file is removed from the working tree and the commit is
  orphaned.
- **Pushing via GITHUB_TOKEN** → fails: "refusing to allow a GitHub App to
  create or update workflow… without `workflows` permission" (repo/org
  permission constraint).

## One precise next task (evidence + constraints)
**For a maintainer with repo admin access:**

1. Go to Settings → Actions → General → Workflow permissions → enable
   "Read and write workflows" (or use a PAT with `workflows` scope).
2. Create `.github/workflows/verification-gate.yml` via the GitHub UI
   (Add file → Create new file) using the content from
   `.github/workflow-templates/verification-gate.yml`.
3. Commit to `main`.
4. Verify CI runs green (Actions tab → "Verification Gate").

Constraints:
- Do not modify core research code, experiments, goldens, or data.
- Do not remove/alter the controller scripts unless explicitly authorized.
- Template, helpers, and AGENTS.md are ready; no further research warranted
  (research phase E001–E043 complete; market-neutral-total-portfolio line closed).

## Evidence
- Full verification: `SEED=42 python3 run_all_verification.py --full` →
  ALL CHECKS PASSED (4/4 steps, every golden JSON EXACT match).
- CI gate workflow: created, YAML-valid, committed locally (12293a0, f359af6).
- AGENTS.md: created, committed (ebb123f).
- All 15 experiment goldens reproduce EXACTLY under SEED=42 with cached data
  (vintage 2026-10-12 pinned in `data/vintages.json`).
