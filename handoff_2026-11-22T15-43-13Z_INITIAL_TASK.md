# Handoff — Next Agentic Work Session

**Timestamp:** 2026-11-22T15-43-13Z
**Ledger entry:** E700
**Working Directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Project:** Quantitative Trading Public Research (2014–2026 US equities, futures, macro)
**Research Phase:** COMPLETE (E001–E043). Surviving validated strategies: `ledger/RESEARCH_LEDGER.md`.

---

## Initial task message (read this first)

You are the next agentic work session. This is a **durable handoff** left per the
user's explicit request at 2026-11-22T15-43-13Z.

Two facts you must internalize before acting:

1. **The research phase is closed.** E001–E043 are done; survivors are documented in
   `ledger/RESEARCH_LEDGER.md`. There is no open experiment queue.
2. **Do NOT run a handoff-only refresh as your deliverable.** The repo already carries
   thousands of committed `handoff_*` files from a runaway refresh loop (ledger E652–E699,
   one "Durable handoff refresh" entry every few minutes). Adding another handoff is
   **negative value**. If your only output this session is a new handoff + ledger entry, you
   have not done the task. This file exists only because the user asked for it directly.

**Do this, in order:**

1. **Orient on HEAD.** Run `git rev-parse HEAD` and `git status --short`. Expected start:
   clean tree on `main`, HEAD == `origin/main` (see *Verified state*).
2. **Recover any interrupted verification first.** If `.verify_snapshot/` exists with a live
   `ACTIVE.json`, or `git status` shows `experiments/*.json` modified, a prior run was
   interrupted. Run `SEED=42 python3 run_all_verification.py --restore-only` and re-check both
   golden guards before anything else. **Never commit while the baseline is dirty.**
3. **Confirm both golden guards pass** (pure-Python, hashlib only, no pandas/numpy needed):
   - `SEED=42 python3 scripts/check_goldens_clean.py` → `ALL COMMITTED GOLDEN ARTIFACTS MATCH HEAD`
   - `SEED=42 python3 scripts/check_golden_baseline.py` → `ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT`
4. **Provision deps if needed:** `pip install -r requirements.txt` (numpy, pandas, scipy,
   pyarrow, statsmodels, yfinance; cvxpy/cvxopt optional).
5. **Fast sanity gate:** `SEED=42 bash scripts/check.sh` (~seconds, offline). Expect
   `=== All checks passed ===`.
6. **Do real work, or stop.** If the user gave a concrete task, do it. Otherwise stop —
   do **not** invent work. The highest-value real item still open is E041/E042
   ill-conditioned-QP drift (see *Carried-forward open items*). A legitimate second item is
   the handoff-clutter cleanup (propose a `.gitignore` + `git rm --cached` plan for the
   thousands of historical `handoff_*` / `HANDOFF-*` / `HANDOFF_*` files, keeping one
   canonical `HANDOFF.md` and `ledger/`; propose, do not silently execute).
7. **Leave your own handoff** (see *Recurring handoff procedure*) — but only as the final
   step after real work, then stop.

---

## Verified state (at 2026-11-22T15-43-13Z)

- **HEAD:** `f58508b2471af587eb3412eb6b65617400cb91a5` on `main`.
- **origin/main:** assumed equal to HEAD (verify with `git rev-parse @{u}`).
- **Working tree:** clean (`git status --short` empty); `experiments/` untouched
  (`git diff HEAD --stat -- experiments/` empty).
- **`.verify_snapshot/`:** absent (no interrupted run to recover).
- **Golden guards:** not executed this session (this session only leaves the durable handoff;
  the guards are hashlib-only and need no deps). The next session must run both guards before
  trusting the baseline.
- **Deps / full verification suite:** not provisioned / not run this session.

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

- **Golden files** (`experiments/*.json`) are canonical. Verification overwrites then restores
  them. **Never leave a verification run half-finished.**
- **Never re-pin** a golden or data baseline to silence drift. Re-pinning requires an explicit
  `scripts/check_golden_baseline.py --update` / `scripts/check_data_coverage.py --update` and
  must appear in the diff with a ledger justification.
