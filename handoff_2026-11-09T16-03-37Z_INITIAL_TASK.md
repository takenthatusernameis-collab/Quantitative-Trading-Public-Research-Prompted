# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-09T16:03:37Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `367f78a56b5c98b21ae81d7be5b1dbd782a559c3` — `chore(kilo): checkpoint agent session` (verify with `git log -1 --oneline`)
**Remote:** `origin/main` (in sync at handoff creation; verify with `git status -sb`)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current State (read before acting)

- **Research phase complete (E001–E043).** Authoritative dispositions/evidence: `ledger/RESEARCH_LEDGER.md`. Repository is in a **closed, handoff-only state** with **no open research items**.
- **`.verify_snapshot/`: absent** — no interrupted verification recovery pending.
- **Working tree clean.** `git status --short --branch` → `## main...origin/main`, no staged/unstaged tracked changes. `git diff --name-only HEAD -- experiments/ data/ ledger/ scripts/ src/ tests/` → empty. `git ls-files experiments/` → 138 tracked golden artifacts, all matching HEAD.
- **Canonical baselines are authoritative:** `experiments/*.json` goldens (138 tracked, all matching HEAD), `ledger/golden_baseline.json`, `ledger/data_baseline.json`, and pinned `data/` / `data/fundamentals/` snapshots/vintages. **Do not modify or re-pin as a side effect of routine verification.**
- **Closed — do not reopen:** E049/E050; E041/E042 residual ill-conditioned QP drift. **Do not re-pin E041/E042 or golden/data baselines to silence drift/output differences.**

## Initial Task for Next Session (CLEAR)

**Default action: WAIT for explicit user instructions.**
Do not invent experiments, run verification unprompted, change gates/outcomes/dispositions, or modify golden/baseline artifacts without explicit direction.

### 1) Verify repository state first
```bash
git status --short --branch
git log -5 --oneline
ls -la .verify_snapshot 2>/dev/null || echo ".verify_snapshot absent"
SEED=42 bash scripts/check.sh
```
- If golden mismatches are reported, **restore/fix before committing**. Never checkpoint verification output over canonical goldens.
- If a stale/interrupted verification snapshot exists:
  ```bash
  SEED=42 python3 run_all_verification.py --restore-only
  ```

### 2) If the user explicitly requests verification
```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 verify_convention_robustness.py
SEED=42 python3 run_all_verification.py              # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended   # if requested (~21 min)
SEED=42 python3 run_all_verification.py --full       # if requested (~15 min)
SEED=42 python3 run_all_verification.py --restore-only  # if interrupted / restore needed
```
**Never commit verification output** over `experiments/*.json`. If interrupted, restore goldens before committing.

### 3) If the user explicitly requests new work
- Keep changes minimal and scoped to the request.
- Preserve pre-registered gates/sensitivity/falsification discipline and multiple-testing rules (sensitivity grids are reported, not gated; promotion requires a dedicated pre-registered confirmatory run + full placebo).
- Record negative results honestly in `ledger/RESEARCH_LEDGER.md` when applicable.
- Before committing substantive changes: `SEED=42 bash scripts/check.sh`.
- Do not re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction.
- Do not create `.github/workflows/` CI gates as an automated agent (template: `.github/workflow-templates/verification-gate.yml`; maintainer/UI only).

## Guardrails

- **SEED=42** for reproducibility/verification runs.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not re-pin E041/E042 or golden/data baselines to silence drift/output differences.
- Do not change pre-registered gates, outcomes, or dispositions without explicit justification and a ledger update.
- Do not stage/commit `__pycache__` or incidental bytecode changes.
- Historical timestamped handoff files are retained as history.

## Handoff Provenance

- **Durable artifact:** `handoff_2026-11-09T16-03-37Z_INITIAL_TASK.md`
- **Delta vs prior durable handoff (E121, HEAD a4bc5c5f):** HEAD advanced `a4bc5c5f` → `367f78a5` via 11 checkpoint commits (`chore(kilo): checkpoint agent session`); only the handoff symlink tree changed between them. Prior closed/conformance state adopted. `git diff --name-only HEAD -- experiments/ data/ ledger/ scripts/ src/ tests/` → empty; no research artifacts, baselines, source, tests, scripts, or ledger substance changed. `.verify_snapshot/` absent.
- **Supersedes (operationally):** prior timestamped handoffs (retained as history), including `handoff_2026-11-09T15-59-28Z_INITIAL_TASK.md`, `handoff_2026-11-09T15-58-02Z_INITIAL_TASK.md`, `handoff_2026-11-09T15-56-45Z_INITIAL_TASK.md`, `handoff_2026-11-09T15-55-53Z_INITIAL_TASK.md`, `handoff_2026-11-09T15-54-16Z_INITIAL_TASK.md`, `handoff_2026-11-09T15-32-10Z_INITIAL_TASK.md`, and `handoff_2026-11-09T15-27-34Z_INITIAL_TASK.md`.