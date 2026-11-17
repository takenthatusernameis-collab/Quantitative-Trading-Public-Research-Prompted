# Agentic Work Session Handoff

**Timestamp (UTC)**: 2026-11-17T06:16:47Z
**Handoff ID**: E440 (durable handoff refresh)
**Project**: Quantitative-Trading-Public-Research-Prompted
**Working directory**: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Git state**: `778b33c2` on `main` (clean working tree at handoff time; HEAD == origin/main, in sync 0/0)

## Delta vs prior durable handoff
- Prior: `handoff_2026-11-17T06:15:41Z_INITIAL_TASK.md` (E439, HEAD `35faf58e`)
- Two checkpoint commits since: `f34a7261`, `778b33c2` — checkpoint/handoff bookkeeping only.
- `git diff --stat 35faf58e..HEAD -- experiments data src scripts tests research_state` is empty: **no changes** to code, data, tests, or research state.

## Project status
- Research phase complete (E001–E051). Validated surviving strategies are documented in `ledger/RESEARCH_LEDGER.md`.
- `experiments/*.json` are canonical golden artifacts. Verification runs overwrite them during execution and must restore them afterward.
- No interrupted verification run: `.verify_snapshot/` and `.verify_reports/` are absent.
- Previous handoff (`handoff_2026-11-17T06:15:41Z_INITIAL_TASK.md`, E439) superseded — no new research work was performed since.

## Immediate checks (recommended first)
```bash
# Fast, offline: golden/coverage/baseline guards + convention checks (~seconds)
SEED=42 bash scripts/check.sh

# Quick verification (~8 min): 8 core drivers + batch_run + validate + E042 n_sim=2
SEED=42 python3 run_all_verification.py
```

Other verification modes:
```bash
SEED=42 python3 run_all_verification.py --extended   # +18 committed drivers, structural compare (~21 min)
SEED=42 python3 run_all_verification.py --full       # E042 n_sim=50 + 96-config grid (~15 min)
SEED=42 python3 run_all_verification.py --skip-slow  # convention-only
```

## Critical invariants / gotchas
- **Never commit verification output.** If a run is interrupted, recover goldens before committing:
  - `SEED=42 python3 run_all_verification.py --restore-only` (preferred) or `git checkout -- experiments/`
  - `scripts/check.sh` / `check_goldens_clean.py` will flag dirty artifacts or a stale `.verify_snapshot/`.
- **Golden baseline pinning**: `ledger/golden_baseline.json` is the SHA-256 authority; changing a golden requires deliberate re-pin (`python3 scripts/check_golden_baseline.py --update`) — never as a side effect of verification.
- **Data inputs are pinned**: `data/vintages.json`, `data/fundamentals_vintages.json`, and `ledger/data_baseline.json`. Verification runs drivers with `QUANT_RESEARCH_OFFLINE=1`; missing/unpinned cache fails hard.
- **Reproducibility**: always set `SEED=42`. Drivers are compared to committed goldens (see AGENTS.md for tolerances/drift notes).
- **Known drift**: E041 has residual numeric drift (ill-conditioned QP, 1-ulp sensitivity; see ledger E049) — do **not** re-pin E041/E042 grid artifacts to silence it. Optimizer validation now checks problem constraints, not solver exit status (E049).
- **CI gate**: workflow template is `.github/workflow-templates/verification-gate.yml`; actual `.github/workflows/verification-gate.yml` must be created manually by a maintainer (agent/controller limitations).

## Suggested next tasks (pick one, pre-register if research)
1. **Baseline health**: run `SEED=42 bash scripts/check.sh` (and optionally `--skip-slow`/quick verify) to confirm a clean, reproducible state.
2. **E049 follow-up (engineering)**: investigate bounded/deterministic handling for the ill-conditioned tangency/min-var QP so E041/E042-grid reproduce without re-pinning (requires careful, pre-registered/justified change; do not move goalposts).
3. **CI enablement (manual)**: if you have maintainer access, instantiate `.github/workflow-templates/verification-gate.yml` as a real workflow via the GitHub UI.

## Clear Initial Task for Next Agentic Work Session
**Refresh the durable handoff for the next agentic work session.**
1. Capture live state: `date -u`, `git rev-parse HEAD`, `git rev-parse origin/main`, `git rev-list --left-right --count origin/main...HEAD`, `git status --short --branch`; confirm no `.verify_snapshot/`/`.verify_reports/` interruption.
2. Delta working tree/HEAD against this handoff (`handoff_2026-11-17T06:16:47Z_INITIAL_TASK.md`, HEAD `778b33c2`); explicitly note any changes to `experiments/`, `data/`, `src/`, `scripts/`, `tests/`, or `research_state/`.
3. Write a fresh timestamped `handoff_<ISO>Z_INITIAL_TASK.md` at repo root and mirror identically to `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/`.
4. Run `python3 scripts/repoint_handoff.py handoff_<ISO>Z_INITIAL_TASK.md` to repoint generic canonical pointers (expect ~452 pointers, 0 bad in this layout unless structure changed).
5. Append/update ledger entry as appropriate for the handoff refresh; keep all guardrails intact.
6. Do not commit unless explicitly directed.

## Key references
- `AGENTS.md` — commands, invariants, baseline integrity, drift notes
- `ledger/RESEARCH_LEDGER.md` — experiment dispositions and E045/E048/E049 notes
- `README.md`, `REPRODUCE.md` — reproduction guide

*Clear initial handoff for the next agentic work session.*