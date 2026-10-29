# Handoff — Next Agentic Work Session

**Timestamp (UTC):** 2026-10-29T21:36:01Z
**Status:** Initial task message (durable handoff)
**Session Owner:** Kilo (current session)
**Branch:** main
**Commit:** 7ce6d99 (`chore(kilo): checkpoint agent session`)
**Working tree:** clean (no modifications, no untracked files, no staged files)
**No `.verify_snapshot/` active** — no stale/pending verification output.

## Initial Task

**PRIMARY OBJECTIVE:** Confirm repository baseline integrity and a clean
starting state before any research work. The repo is already clean; run the
fast convention-robustness gate to verify:

```bash
SEED=42 bash scripts/check.sh
```

(or `make check`). This validates:
- Python syntax/imports across the codebase (`py_compile`)
- Golden artifact integrity vs HEAD (`check_goldens_clean.py`)
- Golden baseline pins match (`check_golden_baseline.py`)
- Data coverage/pinning (`check_data_coverage.py`)
- Experiment template/JSON schema validation
- Portfolio optimizer regression tests (`tests/test_portfolio_opt.py`)

If a previous verification run was interrupted and left driver output
instead of committed goldens, recover first:

```bash
SEED=42 python3 run_all_verification.py --restore-only
```

then re-run `scripts/check.sh`.

## Current State

- **Branch:** main, HEAD `7ce6d99 chore(kilo): checkpoint agent session`.
- **Working tree:** clean — no modified, untracked, or staged files.
- **No `.verify_snapshot/`** active; no stale verification output.
- **Research phase:** Complete (E001–E043). Surviving validated strategies in
  `ledger/RESEARCH_LEDGER.md`.
- **Baselines enforced:** `ledger/golden_baseline.json`,
  `ledger/data_baseline.json`.
- **This file supersedes** all prior `HANDOFF_NEXT_SESSION_*.md` and
  `handoff*.md` symlinks, which reference older commits.

## Outstanding Open Item (from ledger E049 / handoff)

The tangency QP in `src/portfolio_opt.py` remains **ill-conditioned** even
after the optimizer-determinism fix. A 1-ulp input perturbation still moves
the E041/E042 grid and E042-primary `min_var` answers by ~1e-05 to 2.6e-05,
producing 29–133 numeric differences vs. their goldens (down from 360–9273
before the fix). These artifacts are **deliberately left as-is** — re-pinning
them would bake this machine's numbers over an unfixed defect.

**Recommended next research-engineering task:** replace the SLSQP QP solves
with a well-conditioned, deterministic solver (for N <= 5, an exact
active-set enumeration of all KKT points is feasible and already used as
the reference oracle), then *deliberately* re-pin the affected artifacts.
Do NOT re-pin to silence drift — see the ledger's standing disposition.

A second, smaller, deliberately-unfixed defect lives at
`src/portfolio_opt.py:253`: `y0 = w_feas / max(mu_s'w_feas, 1e-12)` masks a
negative denominator at the 2019-10-16 rebalance, so the start point has
magnitude 8.1e+11 and violates `mu'y = 1` by 6.4e+09. SLSQP returns garbage
there (objective 3.7e+20); the feasibility check correctly rejects it and
the shipped code falls back to the LP vertex exactly as the golden did.
Fixing the start point (a max-`mu_s'w` LP on the feasible simplex) would
change published numbers and belongs to the same deliberate re-pin decision.

## Known Issues / Important Notes

- **Known reporting-only drifts (do NOT re-pin):**
  - E041: ~133 numeric diffs from ill-conditioned tangency QP sensitivity;
    optimizer determinism fixed per ledger E049. Structural diffs gone,
    decision unchanged (REJECTED 3/5).
  - E030/E029: data pinned for offline reproducibility.
- **Verification integrity:** If a previous verification was interrupted,
  recover with `SEED=42 python3 run_all_verification.py --restore-only`
  before running checks. The suite self-recovers at startup and refuses to
  start while another live run owns the snapshot.

## Constraints (Must Honor)

- **Always use SEED=42** for any reproducibility work.
- **Never modify `experiments/*.json`** as a side effect of verification —
  re-pinning requires `scripts/check_golden_baseline.py --update` with
  explicit justification.
- **Honor data pins:** All cached data must be committed and pinned;
  verification runs offline with `QUANT_RESEARCH_OFFLINE=1`.
- **Never leave verification half-finished:** Suite backs up/restores via
  `.verify_snapshot/` with PID tracking.
- **No gate weakening:** Don't change tolerances, skip logic, or verification
  gates.
- **No goalpost moves:** Don't alter pre-registered outcomes or validated
  strategy constructions.
- **CI workflow:** Cannot be created by agents (maintainer-gated). Template
  exists at `.github/workflow-templates/verification-gate.yml`.

## Quick Reference

```bash
# Fast integrity check (~seconds)
SEED=42 bash scripts/check.sh

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full

# Convention robustness only (reads JSONs, no writes)
SEED=42 python3 verify_convention_robustness.py

# Recover interrupted run
SEED=42 python3 run_all_verification.py --restore-only
```

## Key Documentation

- `AGENTS.md` — Full project conventions and commands
- `ledger/RESEARCH_LEDGER.md` — Complete experiment history and decisions
- `README.md` — Project overview
- `ledger/PRIORITIZATION.md` — Prioritized follow-up work list

**If `scripts/check.sh` passes cleanly, the repo is in a good state for the
next task. Report status and await further instructions.**
