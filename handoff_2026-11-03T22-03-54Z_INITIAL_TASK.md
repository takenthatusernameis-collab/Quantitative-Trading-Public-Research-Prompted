# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC): 2026-11-03T22:03:54Z**
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** main — `24ad227` "chore(kilo): checkpoint agent session"
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

---

## Session recovery context

This is a fresh worker session. The previous session left the repository in a clean, checkpointed state and there is **no open research task in the queue**. This is a handoff turn, not a research turn. **Wait for explicit user instructions before taking any action that modifies the repo.**

This handoff supersedes all prior handoffs in the repo root and `handoff/`.

## Repo state (verified at handoff time)

- `git status --short` is **empty** for non-`__pycache__` files — working tree clean, no `experiments/` diff. Only modifications are `__pycache__/*.pyc` files (bytecode caches, not source).
- `HEAD` = `24ad22799b07aa1eb1f1587e50c5b42c7924c7dd`; `origin/main` = `24ad22799b07aa1eb1f1587e50c5b42c7924c7dd` (agree).
- `.verify_snapshot/` is **ABSENT** — no live verification run, nothing to recover.
- No stash. `experiments/` holds committed golden JSONs protected by `ledger/golden_baseline.json`.

## Goal

Continue quantitative strategy research per `AGENTS.md`. Research phase is complete (E001–E043); surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`. **There is currently NO open task in the queue.**

## Immediate Priorities (in order)

1. Confirm repo is still clean: `git status --short` and `git rev-parse HEAD origin/main` should agree.
2. If `.verify_snapshot/ACTIVE.json` appears, a verification run was interrupted — run `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`) before anything else.
3. Understand research status — read `ledger/RESEARCH_LEDGER.md` and `AGENTS.md`.
4. Follow verification discipline strictly:
   - Always `SEED=42`.
   - Never re-pin goldens as a side effect of running the suite.
   - Never leave a verification run half-finished; restore `experiments/` if interrupted.
   - New `data.download()` input requires a committed cache file + `ledger/data_baseline.json` re-pin via `python3 scripts/check_data_coverage.py --update`.
5. **Wait for explicit user task/instructions before taking action.**

## Quick Commands

```bash
ls -la .verify_snapshot/ 2>&1 | head
git status --short && git rev-parse HEAD origin/main
SEED=42 bash scripts/check.sh
SEED=42 python3 run_all_verification.py --restore-only
SEED=42 python3 run_all_verification.py --full   # ~15 min full verification
```

## Known Invariants / Caveats

- **Golden baseline is authoritative.** Replacing an artifact under `experiments/` requires explicit re-pinning (`python3 scripts/check_golden_baseline.py --update`); it will show up in the diff. Never re-pin as a side effect of verification.
- **Offline by default in verification.** Missing pinned caches must fail hard (`QUANT_RESEARCH_OFFLINE=1`); do not rely on live downloads.
- **Optimizer determinism (ledger E049):** `src/portfolio_opt.py` validates a solver answer on the problem's constraints, never on the solver's exit status. SLSQP status 8 is acceptable at a constrained optimum. The tangency QP remains ill-conditioned: a 1-ulp input perturbation moves `min_var` answers by ~1e-05, so E041/E042 grid artifacts drift by 29–133 numeric differences. **Do not re-pin them to silence that** — it is an open ledger item.
- **E029 / E030 are offline-reproducible since 2026-10-20** (data/fundamentals snapshot and 16-ETF panel pinned; goldens deliberately re-pinned to those snapshots).
- **E041 still drifts** (133 numeric diffs, 0 structural) — reported, not gated.
- **CI workflow:** Cannot be created by agents. Template at `.github/workflow-templates/verification-gate.yml`, instructions in `VERIFICATION_GATE_TEMPLATE.md`. `make check` / `make verify` / `make verify-full` are the local equivalents.
- **Dependencies:** `pip install -r requirements.txt` before verification if the environment is fresh.

## Key Pointers

- **Ledger:** `ledger/RESEARCH_LEDGER.md`
- **Golden pin:** `ledger/golden_baseline.json`
- **Data pin:** `ledger/data_baseline.json`
- **Verification:** `run_all_verification.py`, `scripts/check.sh`, `make verify-quick/extended/full`
- **Conventions:** `AGENTS.md`
- **Project config:** `kilo.json`

---

**Ready to start: confirm repo cleanliness, then wait for the user's task.**
