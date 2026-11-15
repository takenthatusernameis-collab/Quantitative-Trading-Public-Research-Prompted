# Durable Handoff — Next Agentic Work Session

**Timestamp (UTC):** 2026-11-15T03:16:20Z
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** `main` @ `68a1856c` ("chore(kilo): checkpoint agent session", 2026-11-15 03:15:29 +0000); in sync with `origin/main` (0 ahead / 0 behind)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Initial task (do first)

1. **Confirm baseline integrity** (fast, offline, ~seconds)

   ```bash
   SEED=42 bash scripts/check.sh
   # or: make check
   ```

   Expect exit 0 and `=== All checks passed ===`. This was re-run and confirmed
   green for this handoff (see *Verified state* below).
   If it fails with `ModuleNotFoundError`, install dependencies
   (`pip3 install --break-system-packages -r requirements.txt`) and re-run — a
   dependency error is not a baseline failure.

2. **If checks fail for a real reason**
   - Goldens differ from HEAD → `SEED=42 python3 run_all_verification.py --restore-only`
     (or restore the artifact whose SHA-256 matches `ledger/golden_baseline.json`).
   - Active/stale verification snapshot (`.verify_snapshot/ACTIVE.json`) → recover
     with `--restore-only` before doing anything else.
   - A live verification run is *reported, not failed*; a stale snapshot is a failure.

3. **Then idle awaiting explicit user direction.**
   - Do **not** make source changes or commits unless explicitly asked.
   - Do **not** modify `experiments/*.json` goldens as a side effect of verification.
   - Do **not** re-pin baselines to silence drift (see *Known constraints*).
   - Do **not** commit `__pycache__/*.pyc` or other build artifacts.

## Verified state (live, this session)

- **Baseline integrity:** `SEED=42 bash scripts/check.sh` → **exit 0, "=== All checks passed ==="**
  (py_compile, JSON artifact parse, goldens clean vs HEAD, pinned golden-baseline match,
  data coverage, `tests/test_portfolio_opt.py`, convention robustness, template validation,
  experiment imports).
- **Working tree:** no source/data/research changes. Only tracked `__pycache__/*.pyc` build
  artifacts are modified — treat as non-canonical noise, leave uncommitted.
- **Verification snapshot:** `.verify_snapshot/` and `.verify_reports/` both absent. No
  verification run in progress, no interrupted run to recover.
- **Goldens:** 107 tracked `experiments/*.json` are the canonical baseline, unchanged.
- **Board:** empty; no peer coordination in flight.
- **Sync:** `git rev-list --left-right --count origin/main...HEAD` → `0 0`.

## Delta vs prior durable handoff

Prior artifact: `handoff_2026-11-15T03-15-08Z_INITIAL_TASK.md` (HEAD `4fe5d039`).
`git diff --name-only 4fe5d039..68a1856c` filtered to `experiments/`, `data/`, `src/`,
`scripts/`, `tests/`, `research_state/` → **0 paths**. Only checkpoint commits,
generic handoff pointers, and the ledger changed. No research substance changed.

## Known constraints (do not "fix" by re-pinning)

- **Canonical artifacts:** `experiments/*.json` are golden baselines; the suite overwrites
  then restores them. Replacing an artifact requires an explicit
  `python3 scripts/check_golden_baseline.py --update`, whose diff must justify the change.
- **Seed:** always `SEED=42`. Data/fundamentals vintages and cache coverage are enforced
  (`ledger/data_baseline.json`, `data/vintages.json`, `data/fundamentals_vintages.json`,
  `scripts/check_data_coverage.py`). Verification runs with `QUANT_RESEARCH_OFFLINE=1`,
  so a missing cache entry fails hard instead of downloading.
- **Extended drift (expected, reporting only):** 15/18 drivers reproduce with 0 differences.
  **E041** drifts with ~133 numeric diffs — 1-ulp sensitivity of an ill-conditioned QP
  (optimizer determinism already fixed per ledger E049; decision REJECTED 3/5 and every gate
  flag unchanged). It still exceeds the 1e-4 tolerance: **do not re-pin**. E029/E030 are
  offline-reproducible with pinned snapshots. See
  `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json` (gitignored) after `--extended`.
- **CI gate:** `.github/workflows/verification-gate.yml` must be created by a maintainer via
  the GitHub UI; the repo token lacks `workflows` push permission. Template at
  `.github/workflow-templates/verification-gate.yml`.

## Key commands

```bash
# Baseline integrity (required first)
SEED=42 bash scripts/check.sh

# Verification (never leave half-finished)
SEED=42 python3 run_all_verification.py              # quick   (~8 min)
SEED=42 python3 run_all_verification.py --extended   #         (~21 min)
SEED=42 python3 run_all_verification.py --full       #         (~15 min)

# Recovery / guards
SEED=42 python3 run_all_verification.py --restore-only
python3 scripts/check_golden_baseline.py
python3 scripts/check_data_coverage.py
python3 scripts/check_goldens_clean.py
```

## References

- `AGENTS.md` — project commands, baseline integrity, reproducibility rules.
- `scripts/check.sh` — convention-robustness + golden guards (steps 0.5c, 0.5d).
- `ledger/RESEARCH_LEDGER.md` — validated strategies, dispositions, open items
  (E041/E042 QP conditioning). Research phase complete (E001–E051).
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints.
- `.github/workflow-templates/verification-gate.yml` + `VERIFICATION_GATE_TEMPLATE.md`.

## Durable artifact & pointers

- Primary: `handoff_2026-11-15T03-16-20Z_INITIAL_TASK.md` (repo root).
- Mirrors: `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/`.
- Generic canonical aliases repointed via
  `python3 scripts/repoint_handoff.py handoff_2026-11-15T03-16-20Z_INITIAL_TASK.md`.
- Supersedes: `handoff_2026-11-15T03-15-08Z_INITIAL_TASK.md`.