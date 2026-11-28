# INITIAL TASK — Handoff for Next Agent Session

**Timestamp (UTC): 2026-11-28T03:49:29Z**
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** main — `a812e46cee2d799aeaff740dcd614477a2ff37fa` (2026-11-28 03:49:10 +0000) == origin/main (`git rev-list --left-right --count origin/main...HEAD` = `0 0`)
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Working Tree:** clean. No `.verify_snapshot/`. `experiments/`, `data/`, `ledger/` match HEAD.

## Session Summary

- Responded to user request: *"Leave a timestamped clear initial task message for the next agentic work session in a durable handoff !"*.
- Verified live state before writing (see commands below): HEAD == origin/main == `a812e46c`; working tree clean; no interrupted verification run pending.
- Confirmed the P0 broken-golden-baseline finding from the prior handoff (`handoff_2026-11-28T03-48-30Z_INITIAL_TASK.md`) is **still unfixed at the new HEAD**: `scripts/check_golden_baseline.py` FAILS on the same 5 artifacts while `scripts/check_goldens_clean.py` PASSES (working tree == HEAD). This is the AGENTS.md "checkpoint commit captured verification output" failure mode.

## CLEAR INITIAL TASK

**P0 — Broken golden baseline at HEAD `a812e46c` (real, verified, still unfixed).**

`scripts/check_golden_baseline.py` **FAILS at HEAD**: 5 of 107 committed artifacts under `experiments/` differ from the SHA-256 pinned in `ledger/golden_baseline.json`, while `scripts/check_goldens_clean.py` still PASSES. That combination means a `chore(kilo): checkpoint agent session` commit replaced the canonical baseline with verification-run output (precedents `d6042b0`/`9f20def`, `1623923`, `701ed78`).

Drifted artifacts (pinned != actual):
- `experiments/cointegration_large_liquid.json`
- `experiments/dollar_neutral_lowbeta_large_liquid.json`
- `experiments/e037_portfolio.json`
- `experiments/e042_lead_config_confirmatory.json`
- `experiments/pairs_large_liquid.json`

**Verified recovery target: `c5038332` (2026-11-24 02:05:45Z).** `git diff --stat c5038332 HEAD -- experiments/` shows ONLY those 5 files differ, so:

```bash
git checkout c5038332 -- experiments/
python3 scripts/check_golden_baseline.py   # must print ALL 107 ... MATCH (exit 0)
```

Do **not** re-pin with `--update`; the committed golden is authoritative (E050 precedent).

### Prioritized real-work task list (in order)

1. **Recover the baseline** from `c5038332` (commands above); confirm `check_golden_baseline.py` → ALL 107 MATCH (exit 0).
2. **Provision deps**: `pip install -r requirements.txt` (numpy/pandas were not importable in recent sessions).
3. **Run** `SEED=42 python3 run_all_verification.py --extended` and confirm all committed drivers reproduce (0 structural diffs, numeric_tol=1e-4).
4. **Confirm E041/E042 tangency-QP drift stays closed** (E050 exact active-set solver) **without re-pinning** any artifact.
5. *Propose* — but do NOT execute — a handoff-file cleanup (the ~9,343-file mirror/repoint explosion; ~94% of tracked files are `handoff`-named). Surface the plan to the user first.

### Constraints

- No golden/data baseline re-pinned. No verification output committed. No new research.
- No commit unless the user explicitly asks.
- If you create a handoff at all, keep it to this one file; do NOT run `scripts/repoint_handoff.py` or create mirror directories.
- Do **not** re-open closed items (E049/E050 optimizer determinism + exact KKT enumeration; E041/E042 ill-conditioned QP drift — closed, artifacts reproduce 0 diffs).

## First Steps (verify state)

- `git log -1 --format="%H"` and `git status --short experiments/ data/ ledger/` — confirm HEAD == origin/main and canonical artifacts unmodified.
- `python3 scripts/check_golden_baseline.py` — currently FAILS (5 artifacts); this is the P0 above, not a new regression.
- `python3 scripts/check_goldens_clean.py` — currently PASSES (working tree == HEAD).
- Confirm no `.verify_snapshot/` directory exists.
- Read `ledger/RESEARCH_LEDGER.md` for surviving validated strategies (research phase closed, E001–E043).

## Key Constraints (from AGENTS.md)

- `experiments/*.json` are committed goldens — verification backs them up and restores them; never commit verification output or leave a run half-finished.
- Golden baseline enforced by `scripts/check_golden_baseline.py` vs `ledger/golden_baseline.json`; data coverage by `scripts/check_data_coverage.py` vs `ledger/data_baseline.json`.
- Optimizer: validate on problem constraints, not solver exit status (`tests/test_portfolio_opt.py`, ledger E049/E050).
- Always use `SEED=42`. Close-to-close is the v1.2.3 primary convention.
- CI workflow cannot be created by automated agents. Use local `make check/verify/*`.
- Never re-pin artifacts to silence drift; the committed golden is the authoritative record.

## Handoff provenance

Supersedes previous INITIAL_TASK handoff `handoff_2026-11-28T03-48-30Z_INITIAL_TASK.md` (which first surfaced the P0 at `80fdec89`). This file is the authoritative initial-task message for the next session and re-verifies the P0 at the newer HEAD `a812e46c`.

Handoff written by agent at 2026-11-28T03:49:29Z.