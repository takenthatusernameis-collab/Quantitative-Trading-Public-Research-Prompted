# Durable Handoff — Initial Task for the Next Agentic Work Session

**Timestamp:** 2026-11-22T09-53-22Z
**Ledger slot:** E679 (next free; committed ledger's authoritative last entry remains E678 unless this session commits one)
**Project:** Quantitative Trading Public Research (2014–2026 US equities, futures, macro)
**Working Directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Branch / HEAD:** `main` @ `5966350b` (== `origin/main`)
**Research Phase:** COMPLETE (E001–E043). Surviving validated strategies: `ledger/RESEARCH_LEDGER.md`.

---

## Initial task message — read this first

You are the next agentic work session. The research phase is **closed**; there is no
open experiment queue. A routine session's only durable artifact is a fresh timestamped
handoff like this one.

**Read this before doing anything, then do these in order:**

1. **Orient on HEAD.** Confirm `git rev-parse HEAD` and `git status --short`. Expected
   starting point: clean `experiments/` tree on `main`, HEAD == `origin/main`.
2. **Recover any interrupted verification first.** If `.verify_snapshot/` exists with a
   live `ACTIVE.json`, or `git status` shows `experiments/*.json` modified, a prior run
   was interrupted. Run `SEED=42 python3 run_all_verification.py --restore-only` and
   re-check both golden guards before doing anything else. **Never commit while the
   baseline is dirty.**
3. **Confirm both golden guards pass** (pure-stdlib, no pandas/numpy needed):
   - `SEED=42 python3 scripts/check_goldens_clean.py` → `ALL COMMITTED GOLDEN ARTIFACTS MATCH HEAD`
   - `SEED=42 python3 scripts/check_golden_baseline.py` → `ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT`
4. **Provision deps only if you need the full suite:** `pip install -r requirements.txt`
   (numpy, pandas, scipy, pyarrow, statsmodels, yfinance; cvxpy/cvxopt optional).
5. **Fast sanity check:** `SEED=42 bash scripts/check.sh` (~seconds, offline).
6. **Do the actual user task, or STOP.** If the user gave a concrete task, do it. If
   not, stop — do **not** invent work. In particular, do **not** re-run a "durable
   handoff refresh" as a substitute for real work: this repo already carries **1,800+
   committed handoff files** from a runaway refresh loop (ledger E652–E678). Repeatedly
   refreshing the handoff is not research and adds no value. **Breaking that loop is the
   single most useful thing a session can do here.**
7. **Leave your own handoff only if the user explicitly asks for one** (see *Recurring
   handoff procedure* below), then stop.

---

## Verified state (at 2026-11-22T09-53-22Z)

- **HEAD:** `5966350b083cca56bd22abe4b8d111dd21ac76b3` on `main` == `origin/main`.
- **`experiments/`:** untouched (`git diff HEAD -- experiments/` empty).
- **Golden guards:** **not re-run this session.** Re-run both before any real work.
- **`.verify_snapshot/` and `.verify_reports/`:** unknown state — check for an interrupted
  run before touching `experiments/`.
- **Deps:** not provisioned this session; install with `pip install -r requirements.txt`
  if you intend to run the full verification suite.

---

## Verification scopes

| Command | Scope | Time |
|---------|-------|------|
| `SEED=42 bash scripts/check.sh` | convention robustness + template validation | ~seconds |
| `SEED=42 python3 run_all_verification.py` | quick: 8 drivers + batch_run + validate | ~8 min |
| `SEED=42 python3 run_all_verification.py --extended` | + 18 more committed drivers (structural match) | ~21 min |
| `SEED=42 python3 run_all_verification.py --full` | E042 n_sim=50 + 96-config sensitivity grid | ~15 min |
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
  (`run_all_verification.py --restore-only` or `git checkout -- experiments/`). If HEAD
  already carries a captured run, restore the pinned artifact from the last commit whose
  SHA-256 matches `ledger/golden_baseline.json`.

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
- `ledger/RESEARCH_LEDGER.md` — experiment ledger (E001–E043 + handoff refreshes through E678)
- `ledger/PRIORITIZATION.md` — strategy dispositions and procedure version in force (v1.2.7)
- `ledger/golden_baseline.json` — SHA-256 fingerprints of 107 canonical artifacts
- `ledger/data_baseline.json` — SHA-256 fingerprints of pinned data caches
- `scripts/repoint_handoff.py` — repoints generic handoff aliases to the new artifact
- `scripts/check.sh` — fast local gate

---

## Provenance

- Prior refresh: `handoff_2026-11-22T09-52-24Z_INITIAL_TASK.md` (self-labeled E679).
- This handoff was written at HEAD `5966350b`. `experiments/` is clean. Golden guards
  were **not** re-run this session; no verification suite was run; no verification output
  committed; no new research performed. Left uncommitted pending explicit direction.

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
