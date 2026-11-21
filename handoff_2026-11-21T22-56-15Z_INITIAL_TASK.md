# HANDOFF — Initial Task Message for the Next Agentic Work Session

**Timestamp (UTC):** 2026-11-21T22:56:15Z
**Created by:** previous agentic work session (Kilo)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

---

## 1. What this file is

A durable, timestamped initial-task message for the next agentic session on this
repository. It records the verified repository state and the recommended first
task, so the next session can start without re-deriving context.

> Repo hygiene note: this repository already carries a large number of committed
> `handoff_*_INITIAL_TASK.md` files and alias symlinks. That is unintentional
> runaway output from prior sessions, not a real deliverable. This single file
> is the authoritative handoff; repoint the aliases rather than spawning more.

---

## 2. Repo state (snapshot, verified at 22:56:15Z)

- **Project:** Independent reproducible quantitative-strategy research on
  2014–2026 US equities, futures, and macro data (see `AGENTS.md`).
- **Phase:** Research phase complete — experiments E001–E043. Surviving validated
  strategies are in `ledger/RESEARCH_LEDGER.md`.
- **Canonical artifacts:** `experiments/*.json` (107 files) are the golden
  baselines. Verification backs them up to the gitignored `.verify_snapshot/`
  (with `ACTIVE.json` holding the owning PID) and restores them afterward.
- **Git:** HEAD = `32bf98de` (`chore(kilo): checkpoint agent session`); working
  tree clean (`git status --short` empty). No `.verify_snapshot/` present → no
  interrupted verification run to recover.
- **Guards:** `scripts/check_goldens_clean.py` (tree vs HEAD),
  `scripts/check_golden_baseline.py` (committed artifacts vs SHA-256 pins in
  `ledger/golden_baseline.json`),
  `scripts/check_data_coverage.py` (every `data.download()` site must have a
  git-tracked pinned cache in `ledger/data_baseline.json`).
- **Data:** Cached parquet in `data/` (gitignored except pinned vintages in
  `data/vintages.json` and `data/fundamentals_vintages.json`, snapshots in
  `data/fundamentals/`). Runs must be offline-reproducible
  (`QUANT_RESEARCH_OFFLINE=1`).
- **Known quirks (do not "fix" by re-pinning):** Optimizer determinism (ledger
  E049) — validate on problem constraints, not SLSQP exit status; ill-conditioned
  QPs can drift numerically in E041/E042 grids. E029/E030 inputs/snapshots are
  pinned for reproducibility. The committed golden is the authoritative record.

---

## 3. Initial task for the next session (recommended first actions, in order)

**Primary objective:** Confirm repository integrity and establish a clean,
reproducible baseline *before* making any change. Do not modify research
artifacts without explicit user direction.

1. **Check git state**
   ```bash
   git status --short
   git log -1 --format='%H %s'
   ```
   Confirm no unexpected modifications to `experiments/`, `ledger/`, or `data/`.
   If `experiments/` differs from HEAD, restore first
   (`git checkout -- experiments/`, or re-run with `--restore-only`).

2. **Run the fast integrity check**
   ```bash
   SEED=42 bash scripts/check.sh        # or: make check
   ```
   Covers the JSON-artifact guard, goldens-clean, golden-baseline SHA-256 pins,
   data coverage, portfolio-opt unit test, convention robustness, template
   validation, and experiment-import checks. Fast; catches most issues.

3. **Run quick verification (recommended)**
   ```bash
   SEED=42 python3 run_all_verification.py        # or: make verify-quick
   ```
   If interrupted, recover with
   `SEED=42 python3 run_all_verification.py --restore-only`.

4. **Review and stop**
   - All green → repo is clean and reproducible. **Await the user's next
     requested change.**
   - Failures → follow `AGENTS.md` guardrails. Do **not** re-pin goldens or data
     as a side effect of verification. Only re-pin via explicit scripts
     (`scripts/check_golden_baseline.py --update`,
     `scripts/check_data_coverage.py --update`) with clear justification in the diff.

---

## 4. Constraints & guardrails (from AGENTS.md)

- **Always use `SEED=42`** for verification/runs. Close-to-close is the v1.2.3
  primary convention (overnight decomposition reported alongside).
- **Never commit verification output.** If a run leaves modified `experiments/`
  files, restore before committing. Never leave a verification run half-finished.
- **Golden baseline is authoritative.** Replacing artifacts requires explicit
  re-pinning and shows up in the diff. Never re-pin to silence drift.
- **Offline by default in verification.** Missing pinned caches must fail hard —
  do not rely on live downloads (yfinance is not bit-reproducible).
- **CI workflow cannot be created by agents.** Template at
  `.github/workflow-templates/verification-gate.yml`, instructions in
  `VERIFICATION_GATE_TEMPLATE.md`. Use local `make check` / `make verify*` instead.
- **Research discipline:** pre-registration with falsification expectations;
  sensitivity grids are "reported, not gated"; record negative results honestly.

---

## 5. Key pointers

- Conventions & commands: `AGENTS.md`
- Research ledger: `ledger/RESEARCH_LEDGER.md`
- Prioritization procedure: `ledger/PRIORITIZATION.md`
- Golden pins: `ledger/golden_baseline.json`
- Data pins: `ledger/data_baseline.json`
- Verification: `run_all_verification.py`, `scripts/check.sh`,
  `make verify-quick` / `verify-extended` / `verify-full`
- Project config: `kilo.json`

---

**Status:** No code changes were made by this session. No verification was run
(working tree was already clean). This file is the durable initial-task handoff —
start at section 3, step 1. Aliases `handoff_CURRENT`, `handoff_LATEST`,
`handoff_NEXT`, `handoff_NEXT_SESSION`, and friends now repoint here.
