# Durable Handoff — Next Agentic Work Session

**Timestamp:** 2026-10-31T05:06:39Z
**Branch:** `main`
**HEAD:** `b9a098f` (chore(kilo): checkpoint agent session)
**Working tree:** clean of tracked changes (only `__pycache__/*.pyc`, gitignored).
**Verification snapshot:** none active (`.verify_snapshot/` absent).

---

## INITIAL TASK (do first)

**Confirm baseline integrity before making any changes or running verification.**

1. Run `SEED=42 bash scripts/check.sh` — expect exit 0. Re-verified this session: exit 0, all guards green, all experiment-script imports OK.
2. `check_goldens_clean.py` compares working tree to HEAD. Since HEAD is a checkpoint commit, restored goldens may differ from HEAD — that is expected; the pinned baseline in `ledger/golden_baseline.json` is authoritative. Do NOT `git checkout -- experiments/`.
3. If any pinned artifact differs from its SHA-256 in `ledger/golden_baseline.json`, restore from the matching commit (`git checkout <commit> -- experiments/<file>`); never re-pin without explicit justification.
4. After green checks, idle awaiting explicit user direction. Do not modify goldens, re-pin baselines, or run extended/full verification without explicit instruction.

---

## Current state

- Working tree restored to pinned baseline (goldens match pinned fingerprint).
- Manifests untouched (`ledger/golden_baseline.json`, `ledger/data_baseline.json`).
- No source or data changes.
- Reproducibility caveat documented: E041/E042 sensitivity grids are not byte-reproducible in this sandbox (SLSQP/BLAS-sensitive); no gate or decision affected. See `HANDOFF_REPRO_CAVEAT.md`.

## Known pre-existing drift (reporting-only, decisions unchanged)

- **E041**: ~133 numeric diffs (1-ulp sensitivity of an ill-conditioned QP; optimizer determinism fixed per ledger E049). Structural differences gone. Do **not** re-pin.
- **E042 lead artifacts**: sensitivity grids show similar 1-ulp sensitivity (29-133 numeric diffs). **Do not re-pin.**
- **E030**: numeric diffs on near-zero quantities (documented). Do **not** re-pin.
- **E029/E030 inputs**: pinned for offline reproducibility; goldens deliberately re-pinned. Do not "fix" by re-running.

## Constraints

- Always use `SEED=42`.
- Honor pinned cache vintages (`data/vintages.json`, fundamentals pins in `data/fundamentals/`).
- Never leave a verification run half-finished (the suite backs up and restores `experiments/*.json` via `.verify_snapshot/`).
- Do not commit verification outputs; only intentional source/data changes.
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or validated constructions (`src/backtest.py`, `src/strategies.py`, `src/futures.py`, `src/macro.py`, `src/portfolio_opt.py`).
- CI workflow creation is maintainer-gated (template at `.github/workflow-templates/verification-gate.yml`, instructions in `VERIFICATION_GATE_TEMPLATE.md`).