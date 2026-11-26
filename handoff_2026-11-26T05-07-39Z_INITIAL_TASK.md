# Handoff — Next Agentic Work Session

**Timestamp:** 2026-11-26T05:07:39Z
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**HEAD:** a2cce96f0e2e5a2a1801d9401012b24496832e8b

## ⚠ Read first — do not repeat the handoff loop

A prior agent entered a degenerate loop and produced hundreds of near-identical
`handoff_*_INITIAL_TASK.md` files plus an explosion of alias symlinks
(`handoff_NEXT_SESSION_LATEST_HANDOFF.md.md`, `latest.md.md`, etc.). That is the
failure mode to avoid. This file is the single authoritative handoff. Do **not**
create additional handoffs, alias symlinks, or "just to be safe" copies unless the
user explicitly asks. One handoff per request, then stop.

## Project State

- **Phase:** Research complete (E001–E043). Surviving validated strategies are in
  `ledger/RESEARCH_LEDGER.md`.
- **Golden artifacts:** `experiments/*.json` (canonical baseline, SHA-256 pinned in
  `ledger/golden_baseline.json`).
- **Data vintage:** 2026-10-12 pinned in `data/vintages.json`; 2026-10-11 committed
  for E026/E028/E029/E030/E034/E036/E037. E029 fundamentals pinned in
  `data/fundamentals/` per `data/fundamentals_vintages.json`.
- **Working tree:** Clean for `experiments/` and `data/` at HEAD `a2cce96f`; no
  `.verify_snapshot/` present (no interrupted verification to recover).

## Verification Commands (SEED=42)

```bash
make check            # fast convention-robustness + template validation (~seconds, offline)
make verify-quick     # ~8 min; 8 drivers + batch_run + validate + E042 n_sim=2
make verify-extended  # ~21 min; quick + 18 more drivers, structural match
make verify-full      # ~15 min; E042 n_sim=50 + 96-config sensitivity grid
make verify           # convention robustness only (reads JSONs, no writes)
```

## Critical Integrity Notes

1. **Never leave verification half-finished** — it overwrites `experiments/*.json`
   and restores after. If interrupted: `SEED=42 python3 run_all_verification.py
   --restore-only` (or `git checkout -- experiments/`).
2. **Golden baseline is pinned** in `ledger/golden_baseline.json`. Do not re-pin as a
   side effect of verification; the committed golden is the authoritative record.
3. **Data coverage is enforced** — `scripts/check_data_coverage.py` requires every
   cache file to exist, be git-tracked, and match `ledger/data_baseline.json`. Run
   drivers with `QUANT_RESEARCH_OFFLINE=1`.
4. **Optimizer determinism** — validate on problem constraints, not solver exit
   status (SLSQP status 8 is valid at a constrained optimum). Fixed by E050 exact
   active-set enumeration in `src/portfolio_opt.py`; see `tests/test_portfolio_opt.py`
   and ledger E049/E050. E041/E042 ill-conditioned-QP drift is closed (0 diffs).
5. **CI gate cannot be created by agents** — template at
   `.github/workflow-templates/verification-gate.yml`; a maintainer must create it.
6. **Do not commit verification output** — restore goldens before committing.

## Initial Task

Default: await explicit user instructions. If acting autonomously:
1. Confirm working-tree cleanliness (`git status --short experiments/ data/`) and
   that no `.verify_snapshot/ACTIVE.json` exists.
2. Run `SEED=42 bash scripts/check.sh` (fast convention-robustness check).
3. If clean, reproduce with `SEED=42 python3 run_all_verification.py --extended` and
   report any drift; do **NOT** re-pin goldens.
4. If interrupted, recover with `SEED=42 python3 run_all_verification.py
   --restore-only` before committing anything.

## Last Verification Status

Prior measurement (2026-11-23T05:17Z, numpy 2.5.4, scipy 1.18.1): all 18 extended
drivers reproduce with 0 differences.

## Provenance

Supersedes `handoff_2026-11-26T05-06-19Z_INITIAL_TASK.md`. Written 2026-11-26T05:07:39Z.