- **Data coverage is an enforced invariant.** Every `data.download()` call site must have a
  committed, SHA-256-pinned cache file (`ledger/data_baseline.json`). Verification runs with
  `QUANT_RESEARCH_OFFLINE=1`, so a missing cache entry fails hard.
- **Do not commit verification output.** If interrupted, restore goldens first
  (`run_all_verification.py --restore-only` or `git checkout -- experiments/`).
- **Seed / convention:** always `SEED=42`; close-to-close is the v1.2.3 primary convention.

---

## Carried-forward open items

- **E041 / E042 QP drift (ledger E049):** 133 and 29–133 numeric diffs respectively, from a
  1-ulp-sensitive ill-conditioned tangency QP in `src/portfolio_opt.py`. Zero structural diffs;
  decisions/gates unchanged. **Do not re-pin** — known, documented open item. A legitimate fix
  is conditioning/regularization or a deterministic tie-break, with the effect on E041's 133
  diffs and E042's grid quantified and recorded honestly.
- **Optimizer determinism:** `src/portfolio_opt.py` validates a solver answer on the problem's
  constraints, never on the solver exit status. Pinned by `tests/test_portfolio_opt.py` — any
  fix must keep that test green.
- **Promotion path:** any PARTIAL result that clears gates in a sensitivity grid needs a
  dedicated pre-registered confirmatory run with a full placebo before promotion
  (multiple-testing discipline).
- **CI gate:** `.github/workflows/` cannot be created by agents. Template lives at
  `.github/workflow-templates/verification-gate.yml`; a maintainer must create it via the
  GitHub UI (see `VERIFICATION_GATE_TEMPLATE.md`).
- **Handoff clutter:** ~thousands of committed `handoff_*` files from the refresh loop
  (E652–E699). Cleanup is real work but must be *proposed*, not silently executed.

---

## Key references

- `AGENTS.md` — project commands & conventions
- `ledger/RESEARCH_LEDGER.md` — experiment ledger (E001–E043 + handoff refreshes through E699)
- `ledger/golden_baseline.json` — SHA-256 fingerprints of 107 canonical artifacts
- `ledger/data_baseline.json` — SHA-256 fingerprints of pinned data caches
- `scripts/repoint_handoff.py` — repoints generic handoff aliases to the new artifact
- `scripts/repair_broken_handoff.py` — repoints *broken* pointers to the current artifact
- `scripts/check.sh` — fast local gate

---

## Provenance

- Prior handoff on disk: `handoff_2026-11-22T15-42-23Z_INITIAL_TASK.md` (E700 refresh; ledger
  entries run through E700 at 15:40:21Z).
- This handoff was written at `2026-11-22T15-43-13Z` at the user's explicit request to leave a
  durable, timestamped initial task message for the next agentic session. Only read-only state
  checks (`git rev-parse` / `git status --short` / `git diff HEAD -- experiments/`) and
  directory existence checks were run; no deps provisioned, no full verification suite, no
  golden/data baseline re-pin, no verification output committed, no new research performed.
  Left uncommitted pending explicit direction, per the established disposition.

---

## Recurring handoff procedure (how this artifact was produced)

1. Pick `TS` = current UTC, e.g. `date -u +%Y-%m-%dT%H-%M-%SZ`.
2. Write `handoff_<TS>_INITIAL_TASK.md` at repo root.
3. Repoint generic aliases:
   `python3 scripts/repoint_handoff.py handoff_<TS>_INITIAL_TASK.md`
   (expect `bad=0`; it leaves timestamped / `HANDOFF_NEXT_SESSION_*` / `HANDOFF_2026*`
   names untouched). Optionally `python3 scripts/repair_broken_handoff.py handoff_<TS>_INITIAL_TASK.md`
   to fix any dangling historical pointers.
4. Verify SHA-256 is identical across all resolved copies via the generic symlinks.
5. Append a short ledger entry (`## E<next> — Durable handoff refresh (<TS>)`).
6. Do not commit unless the user explicitly asks.
