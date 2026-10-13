# Handoff: Ready for Maintainer CI Gate Creation

## What changed (this session)
- Added `scripts/check.sh` - fast verification wrapper (runs verify_convention_robustness + template validation)
- Added `scripts/validate_template.py` - validates workflow template content
- Added `.github/workflow-templates/verification-gate.yml` - copyable CI workflow template (cannot live in .github/workflows/ due to controller policy)
- Added `VERIFICATION_GATE_TEMPLATE.md` - explicit copy/paste instructions for maintainers
- Added `Makefile` with `check`, `verify`, `verify-full` targets

## What was actually verified
- Template validation passes: `python3 scripts/validate_template.py` → OK
- Convention robustness verification passes: `SEED=42 python3 verify_convention_robustness.py` → ALL VERIFICATIONS PASSED (E042 PARTIAL as recorded)
- Fast check passes: `SEED=42 bash scripts/check.sh` → OK
- `make check` passes
- No changes to core research code, experiments, data, goldens, or existing workflows

## What remains unresolved
- The actual `.github/workflows/verification-gate.yml` must still be created manually by a maintainer (or with elevated permissions allowing `workflows` scope). 
- Reason: Controller policy (`.github/scripts/kilo-controller.sh`) restores `.github/workflows/` from `WORKFLOW_BASE_SHA` and cleans it at session boundaries, preventing persistent agent-created workflow files. 
- GITHUB_TOKEN also lacks `workflows` permission to push workflow files.

## Which approaches have already failed and why
- Directly creating `.github/workflows/verification-gate.yml` is not persistent under the controller policy (by design).
- Using GITHUB_TOKEN to push workflow files fails due to missing `workflows` permission (repo/org constraint).

## One precise next task (evidence + constraints)
**For a maintainer with appropriate permissions:** Create `.github/workflows/verification-gate.yml` using the provided template.

Steps:
1. Copy content from `.github/workflow-templates/verification-gate.yml` (or `VERIFICATION_GATE_TEMPLATE.md`)
2. Create file `.github/workflows/verification-gate.yml` via GitHub UI (Settings → Actions → create file) or with a token that has `workflows` write scope
3. Commit to `main`
4. Verify CI runs green: `python run_all_verification.py --full` with `SEED=42`

Constraints:
- Do not modify core logic, experiments, goldens, or data
- Do not remove/alter controller scripts unless explicitly authorized
- Template and helpers are ready; no further research warranted

## Evidence
- Verification passes: `SEED=42 python3 run_all_verification.py --skip-slow` completed with ALL CHECKS PASSED
- Template validates cleanly
- Helpers tested end-to-end via check.sh
