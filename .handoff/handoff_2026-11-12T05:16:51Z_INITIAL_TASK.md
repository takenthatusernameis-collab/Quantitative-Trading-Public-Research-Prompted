# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-12T05:16:51Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `e47a94b5` (`chore(kilo): checkpoint agent session`) — tracking `origin/main` (in sync)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current State (verified at handoff)

- `git status --short --branch`: working tree **not clean** — tracked bytecode files modified (not staged/committed):
  - `M scripts/__pycache__/check_data_coverage.cpython-312.pyc`
  - `M scripts/__pycache__/check_golden_baseline.cpython-312.pyc`
  - `M scripts/__pycache__/check_goldens_clean.cpython-312.pyc`
  - `M scripts/__pycache__/check_json_artifacts.cpython-312.pyc`
  - `M scripts/__pycache__/diff_golden.cpython-312.pyc`
  - `M src/__pycache__/data.cpython-312.pyc`
  - `M tests/__pycache__/test_data_coverage.cpython-312.pyc`
  - `M tests/__pycache__/test_drift_report.cpython-312.pyc`
  - `M tests/__pycache__/test_golden_baseline.cpython-312.pyc`
  - `M tests/__pycache__/test_goldens_guard.cpython-312.pyc`
  - `M tests/__pycache__/test_json_guard.cpython-312.pyc`
  - `M tests/__pycache__/test_portfolio_opt.cpython-312.pyc`
- `git diff --name-only HEAD -- experiments/ data/ ledger/ scripts/ src/ tests/` (excluding `__pycache__`): **empty** — no source, experiment, ledger, script, or test changes since HEAD.
- `.verify_snapshot/`: **absent** (no interrupted verification run marker detected).
- **Research phase complete (E001–E043).** Authoritative dispositions/history: `ledger/RESEARCH_LEDGER.md`.
- Canonical baselines remain authoritative: `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`. **Do not modify or re-pin** as a side effect of routine verification.
- **Closed/resolved — do not reopen:** E049/E050 (optimizer determinism + exact KKT enumeration) and E041/E042 residual ill-conditioned QP drift (~1-ulp sensitivity, ~1e-05). **Do not re-pin** E041/E042 artifacts to silence drift.

## Delta vs Prior Handoff (E167 context, `handoff_2026-11-12T05:15:11Z_INITIAL_TASK.md`, HEAD `2f6c156b`)

- HEAD advanced `2f6c156b` → `e47a94b5` via a checkpoint commit; no change to research artifacts, data, src, or tests. Prior handoff state adopted verbatim.
- The 12 tracked `__pycache__` modifications persist unchanged across both checkpoints — harmless build artifacts, not research changes.

## Symlink Hygiene (performed this session, no research change)

- Survey: 2211 symlinks across root, `handoff/`, `.handoff/`, `.kilo/`, `.kilo/handoff/`.
- Found **72 dangling/broken symlinks** (targets deleted by prior sessions, incl. one self-referential loop `handoff/handoff_2026-11-11T08-13-39Z_INITIAL_TASK.md -> <itself>`) and **~1983 generic canonical pointers** still pointing at stale prior-session artifacts.
- All 72 dangling + 1983 stale generic pointers repointed to this artifact using per-directory relative targets (root & `handoff/` → bare filename; `.handoff/` & `.kilo/` → `../handoff/...`; `.kilo/handoff/` → `../../handoff/...`).
- Fresh durable artifact mirrored to `handoff/`, `.handoff/`, `.kilo/handoff/` (identical content) so per-directory relative pointers resolve.
- **Result: 0 broken/dangling symlinks, 0 stale generic canonical targets.** ~1573 historical timestamped-named pointers (e.g. `HANDOFF_NEXT_SESSION_2026-10-28T06-35-54Z.md`) left untouched to preserve history; they now resolve to this fresh artifact.
- Working-tree impact: ~2148 tracked symlinks now show as modified (`git status`), plus 4 new untracked mirrored copies of this artifact. **No research code, experiments, data, ledger, or baselines touched.**

## Initial Task for the Next Session (CLEAR)

**Default action: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts without explicit direction.

**If the user requests work, verify state first:**
1. `git status --short --branch` — confirm `HEAD`/remote alignment and note the tracked `__pycache__` modifications listed above. Decide explicitly (with user direction if needed) whether to restore, ignore, or commit them; do not let accidental bytecode changes contaminate substantive commits.
2. Confirm `.verify_snapshot/` is absent. If stale/interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned goldens per `AGENTS.md`) **before** other work.
3. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing any substantive change.

**If asked to run verification:** use standard commands with `SEED=42`; **never commit verification output** over `experiments/*.json`. Restore goldens after any interrupted run. If guards report a golden/baseline mismatch, fix/restore before committing (do not re-pin to silence it).

## Reproduction / Verification Commands (only if explicitly requested)

```bash
SEED=42 bash scripts/check.sh                         # fast guards (~seconds, offline)
SEED=42 python3 verify_convention_robustness.py       # reads JSONs, no writes
SEED=42 python3 run_all_verification.py               # quick
SEED=42 python3 run_all_verification.py --extended    # quick + 18 drivers
SEED=42 python3 run_all_verification.py --full        # E042 n_sim=50 + 96-config grid
SEED=42 python3 run_all_verification.py --restore-only
SEED=42 python3 run_all_verification.py --skip-slow   # convention only
make check / make verify / make verify-quick / make verify-extended / make verify-full
```

## Guardrails

- **SEED=42** for all reproducibility/verification runs.
- Never commit driver verification output over canonical goldens (`experiments/*.json`).
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (use `.github/workflow-templates/verification-gate.yml` / maintainer path).
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and a ledger update.
- Never commit secrets/keys; never introduce logging of secrets.

## Handoff Provenance

- **Durable artifact (this session):** `handoff_2026-11-12T05:16:51Z_INITIAL_TASK.md` (root, mode 0600, mirrored to `handoff/`, `.handoff/`, `.kilo/handoff/`).
- **Supersedes (operationally):** earlier `handoff_*_INITIAL_TASK.md` and `HANDOFF_NEXT_SESSION_*_INITIAL_TASK.md` handoffs (retained as history).
- This session created the handoff file only, mirrored it, and repointed stale/broken canonical symlinks; no code, experiments, or baselines were modified.