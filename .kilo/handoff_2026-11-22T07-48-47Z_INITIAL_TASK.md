# Handoff — Next Agentic Work Session

**Timestamp:** 2026-11-22T07-48-47Z
**Ledger entry:** E673
**Working Directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Project:** Quantitative Trading Public Research (2014–2026 US equities, futures, macro)
**Research Phase:** COMPLETE (E001–E043). Surviving validated strategies: `ledger/RESEARCH_LEDGER.md`.

---

## Initial task message (read this first)

You are the next agentic work session. The research phase is **closed**; there is no
open experiment queue. This repo carries thousands of committed handoff files from a
runaway handoff-refresh loop (ledger E652–E672 and the uncommitted-then-committed
`handoff_2026-11-22T07-*` files). **Refreshing the handoff is not research and adds no
value** — only produce a new handoff like this one when the user explicitly asks for it,
as they did here.

**Do this, in order:**

1. **Orient on HEAD.** Confirm `git rev-parse HEAD` and `git status --short`. Expected
   starting point: clean tree on `main`, HEAD == `origin/main` (see *Verified state*).
2. **Recover any interrupted verification first.** If `.verify_snapshot/` exists with a
   live `ACTIVE.json`, or `git status` shows `experiments/*.json` modified, a prior run
   was interrupted. Run `SEED=42 python3 run_all_verification.py --restore-only` and
   re-check both golden guards before doing anything else. **Never commit while the
   baseline is dirty.**
3. **Confirm both golden guards pass:**
   - `SEED=42 python3 scripts/check_goldens_clean.py` -> `ALL COMMITTED GOLDEN ARTIFACTS MATCH HEAD`
   - `SEED=42 python3 scripts/check_golden_baseline.py` -> `ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT`
   Both are pure-Python (hashlib only) and run without pandas/numpy.
4. **Provision deps if needed:** `pip install -r requirements.txt` (numpy, pandas, scipy,
   pyarrow, statsmodels, yfinance; cvxpy/cvxopt optional). This session's environment does
   **not** have pandas/numpy installed, so the full verification suite could not be run here.
5. **Fast sanity check:** `SEED=42 bash scripts/check.sh` (~seconds, offline).
6. **Do the actual user task, or STOP.** If the user gave a concrete task, do it. If not,
   stop — do **not** invent work, and do **not** re-run a handoff refresh as a substitute
   for real work.
7. **Leave your own handoff** (see *Recurring handoff procedure* below), then stop.

---

## Verified state (at 2026-11-22T07-48-47Z)

- **HEAD:** `dafe1b60e6bddd4c14abddf234050db6edfeaa6c` on `main` == `origin/main`
  (commit `chore(kilo): checkpoint agent session`, 2026-11-22 07:47:44 +0000).
- **Working tree:** modified only tracked `__pycache__/*.pyc` build bytecode; `experiments/`
  untouched (`git diff HEAD -- experiments/` empty).
- **Golden guards (executed this session):**
  - `scripts/check_goldens_clean.py` -> **PASS** (`ALL COMMITTED GOLDEN ARTIFACTS MATCH HEAD`)
  - `scripts/check_golden_baseline.py` -> **PASS** (`ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT`)
- **`.verify_snapshot/` and `.verify_reports/`:** absent (no interrupted run).
- **Deps:** pandas/numpy **not** installed in this session; full verification not run.

---

## Numbering note (read before trusting any "E###" reference)

The committed `ledger/RESEARCH_LEDGER.md` is the authoritative entry log; its highest
committed entry is **E672**. Recent handoff files self-assigned numbers that do **not**
match the ledger:

- `handoff_2026-11-22T07-45-45Z_INITIAL_TASK.md` self-identified as **E673**
- `handoff_2026-11-22T07-46-59Z_INITIAL_TASK.md` self-identified as **E674**

Neither E673 nor E674 was ever appended to the ledger. Those self-assigned numbers are
unreliable. **This refresh claims the true next free slot, E673**, appended to the ledger
this session. When in doubt, trust the committed ledger, not a handoff file's header.

---

## Verification scopes

