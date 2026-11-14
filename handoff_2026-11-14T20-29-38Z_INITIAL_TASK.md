# Initial Task (for next agentic work session) — 2026-11-14T20:29:38Z (UTC)

## Context (read first)
- Repo: Quantitative-Trading-Public-Research-Prompted (independent reproducible quant research, 2014–2026 US equities/futures/macro). Research phase is **complete (E001–E051)**; surviving validated strategies are summarized in `ledger/RESEARCH_LEDGER.md`.
- Canonical guidance: `AGENTS.md` (commands, reproducibility rules, golden baseline integrity, CI/template notes).
- Key docs: `ledger/RESEARCH_LEDGER.md`, `VERIFICATION_GATE_TEMPLATE.md`, `.github/workflow-templates/verification-gate.yml`, `run_all_verification.py`, `scripts/check.sh`.

## Golden / verification integrity (do NOT skip)
- `experiments/*.json` are canonical artifacts. Verification scripts may overwrite them while running and must restore afterward. **Never leave a verification run half-finished.**
- Before making changes or committing: run `python3 scripts/check_goldens_clean.py` (also part of `scripts/check.sh`). If it reports a mismatch, restore first:
  - Preferred: `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/` if appropriate).
  - If HEAD already contains a wrong captured baseline, restore the pinned file from the correct commit per `AGENTS.md` guidance (compare vs `ledger/golden_baseline.json`).
- Do **not** re-pin `ledger/golden_baseline.json` as a side effect of a routine run. Any baseline change requires an explicit, reviewed re-pin (`python3 scripts/check_golden_baseline.py --update`) and should be rare.
- Data/cache integrity: offline drivers are enforced via `QUANT_RESEARCH_OFFLINE=1` in the suite; cache coverage is checked by `scripts/check_data_coverage.py` / `ledger/data_baseline.json` rules in `AGENTS.md`.

## Recommended first commands (safe, fast)
```bash
SEED=42 bash scripts/check.sh
# or: make check
```
If you need broader confidence:
```bash
SEED=42 python3 run_all_verification.py --quick
# or: make verify-quick
```
Extended/full: only if necessary and you understand runtimes (~21m / ~15m+ behaviors described in `AGENTS.md`).

## Suggested next-session goals (pick one clear objective)
1. **Hygiene/CI enablement** (maintainer action): create the real workflow from `.github/workflow-templates/verification-gate.yml` into `.github/workflows/verification-gate.yml` via GitHub UI (repo token/workflow restrictions prevent agents from doing it). Verify `make check` locally first.
2. **Docs/ledger consistency pass**: scan `ledger/RESEARCH_LEDGER.md` and top-level docs for stale claims vs current repo state (especially any mentions of half-finished verification incidents) and propose minimal edits (do not alter golden artifacts).
3. **Targeted code/doc TODOs**: only if the user gives a specific task; otherwise avoid exploratory refactors. Prefer running `scripts/check.sh` before and after any change.
4. **If investigating a reported regression**: reproduce with `SEED=42`, capture exact commands/output, and fix without touching `experiments/*.json` goldens unless the change is an intentional, pre-approved baseline update (with re-pin + justification).

## Guardrails
- Do not commit generated verification outputs as goldens accidentally.
- Do not run long verification suites unless the user asked or you need them to validate a specific change.
- Prefer small, reviewable diffs. If unsure about baseline changes, stop and document findings instead of re-pinning.

---

## Durable artifact

Primary: `.handoff/2026-11-14T20-29-38Z_INITIAL_TASK.md`. Mirror: this file at repo root `handoff_2026-11-14T20-29-38Z_INITIAL_TASK.md`.

Supersedes previous INITIAL_TASK handoffs. Written by agent at 2026-11-14T20:29:38Z.
