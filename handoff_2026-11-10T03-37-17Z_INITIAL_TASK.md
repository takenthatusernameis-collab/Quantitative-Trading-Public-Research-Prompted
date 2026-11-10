# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-10T03:37:17Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD (at handoff creation):** `main` @ `756f1fa0c4ecfc89e4d4455a38f03f895fbf79f1` (`chore(kilo): checkpoint agent session`)
**Remote:** `origin/main` in sync (`## main...origin/main`)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Observed State

- **Research phase complete (E001–E043).** Authoritative dispositions/evidence: `ledger/RESEARCH_LEDGER.md`. Repository is in a closed, handoff-only state.
- **Canonical baselines authoritative:** `experiments/*.json` goldens, `ledger/golden_baseline.json`, `ledger/data_baseline.json`, pinned `data/` and `data/fundamentals/` snapshots/vintages. Do not modify or re-pin as a side effect of routine verification.
- **Closed — do not reopen:** E049/E050 and E041/E042 residual ill-conditioned QP drift. Do not re-pin E041/E042 to silence drift.
- **Git working tree (observed):** modified tracked `__pycache__` bytecode files only (`scripts/__pycache__/`, `src/__pycache__/`, `tests/__pycache__/`); no substantive changes observed in `experiments/`, `data/`, `ledger/`, source, or docs. `.verify_snapshot/` not present.
- **This session action:** created this durable timestamped handoff and repointed canonical handoff aliases. No experiment drivers, source, baselines, goldens, or research dispositions were changed.

## Initial Task for Next Session (CLEAR)

**Default action: WAIT for explicit user instructions.** Do not invent experiments, run verification unprompted, change gates/outcomes/dispositions, or modify golden/baseline artifacts without explicit direction.

### 1) Verify repository state first
```bash
git status --short --branch
git log -5 --oneline
ls -la .verify_snapshot 2>/dev/null || true
python3 -m pip install -r requirements.txt   # if deps missing
SEED=42 bash scripts/check.sh
```
- If golden mismatches are reported, restore/fix before committing. Never checkpoint verification output over canonical goldens.
- If a stale/interrupted verification snapshot exists: `SEED=42 python3 run_all_verification.py --restore-only`

### 2) If the user explicitly requests verification
```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 verify_convention_robustness.py
SEED=42 python3 run_all_verification.py              # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended   # if requested (~21 min)
SEED=42 python3 run_all_verification.py --full       # if requested (~15 min)
SEED=42 python3 run_all_verification.py --restore-only
```
Never commit verification output over `experiments/*.json`. If interrupted, restore goldens before committing.

### 3) If the user explicitly requests new work
- Keep changes minimal and scoped to the request.
- Preserve pre-registered gates/sensitivity/falsification discipline and multiple-testing rules (sensitivity grids reported, not gated; promotion requires a dedicated pre-registered confirmatory run + full placebo).
- Record negative results honestly in the ledger when applicable.
- Before committing substantive changes: `SEED=42 bash scripts/check.sh`.
- Do not re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction.
- Do not create `.github/workflows/` CI gates as an automated agent (template: `.github/workflow-templates/verification-gate.yml`; maintainer/UI only).

## Guardrails

- **SEED=42** for reproducibility/verification runs.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not re-pin E041/E042 or golden/data baselines to silence drift/output differences.
- Do not change pre-registered gates, outcomes, or dispositions without explicit justification and a ledger update.
- Historical timestamped handoff files are retained; canonical `handoff_*`/`*handoff*`/`initial_task*`/`next_session*` aliases should point to this artifact.

## Handoff Provenance

- **Supersedes (operationally):** `handoff_2026-11-10T03-36-11Z_INITIAL_TASK.md` and earlier timestamped handoffs (retained as history).
- **Durable artifact:** `handoff_2026-11-10T03-37-17Z_INITIAL_TASK.md`