| Command | Scope | Time |
|---------|-------|------|
| `SEED=42 bash scripts/check.sh` | convention robustness + template validation | ~seconds |
| `SEED=42 python3 run_all_verification.py` | quick: 8 drivers + batch_run + validate | ~8 min |
| `SEED=42 python3 run_all_verification.py --extended` | + 18 more committed drivers | ~21 min |
| `SEED=42 python3 run_all_verification.py --full` | E042 n_sim=50 + 96-config grid | ~15 min |
| `SEED=42 python3 run_all_verification.py --restore-only` | recover goldens after interrupted run | fast |

---

## Integrity rules (do not violate)

- **Golden files** (`experiments/*.json`) are canonical. Verification overwrites then
  restores them. **Never leave a verification run half-finished.**
- **Never re-pin** a golden or data baseline to silence drift. Re-pinning requires an
  explicit `scripts/check_golden_baseline.py --update` / `scripts/check_data_coverage.py
  --update` and must appear in the diff with a ledger justification.
- **Data coverage is an enforced invariant.** Every `data.download()` call site must have
  a committed, SHA-256-pinned cache file (`ledger/data_baseline.json`). Verification runs
  with `QUANT_RESEARCH_OFFLINE=1`, so a missing cache entry fails hard.
- **Do not commit verification output.** If interrupted, restore goldens first
  (`run_all_verification.py --restore-only` or `git checkout -- experiments/`).

---

## Carried-forward open items

- **E041 / E042 QP drift (ledger E049):** 133 and 29–133 numeric diffs respectively, from
  a 1-ulp-sensitive ill-conditioned tangency QP. Zero structural diffs; decisions/gates
  unchanged. **Do not re-pin** — this is a known, documented open item.
- **Optimizer determinism:** `src/portfolio_opt.py` validates a solver answer on the
  problem's constraints, never on the solver exit status. Pinned by
  `tests/test_portfolio_opt.py`.
- **Promotion path:** any PARTIAL result that clears gates in a sensitivity grid needs a
  dedicated pre-registered confirmatory run with a full placebo before promotion
  (multiple-testing discipline).
- **CI gate:** `.github/workflows/` cannot be created by agents. Template lives at
  `.github/workflow-templates/verification-gate.yml`; a maintainer must create it via the
  GitHub UI (see `VERIFICATION_GATE_TEMPLATE.md`).

---

## Key references

- `AGENTS.md` — project commands & conventions
- `ledger/RESEARCH_LEDGER.md` — experiment ledger (E001–E043 + handoff refreshes through E672, plus this E673)
- `ledger/golden_baseline.json` — SHA-256 fingerprints of 107 canonical artifacts
- `ledger/data_baseline.json` — SHA-256 fingerprints of pinned data caches
- `scripts/repoint_handoff.py` — repoints generic handoff aliases to the new artifact
- `scripts/check.sh` — fast local gate

---

## Provenance

- Prior refresh: 2026-11-22T07-46-59Z (`handoff_2026-11-22T07-46-59Z_INITIAL_TASK.md`,
  which self-identified as E674 but never reached the ledger).
- This handoff was written with a clean `experiments/` tree at HEAD `dafe1b60`. Both golden
  guards were executed and PASS; no verification suite was run (pandas/numpy absent).
- Constraints honored: no golden/data baseline re-pinned, no verification suite run, no
  verification output committed, no new research performed. Left uncommitted pending
  explicit direction, per the established disposition.

---

## Recurring handoff procedure (how this artifact was produced)

1. Pick `TS` = current UTC, e.g. `date -u +%Y-%m-%dT%H-%M-%SZ`.
2. Write `handoff_<TS>_INITIAL_TASK.md` at repo root.
3. Copy it byte-for-byte into the five mirror dirs:
   `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/`.
4. Repoint generic aliases:
   `python3 scripts/repoint_handoff.py handoff_<TS>_INITIAL_TASK.md`
   (expect `bad=0`; it leaves timestamped / `HANDOFF_NEXT_SESSION_*` / `HANDOFF_2026*`
   names untouched).
5. Verify SHA-256 is identical across all six copies.
6. Append a short ledger entry (`## E<next> — Durable handoff refresh (<TS>)`).
7. Do not commit unless the user explicitly asks.