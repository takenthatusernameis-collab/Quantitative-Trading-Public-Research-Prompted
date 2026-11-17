# Agentic Work Session Handoff

**Timestamp (UTC):** 2026-11-17T05:21:23Z
**Handoff ID:** durable initial task (next agentic session)
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** `main` @ `95bc9118` (clean working tree; in sync with `origin/main`)

## Project status
- Independent reproducible quant-strategy research on 2014–2026 US equities/futures/macro. **Research phase complete (E001–E051).**
- Surviving/validated strategies and dispositions: `ledger/RESEARCH_LEDGER.md`.
- Canonical golden artifacts: `experiments/*.json` (pinned; verification must never be left half-finished).
- No interrupted verification state observed at handoff (`.verify_snapshot/` and `.verify_reports/` absent).

## Delta since prior durable handoff
- Prior handoff: `handoff_2026-11-17T05:20:42Z_INITIAL_TASK.md` (HEAD `7126f8ab`).
- Change since: one checkpoint commit (`95bc9118`, `chore(kilo): checkpoint agent session`). No changes to `experiments/`, `data/`, `src/`, `scripts/`, `tests/`, or `research_state/`.

## Immediate first steps (recommended)
```bash
# 1) Fast, offline integrity + convention checks (~seconds)
SEED=42 bash scripts/check.sh

# 2) Quick verification if deeper confidence needed (~8 min)
SEED=42 python3 run_all_verification.py

# Optional modes:
# SEED=42 python3 run_all_verification.py --extended   # +18 drivers, structural compare (~21 min)
# SEED=42 python3 run_all_verification.py --full       # E042 n_sim=50 + 96-config grid (~15 min)
# SEED=42 python3 run_all_verification.py --skip-slow  # convention-only
```

## Critical invariants (do not violate)
- **Golden artifacts:** never commit verification output. If a run is interrupted/killed, recover before committing:
  - `SEED=42 python3 run_all_verification.py --restore-only` (preferred) or `git checkout -- experiments/`
  - `scripts/check.sh` / `scripts/check_goldens_clean.py` fail on dirty goldens or stale `.verify_snapshot/`.
- **Baseline pinning:** `ledger/golden_baseline.json` is the SHA-256 authority. Changing a golden requires deliberate re-pin via `python3 scripts/check_golden_baseline.py --update` (never as a side effect of verification).
- **Data pinning/offline:** `data/vintages.json`, `data/fundamentals_vintages.json`, `ledger/data_baseline.json`. Verification runs drivers with `QUANT_RESEARCH_OFFLINE=1`; missing/unpinned inputs fail hard.
- **Reproducibility:** always use `SEED=42`. See `AGENTS.md` for driver coverage, tolerances, and known drift notes.
- **Known drift (do not "fix" by re-pinning):** E041 has residual numeric drift from an ill-conditioned QP (1-ulp sensitivity; ledger E049). E041/E042 grid artifacts must not be re-pinned to silence this. Optimizer validation checks problem constraints, not solver exit status (E049).
- **CI gate:** workflow template at `.github/workflow-templates/verification-gate.yml`; actual `.github/workflows/verification-gate.yml` must be created manually by a maintainer (agent/controller/token limitations).

## Suggested next tasks (pick one; pre-register if research)
1. **Baseline health:** run `SEED=42 bash scripts/check.sh` (and quick verify if warranted) to confirm clean, reproducible state from this HEAD.
2. **E049 follow-up (engineering, careful):** investigate a bounded/deterministic treatment for the ill-conditioned tangency/min-var QP so E041/E042-grid reproduce without re-pinning. Requires pre-registration/clear justification; do not move goalposts or re-pin to hide drift.
3. **CI enablement (manual, maintainer-only):** instantiate `.github/workflow-templates/verification-gate.yml` as `.github/workflows/verification-gate.yml` via GitHub UI.

## Key references
- `AGENTS.md` — commands, integrity guards, coverage, drift/invariant details
- `ledger/RESEARCH_LEDGER.md` — experiment dispositions (E001–E051), E045/E048/E049 notes
- `README.md`, `REPRODUCE.md` — reproduction and project overview
- Prior handoff: `handoff_2026-11-17T05:20:42Z_INITIAL_TASK.md`

## Initial task for next session
**CLEAR INITIAL TASK:** Confirm baseline health (`SEED=42 bash scripts/check.sh`), then act only on explicit user instruction. Do not re-run verification, modify experiments, or change baselines without direction. The baseline is clean and recoverable. Do **not** invent new tasks, re-run verification "just to be sure", create additional handoffs unprompted, or re-open closed items (E049/E050 optimizer determinism; E041/E042 ill-conditioned QP drift).

*Durable, timestamped initial handoff for the next agentic work session. No research/code changes made in this handoff step.*
