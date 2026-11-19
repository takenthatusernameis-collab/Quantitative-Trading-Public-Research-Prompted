# Initial Task Message — Next Agentic Work Session

**Written:** 2026-11-19T04:45:59Z
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**HEAD at write time:** `e61cd4d3` (`chore(kilo): checkpoint agent session`), equal to `origin/main`
**Supersedes:** `handoff_2026-11-19T04-42-47Z_INITIAL_TASK.md` (only as the current pointer; no earlier handoff is edited)

---

## START HERE — ordered checklist for the next session

1. **Orient on the live tree (read-only, ~seconds).**
   ```bash
   git status --short --branch
   git log --oneline -5
   git rev-parse HEAD origin/main
   ```
   Expect a clean tree on `main` tracking `origin/main`. If the tree is dirty under
   `experiments/`, stop and go to step 2 before anything else.

2. **Recover any interrupted verification run.**
   ```bash
   ls -d .verify_snapshot .verify_reports 2>/dev/null
   SEED=42 python3 run_all_verification.py --restore-only   # only if a snapshot is pending
   ```
   A live run is safe to let finish; a stale one must be restored (or
   `git checkout -- experiments/`) before committing anything.

3. **Confirm the golden baseline is intact.**
   ```bash
   python3 scripts/check_goldens_clean.py     # working tree vs HEAD
   python3 scripts/check_golden_baseline.py   # HEAD vs ledger/golden_baseline.json SHA-256
   ```
   Both must pass. Never "fix" a failure by re-pinning; restore the pinned artifact instead.

4. **Install dependencies (this runner has none pre-installed).**
   ```bash
   pip install -r requirements.txt
   ```
   Verified in the writing session: `/usr/bin/python3` is 3.12.3 and `numpy` is
   **not** importable, so `scripts/check.sh` was not executed here.

5. **Run the fast gate before any new work.**
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   Offline, seconds: goldens-clean, golden-baseline fingerprint, data-coverage,
   template/import/JSON checks, optimizer-determinism test.

6. **Await explicit user direction.** Research is closed (E001–E051); do not start
   new experiments, re-pin baselines, or "improve" artifacts on your own.

7. **Before you finish, leave your own handoff** — see *Handoff procedure* below.

---

## Current state (verified in the writing session)

| Check | Result |
|---|---|
| `git status --short --branch` | `## main...origin/main`, clean before this write |
| HEAD vs `origin/main` | `e61cd4d37976b059469c656a5b5905421d874587` on both |
| `.verify_snapshot/` / `.verify_reports/` | absent — no interrupted run to recover |
| `scripts/check_goldens_clean.py` | ALL COMMITTED GOLDEN ARTIFACTS MATCH HEAD |
| `scripts/check_golden_baseline.py` | ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT |
| Canonical artifacts | 138 tracked files under `experiments/` |
| Python | 3.12.3, numpy/pandas/scipy **not** installed on this runner |

## Verification scopes

```bash
SEED=42 bash scripts/check.sh                          # fast gate, offline, seconds
SEED=42 python3 run_all_verification.py                # quick, ~8 min (8 drivers + batch + validate + E042 n_sim=2)
SEED=42 python3 run_all_verification.py --extended     # ~21 min (+18 drivers, structural match)
SEED=42 python3 run_all_verification.py --full         # ~15 min (E042 n_sim=50 + 96-config sensitivity)
SEED=42 python3 run_all_verification.py --skip-slow    # convention checks only
SEED=42 python3 run_all_verification.py --restore-only # recover goldens after interruption
SEED=42 python3 verify_convention_robustness.py        # reads JSONs, no writes
```

## Known drift / open items (ledger E045, E048, E049)

| Experiment | Status | Note |
|---|---|---|
| E029 | Reproduces with 0 diffs | Fundamentals pinned in `data/fundamentals/` per `data/fundamentals_vintages.json` |
| E030 | Reproduces with 0 diffs | 16-ETF panel committed; golden deliberately re-pinned per E048 |
| E041 | Still drifts (133 numeric diffs) | Ill-conditioned tangency QP, 1-ulp sensitivity. **Do not re-pin.** |
| E042 grid | Still drifts (29–133 numeric diffs) | Same QP. **Do not re-pin.** |

**Optimizer rule (E049):** `src/portfolio_opt.py` validates the answer on the
problem's constraints, never on the SLSQP exit status (status 8 at a constrained
optimum is acceptable and scipy-build dependent). Pinned by `tests/test_portfolio_opt.py`.

## Integrity rules (non-negotiable)

- Golden artifacts under `experiments/` are canonical; verification must never
  leave its output behind. Restore before committing.
- Replacing a golden requires re-pinning via
  `python3 scripts/check_golden_baseline.py --update` so the change shows in the diff.
  Never re-pin to silence drift.
- Every `data.download()` input must be a tracked cache file pinned in
  `ledger/data_baseline.json`; verification runs with `QUANT_RESEARCH_OFFLINE=1`.
  Add inputs by committing the file, then `python3 scripts/check_data_coverage.py --update`.
- Never commit verification output, `__pycache__`, or `.verify_snapshot/`.

## Key references

- `AGENTS.md` — commands, verification tiers, baseline-integrity history
- `ledger/RESEARCH_LEDGER.md` — all findings incl. E045/E048/E049 and handoff-refresh entries
- `ledger/PRIORITIZATION.md` — standing dispositions
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints
- `.github/workflow-templates/verification-gate.yml` + `VERIFICATION_GATE_TEMPLATE.md`
  — CI gate template (agents cannot create `.github/workflows/`; a maintainer must)

## Handoff procedure (repeat each session)

1. Write `handoff_<UTC ISO with dashes>_INITIAL_TASK.md` at the repo root, e.g.
   `handoff_2026-11-19T04-45-59Z_INITIAL_TASK.md`, with a fresh timestamp header,
   the ordered checklist, and the state verified that session.
2. Repoint every generic pointer:
   ```bash
   python3 scripts/repoint_handoff.py handoff_<timestamp>_INITIAL_TASK.md
   ```
   It touches only timestamp-free aliases in `.`, `handoff/`, `HANDOFFS/`,
   `.handoff/`, `.kilo/`, `.kilo/handoff/` and audits them (expect `0 bad`).
3. Append a ledger entry `## E<next>: Durable Handoff Refresh — Clear Initial Task Message
   (HEAD <sha>) [<timestamp>]` recording actions, verification output, and constraints honored.
4. Leave the work uncommitted unless the user asks for a commit; the controller
   checkpoints the session.

---

**Next session's first substantive step:** `pip install -r requirements.txt` then
`SEED=42 bash scripts/check.sh` — the gate has not yet been executed on this runner.
