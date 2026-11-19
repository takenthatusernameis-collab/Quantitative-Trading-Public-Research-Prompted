# Initial Task Handoff — Next Agentic Work Session

**Timestamp**: 2026-11-19T01:35:25Z
**Session**: Durable handoff for the next agentic work session (E514)
**Project**: Quantitative-Trading-Public-Research-Prompted
**Working Directory**: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**HEAD at write time**: `48ac63ab` (`chore(kilo): checkpoint agent session`), working tree clean apart from gitignored `__pycache__`, `main` == `origin/main`

---

## START HERE — Your First Task

1. **Orient (cheap, no side effects).**

   ```bash
   git rev-parse HEAD && git status --short --branch
   ls -d .verify_snapshot .verify_reports 2>/dev/null   # must print nothing
   git diff --name-only HEAD -- experiments/             # must print nothing
   ```

   If `.verify_snapshot/ACTIVE.json` exists, a verification run was interrupted —
   recover **before** anything else:
   `SEED=42 python3 run_all_verification.py --restore-only`.

2. **Install deps (required on this runner).** Bare `/usr/bin/python3` (3.12.3) has
   no numpy/pandas/scipy (`import pandas` → `ModuleNotFoundError`):

   ```bash
   python3 -m pip install -r requirements.txt
   ```

3. **Run the fast integrity gate** (~seconds, offline, must pass before any commit):

   ```bash
   SEED=42 bash scripts/check.sh      # or: make check
   ```

4. **Then stop and wait for an explicit instruction.** The repository is in its
   documented closed state. Do **not** invent research, re-run the full suite "to be
   sure", create extra handoffs unprompted, or re-open closed items (E049/E050
   optimizer determinism + exact KKT enumeration; E041/E042 ill-conditioned QP drift —
   all closed and documented). If a new experiment is requested, follow the
   pre-registration + falsification protocol and record it in `ledger/RESEARCH_LEDGER.md`.

5. **Leave your own handoff** at session end using *Handoff Procedure* below.

---

## Project Status Summary

- **Research phase**: Complete (E001–E051). Surviving validated strategies are in
  `ledger/RESEARCH_LEDGER.md`; selection criteria in `ledger/PRIORITIZATION.md`.
  Ledger tail after E511 is durable-handoff/closure refreshes only.
- **Artifacts**: `experiments/*.json` are the canonical goldens;
  `ledger/golden_baseline.json` pins their SHA-256; `ledger/data_baseline.json` pins
  every cached data input (2026-10-12 and 2026-10-11 vintages plus
  `data/fundamentals/`).
- **Verification tiers**: `check` (seconds) → `verify-quick` (~8 min) →
  `verify-extended` (~21 min) → `verify-full` (~15 min).
- **No open research items.** Known, accepted drift: E041/E042 tangency QP is
  ill-conditioned (1-ulp input perturbation → ~1e-05 moves in `min_var`). Documented
  in ledger E049; must **not** be silenced by re-pinning goldens.

---

## Critical Integrity Rules (READ BEFORE RUNNING)

1. **Never leave verification half-finished.** A killed run leaves `.verify_snapshot/`
   with an `ACTIVE.json` pid marker. Recover with
   `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`).
2. **Never commit verification output.** `scripts/check_goldens_clean.py` (tree vs HEAD)
   and `scripts/check_golden_baseline.py` (tree vs pinned SHA-256) are first-class steps
   of `scripts/check.sh`. Fix a mismatch before committing; re-pin only deliberately via
   `python3 scripts/check_golden_baseline.py --update` and call it out in the diff.
3. **Data coverage is an enforced invariant** (ledger E048). Every `data.download()` call
   site needs a committed, SHA-256-pinned cache file, or the suite fails hard under
   `QUANT_RESEARCH_OFFLINE=1`. New input → commit file +
   `python3 scripts/check_data_coverage.py --update`.
4. **Optimizer determinism** (ledger E049). `src/portfolio_opt.py` validates on problem
   constraints, never on solver exit status. Do not gate on SLSQP status 8.
5. **No golden/data re-pins, no `__pycache__` commits, no commits unless explicitly asked.**

---

## Key Commands

```bash
SEED=42 bash scripts/check.sh                       # fast gate (~seconds, offline)
SEED=42 python3 run_all_verification.py             # quick (~8 min)  == make verify-quick
SEED=42 python3 run_all_verification.py --extended  # extended (~21 min) == make verify-extended
SEED=42 python3 run_all_verification.py --full      # full (~15 min)  == make verify-full
SEED=42 python3 run_all_verification.py --restore-only
SEED=42 python3 verify_convention_robustness.py     # read-only convention check
```

Single experiments: `SEED=42 python3 experiments/run_e042.py --n-sim 50`, etc.

---

## Handoff Procedure (keep this going)

1. Write `handoff_<UTC ISO with colons replaced by '-'>_INITIAL_TASK.md` at repo root.
2. Mirror it **byte-identically** into `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`,
   `.kilo/handoff/` and verify with `sha256sum` (all six copies must match).
3. Repoint the generic pointers: `python3 scripts/repoint_handoff.py <file>`; confirm
   `bad=0` and spot-check `HANDOFF.md`, `LATEST.md`, `INITIAL_TASK.md`, `NEXT_SESSION.md`,
   `handoff/CURRENT`, `.kilo/HANDOFF.md`.
4. Append a ledger entry (`## E<n>: Durable Handoff Refresh (HEAD <sha>) [<ts>]`) with
   HEAD, tree status, verification performed, and constraints honored.
5. Leave changes **uncommitted** unless the user asks for a commit.

---

## Environment Notes (this runner)

- Deps missing at handoff time: numpy/pandas/scipy not importable → `scripts/check.sh`
  was **not** run this session; only static/link integrity was verified.
- `.verify_snapshot/` and `.verify_reports/` absent; no interrupted run to recover.
- `experiments/` clean against HEAD `48ac63ab` at write time.

---

**Handoff Complete** — resume by orienting, installing deps, then running `SEED=42 bash scripts/check.sh`.
