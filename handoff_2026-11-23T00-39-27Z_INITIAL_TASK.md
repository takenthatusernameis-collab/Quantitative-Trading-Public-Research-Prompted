# Agentic Work Session Handoff

**Timestamp**: 2026-11-23T00:39:27Z
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Project**: Quantitative Trading Public Research (2014–2026 US equities, futures, macro)
**HEAD**: `d8d806f661aa98dff793cca0ab8aea305c13aa99` on `main` (== `origin/main`)

---

## Initial Task (read this first)

You are the next agentic work session. This project's **research phase is
complete (E001–E043)**; surviving validated strategies are documented in
`ledger/RESEARCH_LEDGER.md`.

**Do NOT repeat this handoff refresh as your deliverable.** Entries E652–E716
in the ledger are a runaway loop of handoff-only refreshes — sessions that only
rewrite this file instead of doing real work. That loop has produced **8,152
git-tracked handoff files** and keeps growing. Adding another refresh (this one,
E717) is acceptable only because the user explicitly asked for a durable
handoff. Your job is to break the loop, not extend it.

Pick ONE of the following and actually do it, then stop:

1. **Verify-and-stop (cheapest, always valid).** Run the fast guard + real
   suite below. If everything passes, report PASS and stop. Do not write a new
   handoff unless you made a change.
2. **Provision deps + run the real verification suite.** `pip install -r
   requirements.txt`, then `SEED=42 python3 run_all_verification.py`. This is
   the first time in many sessions the real suite will have been exercised.
   Report any drift precisely.
3. **Address the open E049 item**: the E041/E042 ill-conditioned tangency-QP
   artifacts drift by 29–133 differences beyond the 1e-4 tolerance. Do **not**
   re-pin them to silence it. Investigate the conditioning or document the
   bound. (See ledger E049 and AGENTS.md "Optimizer determinism".)
4. **Explicitly-requested pre-registered research only.** Goalposts are never
   moved post-hoc; grids are "reported, not gated."
5. **If none of the above is possible**, do not silently refresh again —
   instead **propose** (do not execute) a `.gitignore` + `git rm --cached`
   cleanup of the historical handoff clutter and surface it to the user.

If you truly have no instruction beyond "leave a handoff", say so plainly and
stop; do not manufacture work.

---

## Verified state (this session, 2026-11-23T00:39:27Z)

- HEAD `d8d806f661aa98dff793cca0ab8aea305c13aa99` on `main`;
  `git rev-list --left-right --count origin/main...HEAD` = `0  0`.
- `git diff HEAD -- experiments/` empty (canonical goldens untouched).
- `.verify_snapshot/` and `.verify_reports/` absent (no interrupted run).
- `git status --short` shows only `__pycache__/*.pyc` noise (no source change).
- **Both pure-Python golden guards PASS this session**:
  - `scripts/check_goldens_clean.py` -> ALL COMMITTED GOLDEN ARTIFACTS MATCH HEAD (exit 0)
  - `scripts/check_golden_baseline.py` -> ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT (exit 0)
- Deps **not** provisioned (guards are hashlib-only); full verification suite
  **not** run this session.

## Start-here checklist (ordered)

1. Orient on HEAD: `git rev-parse HEAD`, `git status --short`,
   `git diff HEAD -- experiments/`.
2. Recover any interrupted verification: `SEED=42 python3 run_all_verification.py --restore-only`
   (or `git checkout -- experiments/` only if HEAD is not a captured run).
3. Confirm both golden guards: `python3 scripts/check_goldens_clean.py` then
   `python3 scripts/check_golden_baseline.py`.
4. Provision deps if running the suite: `pip install -r requirements.txt`.
5. Run `SEED=42 bash scripts/check.sh` (fast, offline, seconds).
6. Do the user task from the "Initial Task" section — or stop if verified clean.
7. Leave your own handoff ONLY if you made a real change.

## Key commands

```bash
SEED=42 bash scripts/check.sh                              # fast convention + template validation
SEED=42 python3 run_all_verification.py                    # quick full (~8 min; 8 drivers)
SEED=42 python3 run_all_verification.py --extended         # + 18 committed drivers (~21 min)
SEED=42 python3 run_all_verification.py --full             # E042 n_sim=50 + 96-config grid
SEED=42 python3 run_all_verification.py --restore-only     # recover goldens after interruption
python3 -m py_compile <changed_file>.py                    # compile check on changed files
```

## Integrity rules (do not violate)

- `experiments/*.json` are canonical; never commit verification output over them.
- Always `SEED=42`.
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` to
  silence drift; replacing an artifact requires a deliberate, reviewed re-pin.
- Every `data.download()` call site needs a git-tracked cache matching
  `ledger/data_baseline.json`; the suite runs with `QUANT_RESEARCH_OFFLINE=1`.
- Do not commit unless the user explicitly asks.

## Key references

- `ledger/RESEARCH_LEDGER.md` — surviving strategies, open items (E045, E048, E049).
- `ledger/golden_baseline.json` — pinned artifact fingerprints (107 artifacts).
- `ledger/data_baseline.json` — pinned data-cache fingerprints.
- `AGENTS.md` — full commands, conventions, baseline-integrity rules.
- `src/portfolio_opt.py` + `tests/test_portfolio_opt.py` — optimizer determinism (E049).

## Provenance

- This handoff (E717) was written at the user's explicit request to leave a
  timestamped, durable initial task message for the next agentic work session.
- Canonical artifact:
  `handoff_2026-11-23T00-39-27Z_INITIAL_TASK.md` (repo root + five mirror dirs
  `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/` via repointed
  generic symlinks; see `scripts/repoint_handoff.py`).
- No golden/data baseline re-pinned, no verification suite run, no verification
  output committed, no new research performed, no commit made.

## Recurring handoff procedure (for when a refresh is genuinely warranted)

1. Write `handoff_<UTC timestamp with T..Z>.md` in the repo root.
2. `python3 scripts/repoint_handoff.py handoff_<timestamp>.md` (pass the filename
   explicitly — a bare invocation resets aliases to the old default).
3. `python3 scripts/repair_broken_handoff.py handoff_<timestamp>.md` if any
   historical pointer is broken.
4. Verify: generic pointers resolve, `checked=N bad=0`, single SHA-256 across copies.

---

*This handoff was created at 2026-11-23T00:39:27Z. Research phase remains closed
(E001–E043). Do not turn handoff refreshes into the work.*