# Verification Gate Workflow Template

This file contains the workflow content suggested in `HANDOFF.md` for the verification gate.

## Rationale

The controller (`.github/scripts/kilo-controller.sh`) restores tracked workflows to `WORKFLOW_BASE_SHA` and cleans `.github/workflows` at session boundaries, preventing agents from creating persistent workflow files. Also the repo-scoped `GITHUB_TOKEN` cannot grant `workflows` permission.

## Usage (for maintainer)

Create `.github/workflows/verification-gate.yml` via GitHub UI with the following content:

```yaml
name: Verification Gate

on:
  push:
    branches: [main]
    paths:
      - 'src/**'
      - 'experiments/**'
      - 'run_all_verification.py'
      - 'verify_convention_robustness.py'
      - 'requirements.txt'
  pull_request:
    branches: [main]
    paths:
      - 'src/**'
      - 'experiments/**'
      - 'run_all_verification.py'
      - 'verify_convention_robustness.py'
      - 'requirements.txt'

jobs:
  verification-gate:
    runs-on: ubuntu-latest
    env:
      SEED: 42
    steps:
      - uses: actions/checkout@v4
      - name: Set up Python
        uses: actions/setup-python@v5
        with:
          python-version: '3.11'
      - name: Install dependencies
        run: |
          python -m pip install --upgrade pip
          pip install -r requirements.txt
      - name: Run verification
        run: python run_all_verification.py --full
```

See also: `.github/workflow-templates/verification-gate.yml`
