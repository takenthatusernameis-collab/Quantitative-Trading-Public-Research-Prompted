# Initial Task Handoff — Next Agentic Work Session

**Timestamp**: 2026-11-19T00:53:41Z
**Session ID**: Durable handoff for the next agentic work session (E512)
**Project**: Quantitative-Trading-Public-Research-Prompted
**Working Directory**: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**HEAD at write time**: `7b7b0532` (`chore(kilo): checkpoint agent session`), working tree clean, `main` == `origin/main`

---

## START HERE — Your First Task

1. **Install deps (required on this runner).** Bare `/usr/bin/python3` (3.12.3) has
   **no** numpy/pandas/scipy — `import pandas` raises `ModuleNotFoundError`. Run:

   ```bash
   python3 -m pip install -r requirements.txt
   ```

2. **Run the fast integrity gate** (~seconds, offline, must pass before any commit):

   ```bash
   SEED=42 bash scripts/check.sh      # or: make check
   ```

3. **If the gate is green**, the repository is in its documented closed state — do
   **not** invent research. Only act on an explicit new instruction. If a new
   experiment is requested, follow the pre-registration + falsification protocol
   below and record it in `ledger/RESEARCH_LEDGER.md`.

4. **Leave your own handoff** at the end of the session using the procedure in
   *Handoff Procedure* below (new timestamped artifact + mirrors + repoint + ledger entry).

---

## Project Status Summary

- **Research phase**: Complete (E001–E051). Surviving validated strategies are in
  `ledger/RESEARCH_LEDGER.md`; selection criteria in `ledger/PRIORITIZATION.md`.
- **Artifacts**: `experiments/*.json` are canonical goldens; `ledger/golden_baseline.json`
  pins their SHA-256; `ledger/data_baseline.json` pins every cached data input.
- **Verification tiers**: `check` (seconds) → `verify-quick` (~8 min) →
  `verify-extended` (~21 min) → `verify-full` (~15 min).
- **No open research items.** Known, accepted drift: E041/E042 tangency QP is
  ill-conditioned (1-ulp input perturbation → ~1e-05 moves in `min_var`). This is
  documented (ledger E049) and must **not** be silenced by re-pinning goldens.

---

## Critical Integrity Rules (READ BEFORE RUNNING)

1. **Never leave verification half-finished.** A killed run leaves `.verify_snapshot/`
   with an `ACTIVE.json` pid marker. Recover with
   `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`).
2. **Never commit verification output.** `scripts/check_goldens_clean.py` (compares tree
   to HEAD) and `scripts/check_golden_baseline.py` (compares to the pinned SHA-256) are
   first-class steps of `scripts/check.sh`. Fix a mismatch before committing; re-pin only
   deliberately via `python3 scripts/check_golden_baseline.py --update` and say so in the diff.
3. **Data coverage is an enforced invariant** (ledger E048). Every `data.download()` call
   site must have a committed, SHA-256-pinned cache file, or the suite fails hard under
   `QUANT_RESEARCH_OFFLINE=1`. New input → commit file + `python3 scripts/check_data_coverage.py --update`.
4. **Optimizer determinism** (ledger E049). `src/portfolio_opt.py` validates on problem
   constraints, never solver exit status. Do not gate on SLSQP status 8.
5. **No golden/data re-pins, no `__pycache__` commits, no committing unless explicitly asked.**

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
   `.kilo/handoff/` (e.g. `cp -f <file> handoff/ && ...`) and verify with `sha256sum`.
3. Repoint the generic pointers: `python3 scripts/repoint_handoff.py <file>`; confirm
   0 dangling symlinks.
4. Append a ledger entry (`## E<n>: Durable Handoff Refresh (HEAD <sha>) [<ts>]`) with
   HEAD, tree status, verification performed, and constraints honored.
5. Leave changes **uncommitted** unless the user asks for a commit.

---

## Environment Notes (this runner)

- Deps missing at handoff time: `numpy`, `pandas`, `scipy` not importable → `scripts/check.sh`
  was **not** run this session; only static/link integrity was verified.
- `.verify_snapshot/` and `.verify_reports/` absent; no interrupted run to recover.
- `experiments/` clean against HEAD at write time.

---

**Handoff Complete** — resume by installing deps and running `SEED=42 bash scripts/check.sh`.
