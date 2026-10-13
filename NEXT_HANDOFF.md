# Handoff: Workflow template + verification helpers

## What changed
- Added `.github/workflow-templates/verification-gate.yml` (copyable workflow for maintainers; can't live in `.github/workflows/` due to controller reset policy)
- Added `VERIFICATION_GATE_TEMPLATE.md` with explicit copy/paste instructions
- Added `scripts/validate_template.py` to sanity-check the template

## What was actually verified
- Template validation helper passes (`python3 scripts/validate_template.py`)
- Convention robustness verification passes with cached data: `SEED=42 python3 verify_convention_robustness.py` → ALL VERIFICATIONS PASSED
- Python files compile cleanly
- No changes to core research code, experiments, data, or existing workflows

## What remains unresolved
- The actual `.github/workflows/verification-gate.yml` must still be created manually by a maintainer (or with elevated permissions allowing `workflows` scope). The controller's `git restore --source="$WORKFLOW_BASE_SHA" -- .github/workflows && git clean -fd -- .github/workflows` prevents persistent agent-created workflow files. Also GITHUB_TOKEN lacks `workflows` permission.
- Template content is documented; maintainer action still required as described in HANDOFF.md.

## Which approaches have already failed and why
- Directly creating `.github/workflows/verification-gate.yml` is not persistent under the controller policy; the file gets restored/cleaned at session boundaries. This is by design per controller script.
- Using GITHUB_TOKEN to push workflow files fails due to missing `workflows` permission. This is an org/repo permission constraint.

## One precise next task (evidence + constraints)
Create a small "dev check" wrapper that runs the fast verification path and optionally checks the template. For example:
- Add `scripts/check.sh` or `make check` that runs `SEED=42 python3 verify_convention_robustness.py` and `python3 scripts/validate_template.py`
- Keep it minimal, no new dependencies
- Verify: `bash scripts/check.sh` exits 0
- Constraint: do not modify `.github/workflows/*`, do not change core logic, do not regenerate experiment goldens

