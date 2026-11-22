# Agent Handoff — 2026-11-22T20:52:18Z

## Initial Task for Next Session
- **Goal**: Resume quantitative research *verification* work. No new research is queued;
  research phase is closed (E001–E043, with handoff-refresh ledger entries E001–E710).
- **First action**: Run `SEED=42 bash scripts/check.sh` (offline, seconds) to confirm the
  repository is green: golden integrity (`check_goldens_clean.py`,
  `check_golden_baseline.py`), data coverage, and optimizer-determinism tests.
- **If clean**: Pick a verification tier by time budget — `make verify-quick` (~8 min),
  `make verify-extended` (~21 min), or `make verify-full` (~15 min + 50 sims). Leave the
  tree clean afterward (never leave a verification run half-finished).
- **If dirty**: Recover with `SEED=42 python3 run_all_verification.py --restore-only`
  (or restore a pinned artifact via `git checkout <commit> -- experiments/<file>`).

## IMPORTANT — Do not repeat the handoff-only refresh loop
Ledger entries E652–E710 record a runaway loop in which successive sessions did nothing but
regenerate timestamped handoff files (thousands now committed). **Writing another handoff is
not real work.** This session's handoff exists only because it was explicitly requested to
leave a durable initial task message. Before creating yet another `handoff_*` file, do
something substantive: run a verification tier, fix an open ledger item, or close a task.
If you find yourself about to write a handoff with no other change, stop — instead run
`make check` / a verification tier and report real results.

## Session Context
- **Project**: Quantitative Trading Public Research (2014–2026 US equities, futures, macro)
- **Phase**: Research complete (E001–E043). Surviving strategies in `ledger/RESEARCH_LEDGER.md`
- **Working Directory**: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
- **HEAD at creation**: `28d1565b294c0a8a86834b65ea3ae537f65e32ad` on `main` == `origin/main`
  (`git rev-list --left-right --count origin/main...HEAD` = `0  0`; clean working tree;
  `git diff HEAD -- experiments/` empty; no `.verify_snapshot/` or `.verify_reports/`).

## Key Commands (from AGENTS.md)
```bash
# Fast check (seconds, offline)
SEED=42 bash scripts/check.sh
# Quick verification (~8 min)
SEED=42 python3 run_all_verification.py
# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended
# Full verification (~15 min + 50 sims)
SEED=42 python3 run_all_verification.py --full
# Convention robustness only (reads JSONs, no writes)
SEED=42 python3 verify_convention_robustness.py
```

## Critical Integrity Notes
- **Never leave verification half-finished**: `experiments/*.json` are backed up to
  `.verify_snapshot/` with an `ACTIVE.json` marker. If killed, recover with
  `SEED=42 python3 run_all_verification.py --restore-only`.
- **Golden baseline pinned in `ledger/golden_baseline.json`** — do not re-pin as a side
  effect of a verification run; re-pinning requires a ledger entry and a deliberate diff.
- **Data cache coverage enforced**: `scripts/check_data_coverage.py` validates all
  `data.download()` call sites against `ledger/data_baseline.json`. Add inputs by
  committing the file and re-pinning with `python3 scripts/check_data_coverage.py --update`.
- **CI workflow cannot be created by agents** — template at
  `.github/workflow-templates/verification-gate.yml` (see `VERIFICATION_GATE_TEMPLATE.md`).

## Current State (verified this session)
- Both pure-Python golden guards PASS: `check_goldens_clean.py` -> ALL COMMITTED GOLDEN
  ARTIFACTS MATCH HEAD (exit 0); `check_golden_baseline.py` -> ALL 107 PINNED GOLDEN
  ARTIFACTS MATCH THE BASELINE FINGERPRINT (exit 0). Guards are hashlib-only; the full
  verification suite was not run (deps not provisioned).
- All experiments committed to `experiments/*.json`; no stale snapshot pending.
- E029 fundamentals pinned in `data/fundamentals/` per `data/fundamentals_vintages.json`.
- E030 16-ETF panel committed (ledger E048).
- E041 optimizer defect fixed (ledger E049) — 133 numeric diffs remain (ill-conditioned QP),
  **do not re-pin** to silence the extended drift report.
- E041/E042 tangency QP remains ill-conditioned (~1e-05 drift per 1-ulp perturbation);
  optimizer determinism rule pinned by `tests/test_portfolio_opt.py` — do not re-pin.

## Next Steps (if resuming)
1. Run `SEED=42 bash scripts/check.sh` to verify clean state.
2. Choose a verification tier based on time budget and run it to completion.
3. Check `ledger/RESEARCH_LEDGER.md` open items before any re-pinning or new work.