# Handoff: Next Agentic Session — Timestamped Initial Task

**Timestamp (UTC): 2026:10:28T12:21:34ZZ
**Branch:** main
**HEAD: 429f7ad (current)
**Durable handoff:** this file; `HANDOFF_CURRENT.md` and `HANDOFF_NEXT_SESSION.md` symlink here.
**Working tree:** clean of tracked changes — only `scripts/__pycache__/*.pyc`, `src/__pycache__/*.pyc`, `tests/__pycache__/*.pyc` (all gitignored). No `.verify_snapshot/` / `ACTIVE.json` — no interrupted verification run.

## Initial task (do this first)

Verify baseline integrity before making any changes. This repo is post-research (E001–E043 complete); no new research is warranted unless explicitly requested.

```bash
git status --short
echo "---"
SEED=42 bash scripts/check.sh
```

**Success criteria:** `scripts/check.sh` exits 0 ("ALL CHECKS PASSED", "=== All checks passed ==="); `git status --short` shows only `__pycache__/*.pyc`.

## Verification commands (quick reference)

- Fast check: `SEED=42 bash scripts/check.sh` (or `make check`)
- Quick verify (~8 min): `SEED=42 python3 run_all_verification.py` (`make verify-quick`)
- Extended (~21 min): `SEED=42 python3 run_all_verification.py --extended` (`make verify-extended`)
- Full (~15 min): `SEED=42 python3 run_all_verification.py --full` (`make verify-full`)
- Restore goldens if interrupted: `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`)
- Convention robustness: `SEED=42 python3 verify_convention_robustness.py` (`make verify`)

## Guards in place (all passing as of this handoff)

- `scripts/check_goldens_clean.py` — working tree vs HEAD under `experiments/`
- `scripts/check_golden_baseline.py` — tracked artifacts vs SHA-256 pinned in `ledger/golden_baseline.json`
- `scripts/check_data_coverage.py` — every `data.download()` call site resolves to a committed, pinned cache file (`ledger/data_baseline.json`)
- `tests/test_portfolio_opt.py` — optimizer determinism (validates constraints, not solver exit status)
- Experiment-script imports + template validation

## Known pre-existing drift (reporting-only; do NOT re-pin)

- **E041:** ~133 numeric diffs from 1-ulp sensitivity of an ill-conditioned tangency QP (optimizer determinism fixed per ledger E049). Structural differences gone. Do not re-pin.
- **E030:** numeric diffs on near-zero quantities. Do not re-pin.
- **E029/E030 inputs:** pinned for offline reproducibility (`data/fundamentals/`, `data/vintages.json`); goldens deliberately re-pinned. Do not "fix" by re-running.

## Constraints

- Always use `SEED=42`. Cost model: tc=0.5bps + slippage=0.2bps, next-day open execution.
- Never modify `experiments/*.json` as a side effect of verification; the suite backs up and restores them. Never leave a run half-finished.
- Do not commit verification outputs; only intentional source/data changes.
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or validated constructions (`src/backtest.py`, `src/strategies.py`, `src/futures.py`, `src/macro.py`, `src/portfolio_opt.py`).
- If adding data inputs, commit the file and re-pin with `python3 scripts/check_data_coverage.py --update`.
- CI workflow creation is maintainer-gated; template at `.github/workflow-templates/verification-gate.yml`, instructions in `VERIFICATION_GATE_TEMPLATE.md`.
- Ignore `__pycache__/*.pyc` — do not commit.

## Context to review if needed

- `ledger/RESEARCH_LEDGER.md` — validated strategies (E001–E043) and open items
- `AGENTS.md` — full project conventions and verification semantics
- Prior handoffs for continuity: `HANDOFF_NEXT.md`, `HANDOFF.md`, `HANDOFF_SESSION_*.md`