# HANDOFF — Timestamped initial task for next agentic session

Timestamp (UTC): 2026-10-28T10:30:06Z
Written by: kilo (kilo-auto/free), session end
Repo: Quantitative-Trading-Public-Research-Prompted
Branch: main
HEAD: bb88646 (chore(kilo): checkpoint agent session)
Working tree: clean of tracked changes except `__pycache__/*.pyc` (gitignored — ignore). Verified with `git status --short`.
Verify snapshot: none active (`.verify_snapshot/` absent, no `ACTIVE.json`). No interrupted run to recover.

## Mission for next session

Start here and verify baseline integrity before making any changes. This repo is in **post-research state (E001–E043 complete)** with strict baseline/verification guards. **No new research is warranted unless explicitly requested.** The durable pointer is this file (`HANDOFF_NEXT.md` is updated to point here).

## Current known state (verified at handoff)

- Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- Baseline verified this session: `SEED=42 bash scripts/check.sh` → **ALL CHECKS PASSED** (convention-robustness, template validation, golden/data/coverage guards, all experiment-script imports OK).
- Verification guards: `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`.
- Optimizer determinism pinned by `tests/test_portfolio_opt.py` (solver exit status must not gate feasibility/optimality).
- Data: pinned vintages `data/vintages.json` (2026-10-12), committed 2026-10-11 vintage, E029 fundamentals pinned in `data/fundamentals/` per `data/fundamentals_vintages.json`.
- Verification driver: `run_all_verification.py` (`--quick`/`--extended`/`--full`/`--skip-slow`/`--restore-only`). Backups in `.verify_snapshot/` (gitignored) with `ACTIVE.json` marker.
- CI workflow cannot be created by agents (controller restores `.github/workflows/`, token lacks `workflows` push). Template at `.github/workflow-templates/verification-gate.yml`; instructions in `VERIFICATION_GATE_TEMPLATE.md`.

## Immediate priorities (do in order)

1. **Clean baseline** — Run `git status --short`. If any tracked files differ, do **not** re-pin goldens. Follow AGENTS.md baseline integrity rules.
2. **Sanity check** — Run `SEED=42 bash scripts/check.sh` (convention-robustness + template validation + golden/data/coverage guards). All must pass.
3. **Verify reproducibility (choose scope)** — If check passes:
   - Quick (~8 min): `SEED=42 python3 run_all_verification.py`
   - Extended (~21 min): `SEED=42 python3 run_all_verification.py --extended` (E041 still has numeric drift; do **not** re-pin)
   - Full (~15–30 min): only if explicitly needed
4. **Recovery if interrupted** — If verification was cut out or goldens look modified: `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`. Confirm `.verify_snapshot/ACTIVE.json` removed.

## Known open items

- **E041 numeric drift (~133 diffs)** due to 1-ulp sensitivity of ill-conditioned tangency QP. Structural diffs resolved, gates/decision unchanged. Open in ledger (E049); do **not** silence by re-pinning.
- **E030/E029** now offline-reproducible via pinned inputs; do not revert to live yfinance downloads.
- **Data coverage invariant**: any new `data.download()` inputs must be committed and re-pinned via `python3 scripts/check_data_coverage.py --update`.

## Suggested first command

```bash
git status --short && echo "---" && SEED=42 bash scripts/check.sh
```

## Constraints honored this session

- Always use `SEED=42`.
- Honor pinned cache vintages (`data/vintages.json`, fundamentals pins in `data/fundamentals/`).
- Never leave a verification run half-finished (the suite backs up and restores `experiments/*.json`).
- Do not commit verification outputs; only intentional source/data changes.
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or validated constructions.
- CI workflow creation is maintainer-gated (template at `.github/workflow-templates/verification-gate.yml`, instructions in `VERIFICATION_GATE_TEMPLATE.md`).

## What was NOT done (by design)

No code changes, no new experiments, no golden re-pinning. This session's only action was verifying the baseline (`SEED=42 bash scripts/check.sh` → ALL CHECKS PASSED) and writing this handoff. The working tree remains clean of tracked changes.

## Current handoff pointer

This session's durable handoff: `HANDOFF_NEXT_SESSION_2026-10-28T10-30-06Z.md` (this file). See also `HANDOFF_NEXT.md`.
