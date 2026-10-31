# Durable Handoff — Next Agentic Work Session

**Timestamp:** $(date -u +%Y-%m-%dT%H:%M:%SZ)
**Branch:** $(git branch --show-current 2>&1 | tail -1)
**HEAD:** $(git log -1 --format='%h %s' 2>&1 | tail -1)
**Working tree:** $(git status --short 2>&1 | grep -v __pycache__ | wc -l | xargs echo) tracked changes ($(git status --short 2>&1 | grep -v __pycache__ | head -c 80))
**Verification snapshot:** none active (`.verify_snapshot/` absent)

---

## INITIAL TASK (do first)

**Confirm baseline integrity before making any changes or running verification.**

1. Run `SEED=42 bash scripts/check.sh` — expect exit 0. This runs py_compile, tests (including `tests/test_portfolio_opt.py`), data coverage, golden-clean, golden-baseline checks.
2. If `check_goldens_clean.py` or `check_golden_baseline.py` fail on tracked artifacts under `experiments/` due to HEAD drift, DO NOT re-pin. The pinned baseline in `ledger/golden_baseline.json` is authoritative. If needed, restore specific files from the commit whose SHA-256 matches the ledger (`git checkout <commit> -- experiments/<file>`).
3. After green checks, report status and await explicit user direction. Do **not** modify goldens, re-pin baselines, run `--extended`/`--full` verification, or change gate logic without explicit instruction.

---

## Current state

- **Research phase complete** (E001–E043). Market-neutral-total-portfolio line is CLOSED (E042 PARTIAL 4/5, E042b REJECTED 4/5). All surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- **Portfolio optimizer (E049)**: `src/portfolio_opt.py` has exact active-set KKT solver wired as primary path for `max_sharpe` and `min_var`; SLSQP fallback only. Feasibility judged on problem constraints (not solver exit status). Pinned by `tests/test_portfolio_opt.py`.
- **Canonical artifacts**: `experiments/*.json` are goldens; SHA-256 pinned in `ledger/golden_baseline.json`. Data caches pinned per `ledger/data_baseline.json` and fundamentals in `data/fundamentals_vintages.json`.
- **Working tree**: clean (no unintended tracked changes). No verification snapshot active.

## Known pre-existing drift (reporting-only, decisions unchanged)

- **E041**: ~133 numeric diffs (1-ulp sensitivity of an ill-conditioned QP). Structural differences gone. **Do not re-pin.**
- **E042 lead artifacts**: sensitivity grids show similar 1-ulp sensitivity (29-133 numeric diffs). **Do not re-pin.**
- **E030**: numeric diffs on near-zero quantities (documented; inputs now pinned). **Do not re-pin.**
- **E029**: fundamentals pinned for offline reproducibility; golden deliberately re-pinned. **Do not "fix" by re-running.**

## Constraints (must follow)

- Always use `SEED=42`.
- Honor pinned cache vintages (`data/vintages.json`, `data/fundamentals_vintages.json`).
- Never leave a verification run half-finished (suite backs up/restores `experiments/*.json` via `.verify_snapshot/` with `ACTIVE.json`). If interrupted: `SEED=42 python3 run_all_verification.py --restore-only`.
- Do **not** commit verification outputs; only intentional source/data changes.
- Do **not** move goalposts, change tolerances/drivers/skips, or change research decisions as a side effect of verification.
- Replacing an artifact requires deliberate `python3 scripts/check_golden_baseline.py --update` (visible in diff). Never re-pin as side effect of running verification.
- Run `python3 -m py_compile` on any modified files; no separate linter configured.
- Offline mode enforced by verification (`QUANT_RESEARCH_OFFLINE=1`); unpinned inputs fail hard.
- Do **not** change `src/backtest.py`, `src/strategies.py`, `src/futures.py`, `src/macro.py`, `src/portfolio_opt.py` gate logic, sensitivity grids, or pre-registered outcomes without explicit instruction.
- CI workflow creation is maintainer-gated (template at `.github/workflow-templates/verification-gate.yml`, instructions in `VERIFICATION_GATE_TEMPLATE.md`).
