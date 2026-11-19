# Agentic Work Session Handoff

**Timestamp (UTC)**: 2026-11-19T19:09:34Z
**Artifact**: `handoff_2026-11-19T19-09-34Z_INITIAL_TASK.md` (repo root; mirrored byte-identically to
`handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/`)
**Session ID**: Initial handoff for the next agentic work session (ledger entry E549)
**Working Directory**: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Repository state at handoff**: branch `main` at `origin/main`, HEAD
**`ac52a462faec5c441f23c8fcd8826c1bac764f3c`** (`chore(kilo): checkpoint agent session`).
Working tree clean except gitignored `__pycache__/*.pyc` churn.

---

## START HERE — ordered checklist for the next session

1. **Orient (read-only, no writes).**
   ```bash
   git log --oneline -3
   git status -sb
   ```
   Confirm HEAD and that `experiments/` is not dirty. Adopt the closed research state
   (research phase complete; E001–E051 substantive, E052–E548 handoff/conformance refreshes,
   this handoff is E549). Do **not** invent new research scope without an explicit user request.

2. **Recover any interrupted verification run (only if present).**
   ```bash
   ls -d .verify_snapshot .verify_reports 2>/dev/null
   ```
   Both were **absent** at handoff time, so nothing needed recovery. If a future session finds
   them, run `SEED=42 python3 run_all_verification.py --restore-only` before any commit.

3. **Confirm both golden guards pass** (they did at handoff; ~seconds each, no numpy needed):
   ```bash
   python3 scripts/check_goldens_clean.py      # -> ALL COMMITTED GOLDEN ARTIFACTS MATCH HEAD
   python3 scripts/check_golden_baseline.py    # -> ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT
   ```
   If either fails, fix the baseline **before** committing — never re-pin to silence a red guard.

4. **Provision dependencies before any Python/numpy step.**
   At handoff time `numpy`/`pandas`/`scipy` were **not** importable on this runner
   (`ModuleNotFoundError: No module named 'numpy'`). Run `pip install -r requirements.txt`
   before `scripts/check.sh`, the drivers, or the verification suite. (The two golden guards in
   step 3 use only the standard library and already pass without it.)

5. **Fast environment check (after deps installed).**
   ```bash
   SEED=42 bash scripts/check.sh          # or: make check   (~seconds, offline)
   ```

6. **Await explicit instruction** for any deeper work. The research program is closed; the
   default session action is verification/guard maintenance, not new experiments.

7. **Leave your own timestamped handoff** using the recurring procedure at the bottom of
   this file, and append the matching `Exxx` ledger entry.

---

## Project context

Independent, reproducible quantitative-strategy research on 2014–2026 US equities, futures and
macro data, built from free public data. Every experiment is pre-registered with explicit
falsification expectations and promotion gates; negatives are recorded honestly. Research phase
is complete (E001–E043 substantive close-out; E051 last substantive ledger entry). Surviving
validated components and all dispositions live in `ledger/RESEARCH_LEDGER.md`:

- equity TSM flagship (β-bearing), DN low-beta sort, futures TSM 18m,
  futures realized-roll-yield carry, macro momentum.
- The market-neutral total-portfolio blend line is **CLOSED** (E042 PARTIAL 4/5, G2 placebo
  z 2.11 < 3.0; E042b REJECTED 4/5). Do not re-open without an explicit user request.

## Verification scopes (all seeded `SEED=42`)

```bash
SEED=42 bash scripts/check.sh                          # ~seconds, offline; convention robustness + templates + guards
SEED=42 python3 run_all_verification.py                # verify-quick  ~8 min (8 drivers + batch_run + validate + E042 n_sim=2)
SEED=42 python3 run_all_verification.py --extended     # verify-extended ~21 min (+18 committed drivers, structural match)
SEED=42 python3 run_all_verification.py --full         # verify-full  ~15 min (E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 python3 run_all_verification.py --skip-slow    # convention-only
SEED=42 python3 run_all_verification.py --restore-only # recover goldens after an interrupted run
```

## Integrity rules (do not violate)

- **Goldens are canonical.** `experiments/*.json` are committed research artifacts, pinned by
  SHA-256 in `ledger/golden_baseline.json`. The verification suite backs them up to the
  repo-local gitignored `.verify_snapshot/` (with `ACTIVE.json` owner pid) and restores them.
  Never commit verification output; never re-pin baselines as a side effect of a run.
- **Data inputs are pinned.** `scripts/check_data_coverage.py` statically resolves every
  `data.download()` call site and requires each cache file to be git-tracked and SHA-256-pinned in
  `ledger/data_baseline.json`. Verification re-runs drivers with `QUANT_RESEARCH_OFFLINE=1`.
- **Optimizer contract.** `src/portfolio_opt.py` validates solver answers on the problem's
  constraints, not on the solver's exit status (ledger E049); pinned by `tests/test_portfolio_opt.py`.
- **Known accepted drift (reporting only).** E041 exhibits 29–133 numeric diffs from 1-ulp
  sensitivity of an ill-conditioned QP. Do **not** re-pin it to silence the extended report.
- **Commits.** Only commit when the user explicitly asks. Prior handoff sessions deliberately
  left the artifact uncommitted pending explicit direction; the controller makes checkpoint
  commits.

## Key references

- `AGENTS.md` — project commands & conventions (authoritative).
- `ledger/RESEARCH_LEDGER.md` — every experiment, disposition, and standing rule.
- `ledger/PRIORITIZATION.md` — ranking procedure (v1.2.0–v1.2.7 standing rules).
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned SHA-256 fingerprints.
- `scripts/check.sh`, `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`,
  `scripts/check_data_coverage.py`, `scripts/repoint_handoff.py`, `run_all_verification.py`.

## Open items

No actionable open items. Standing "do not touch" notes: E041 numeric drift is expected and
must not be re-pinned; the market-neutral blend line is closed; the CI workflow
(`.github/workflows/verification-gate.yml`) cannot be created by automated agents — a maintainer
must add it from `.github/workflow-templates/verification-gate.yml`.

## Recurring durable-handoff procedure (for the next session)

1. Write `handoff_<UTC ISO timestamp with `:` -> `-`>_INITIAL_TASK.md` at the repo root, with a
   timestamped ordered start-here checklist and the verified HEAD.
2. Mirror it byte-identically into `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/`;
   verify all six copies share one SHA-256.
3. Repoint the generic canonical pointers:
   `python3 scripts/repoint_handoff.py handoff_<new>.md` (expect ~490 pointers, 0 bad).
4. Append the next `E###: Durable Handoff Refresh — Clear Initial Task Message (HEAD <short>)`
   ledger entry with the artifact name, SHA-256, repoint audit, provenance (supersedes), and
   constraints honored.

(End of handoff)
