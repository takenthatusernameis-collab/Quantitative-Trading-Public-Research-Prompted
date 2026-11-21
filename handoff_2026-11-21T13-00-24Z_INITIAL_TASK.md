# Durable Handoff — Initial Task for the Next Agentic Work Session

**Timestamp (UTC):** 2026-11-21T13:00:24Z
**Artifact:** `handoff_2026-11-21T13-00-24Z_INITIAL_TASK.md`
(mirrored byte-identically into `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/`)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Branch:** `main`, HEAD **`b34ffbc8f03c52a392640038261c1d112e8f091b`** == `origin/main` (in sync)
**Working tree:** clean (`git status -sb` empty); `git diff HEAD -- experiments/` empty.

---

## 1. Initial task (do this first, in order)

The research program is **CLOSED** (E001–E043 substantive; all later entries are handoff /
conformance refreshes). The default job of the next session is to **orient, verify integrity, and
await explicit instruction** — not to start new research. Execute this checklist before anything else:

1. **Orient (read-only).**
   ```bash
   git log --oneline -3
   git status -sb
   ```
   Confirm HEAD is `b34ffbc8` on `main` and that `experiments/` is not dirty. Do not commit,
   branch, or modify anything in this step.

2. **Recover an interrupted verification run, only if one exists.**
   ```bash
   ls -d .verify_snapshot .verify_reports 2>/dev/null
   ```
   Both are **absent** at handoff time, so no recovery is needed. If a future session finds either,
   run `SEED=42 python3 run_all_verification.py --restore-only` **before** any commit. Never leave
   `experiments/` holding driver output instead of the golden baselines.

3. **Confirm both golden guards pass** (they did at handoff; seconds each, no numpy needed).
   ```bash
   python3 scripts/check_goldens_clean.py      # -> ALL COMMITTED GOLDEN ARTIFACTS MATCH HEAD
   python3 scripts/check_golden_baseline.py    # -> ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT
   ```
   If either fails, fix the baseline **before** committing. Never re-pin to silence a red guard.

4. **Provision dependencies before any Python/numpy step.** `numpy`/`pandas`/`scipy` are **not**
   importable on this runner at handoff time (`ModuleNotFoundError: No module named 'numpy'`):
   ```bash
   pip install -r requirements.txt
   ```

5. **Run the fast convention-robustness check (after deps).**
   ```bash
   SEED=42 bash scripts/check.sh          # or: make check   (~seconds, offline)
   ```

6. **Await explicit instruction** for any deeper work. Do not invent research scope, re-open a
   closed strategy, re-pin a golden, or run the full verification suite without a user request.

7. **Leave your own timestamped handoff** using the procedure in section 6, and append the matching
   `Exxx` ledger entry (next is **E644**).

---

## 2. Project state

- Independent, reproducible quantitative-strategy research on 2014–2026 US equities, futures and
  macro data from free public data. Every experiment is pre-registered with falsification
  expectations and promotion gates; negatives are recorded honestly (REJECTED / PARTIAL).
- **Research phase complete (E001–E043).** Surviving validated strategies are documented in
  `ledger/RESEARCH_LEDGER.md` (equity TSM flagship, DN low-beta sort, futures TSM 18m, futures
  realized-roll-yield carry, macro momentum).
- The market-neutral total-portfolio blend line is **CLOSED** (E042 PARTIAL 4/5, G2 placebo
  z 2.11 < 3.0; E042b REJECTED 4/5). Do not re-open without an explicit user request.
- Canonical artifacts: `experiments/*.json` (107 tracked goldens), pinned in
  `ledger/golden_baseline.json`. Data cache SHA-256s pinned in `ledger/data_baseline.json`.

---

## 3. Verification scopes (all seeded `SEED=42`)

```bash
SEED=42 bash scripts/check.sh                          # ~seconds, offline; convention robustness + guards
SEED=42 python3 run_all_verification.py                # verify-quick  ~8 min (8 drivers + batch_run + validate + E042 n_sim=2)
SEED=42 python3 run_all_verification.py --extended     # verify-extended ~21 min (+18 committed drivers, structural match)
SEED=42 python3 run_all_verification.py --full         # verify-full  ~15 min (E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --skip-slow    # convention-only
SEED=42 python3 run_all_verification.py --restore-only # recover goldens after an interrupted run
```

## 4. Integrity rules (do not violate)

- Never commit verification output into `experiments/`; restore via `--restore-only`.
- Verification always runs with `QUANT_RESEARCH_OFFLINE=1`; an unpinned input fails hard instead of
  silently downloading (yfinance is not bit-reproducible).
- Always use `SEED=42` (walk-forward + placebo RNG).
- Do **not** re-pin goldens to silence the known E041/E042 optimizer drift (ill-conditioned QP;
  1-ulp sensitivity). See AGENTS.md "Optimizer determinism (ledger E049)".
- Golden baseline is the authoritative record, not the latest re-run. Re-pin only to intentionally
  replace an artifact, and always land that in the diff.
- Never commit unless the user explicitly asks.

## 5. Key references

- `AGENTS.md` — commands, conventions, baseline-integrity rules (read before running the suite).
- `ledger/RESEARCH_LEDGER.md` — full experiment record and dispositions (latest entry E643).
- `ledger/golden_baseline.json`, `ledger/data_baseline.json`, `data/fundamentals_vintages.json`.
- `src/batch_run.py`, `src/validate.py`, `src/portfolio_opt.py`, `experiments/run_e*.py`.
- `scripts/check.sh`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`,
  `scripts/repoint_handoff.py`, `scripts/repair_broken_handoff.py`.

## 6. Recurring handoff procedure (leave one each session)

1. Orient and verify as in section 1; record live HEAD, sync status, guard results.
2. Write `handoff_<UTC-timestamp>_INITIAL_TASK.md` at the repo root with an ordered start-here
   checklist, verification scopes, integrity rules, key references, and the explicit initial task.
3. Mirror it byte-identically (same SHA-256) into `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`,
   `.kilo/handoff/`.
4. Repoint generic aliases:
   ```bash
   python3 scripts/repoint_handoff.py handoff_<UTC-timestamp>_INITIAL_TASK.md
   python3 scripts/repair_broken_handoff.py
   ```
5. Append the matching `Exxx` entry to `ledger/RESEARCH_LEDGER.md` recording artifact name, mirror
   SHA-256, HEAD/sync state, and guard results. Leave changes uncommitted pending explicit direction.

## 7. State verified this session

- HEAD `b34ffbc8f03c52a392640038261c1d112e8f091b` on `main` == `origin/main` (in sync).
- Working tree clean before this handoff was written (`git status -sb` empty).
- `git diff HEAD -- experiments/` empty (no driver output contaminating the goldens).
- No `.verify_snapshot/` or `.verify_reports/` pending (no active/interrupted verification run).
- Both golden guards pass:
  - `python3 scripts/check_goldens_clean.py` -> "ALL COMMITTED GOLDEN ARTIFACTS MATCH HEAD"
  - `python3 scripts/check_golden_baseline.py` -> "ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT"
- This session created this durable handoff only. No code, experiments, baselines, or canonical
  artifacts were modified. No commit made (left uncommitted pending explicit direction).

## 8. Handoff provenance

- **Durable artifact (this session):** `handoff_2026-11-21T13-00-24Z_INITIAL_TASK.md` (repo root,
  plus five byte-identical mirrors above).
- Supersedes `handoff_2026-11-21T12-57-24Z_INITIAL_TASK.md` only as the current durable artifact;
  earlier handoff history is retained.
- This session created this durable handoff only. No code, experiments, baselines, or canonical
  artifacts were modified.