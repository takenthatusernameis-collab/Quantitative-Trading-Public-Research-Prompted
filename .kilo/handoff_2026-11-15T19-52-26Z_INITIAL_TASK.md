# Durable Handoff — Initial Task for Next Agentic Session

- **Timestamp (UTC):** 2026-11-15T19:52:26Z
- **HEAD:** `15e283e7d25abdc390cc7fe692787c3b3eb0c173` (`chore(kilo): checkpoint agent session`, main)
- **Remote sync:** `origin/main...HEAD = 0 0` (in sync)
- **Prior handoff superseded:** `handoff_2026-11-15T19-51-01Z_INITIAL_TASK.md` (retained for history)

## Repository state
- Research phase **complete/closed**: E001–E051. Ledger handoff refreshes recorded through **E392** prior to this session (see `ledger/RESEARCH_LEDGER.md`). No new research task is open.
- No interrupted verification run (`.verify_snapshot/` absent, `.verify_reports/` absent).
- Working tree before this deliverable: pre-existing modified `__pycache__/*.pyc` files under `scripts/`, `src/`, `tests/` (gitignored/build artifacts; **do not commit**). No research-source, experiment, data, golden, or ledger content changes since E392.

## Baseline integrity (re-verified this session, per-step isolation, no verification suite run)
All **exit 0**:
- `python3 scripts/check_json_artifacts.py` — 114 JSON artifacts parse OK
- `python3 scripts/check_goldens_clean.py` — committed golden artifacts match HEAD
- `python3 scripts/check_golden_baseline.py` — all 107 pinned golden artifacts match baseline fingerprint
- `python3 scripts/check_data_coverage.py` — all 35 pinned data inputs present, tracked, unchanged
- `python3 scripts/validate_template.py` — OK
- `python3 scripts/check_experiment_imports.py` — all experiment script imports/calls OK
- `python3 verify_convention_robustness.py` — all strategy blocks PASS

**Not run (sandbox dependency gap):** `pytest`/unit tests requiring `numpy`, `pandas`, `scipy`, `pytest` are unavailable in this environment; this is an environment constraint, not a repo regression. Install deps with `pip install -r requirements.txt` before running tests/verification.

## Known open items / caveats (do not “fix” without pre-registration)
- **E041/E042 grid artifacts**: residual 1-ulp optimizer sensitivity (ill-conditioned QP) causes numeric drift beyond tolerance in extended checks; structural/gate decisions unchanged. **Do not re-pin** these goldens to silence drift (see ledger E049 and open item).
- **Extended drift report**: `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json` is gitignored/reporting-only when produced by `--extended`.
- **CI workflow**: intended gate `.github/workflows/verification-gate.yml` cannot be created by automated agents here; maintainer must add via GitHub UI from `.github/workflow-templates/verification-gate.yml` (see `VERIFICATION_GATE_TEMPLATE.md`).
- **Golden restore note**: if a verification run is interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/` (and ensure HEAD matches intended pinned baseline before treating HEAD as authoritative).

## Reproduction / verification commands
```bash
pip install -r requirements.txt   # if deps missing
SEED=42 bash scripts/check.sh          # fast guards (recommended first)
SEED=42 python3 run_all_verification.py              # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended   # ~21 min
SEED=42 python3 run_all_verification.py --full       # ~15 min
SEED=42 python3 verify_convention_robustness.py
```

## Guardrails
- Always `SEED=42`. Never commit verification output or modify `experiments/*.json` goldens except an explicit, reviewed re-pin with `scripts/check_golden_baseline.py --update` (not for silencing drift).
- Do not move pre-registered goalposts, gates, or validated constructions post-hoc. Negative results stay recorded honestly.
- `__pycache__`, `.verify_snapshot/`, `.verify_reports/` are not research artifacts to commit.

## Clear initial task for next session
**No research action required.** The repository is in a clean, closed, guard-verified state.
1. If starting work, run `SEED=42 bash scripts/check.sh` (after installing deps) to confirm environment parity.
2. Only proceed with new work if the user provides an explicit, pre-registered research request or maintenance directive; otherwise report status and await instructions.
3. If asked to investigate reproducibility, prefer read-only checks first; do not re-run drivers or re-pin baselines unless explicitly directed and justified per ledger policy.
