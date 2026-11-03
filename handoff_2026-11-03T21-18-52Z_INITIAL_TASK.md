# HANDOFF — 2026-11-03T21-18-52Z

## Repo state (snapshot)
- **Project:** Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data.
- **Status:** Research phase complete (E001–E043). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.
- **Canonical artifacts:** `experiments/*.json` are the golden baselines. The verification suite backs them up to repo-local gitignored `.verify_snapshot/` (with `ACTIVE.json` holding the owning PID) and restores them afterward — **never leave a verification run half-finished**.
- **Guards in place:** `scripts/check_goldens_clean.py` (working tree vs HEAD), `scripts/check_golden_baseline.py` (committed artifacts vs SHA-256 pins in `ledger/golden_baseline.json`), `scripts/check_data_coverage.py` (all `data.download()` call sites must have git-tracked pinned caches in `ledger/data_baseline.json`).
- **Data:** Cached parquet in `data/` (gitignored except pinned vintages in `data/vintages.json` and `data/fundamentals_vintages.json` with snapshots in `data/fundamentals/`). Runs must be offline-reproducible (`QUANT_RESEARCH_OFFLINE=1`).
- **Known quirks:** Optimizer determinism (E049) — SLSQP status 8 acceptable if feasible/optimal; ill-conditioned QPs can cause numeric drift in E041/E042 grids (do **not** re-pin to silence). Some extended drivers (E030/E029) have pinned inputs/snapshots for reproducibility.

## Initial task for the next session
**Primary objective:** Verify repository integrity and establish a clean baseline before making any changes.

### Concrete steps (in order)
1. **Check git state**
   `git status --short` — ensure no unexpected modifications to `experiments/`, `ledger/`, or `data/`. If `experiments/` differ from HEAD, restore first.
2. **Run fast integrity check**
   `SEED=42 bash scripts/check.sh` (convention-robustness, template validation, py_compile, golden/data coverage checks). Fast and catches most issues.
3. **Run quick verification (recommended)**
   `SEED=42 python3 run_all_verification.py` (or `make verify-quick`). If interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`).
4. **Review results**
   - If all checks pass: repo is clean and reproducible. Proceed with the user's next requested change.
   - If failures occur: follow `AGENTS.md` guardrails. Do **not** re-pin goldens/data as a side effect of verification. Only re-pin via explicit scripts (`scripts/check_golden_baseline.py --update`, `scripts/check_data_coverage.py --update`) with clear justification.

## Constraints & guardrails
- **Always use `SEED=42`** for verification/runs.
- **Never commit verification output.** If a run leaves modified `experiments/` files, restore before committing.
- **Golden baseline is authoritative.** Replacing artifacts requires explicit re-pinning and will show up in the diff.
- **Offline by default in verification.** Missing pinned caches must fail hard (do not rely on live downloads).
- **CI workflow:** Cannot be created by agents. Template at `.github/workflow-templates/verification-gate.yml`, instructions in `VERIFICATION_GATE_TEMPLATE.md`.
- **Discipline:** Follow pre-registration, multiple-testing ("reported, not gated"), and negative-result recording if adding experiments.

## Key pointers
- **Ledger:** `ledger/RESEARCH_LEDGER.md`
- **Golden pin:** `ledger/golden_baseline.json`
- **Data pin:** `ledger/data_baseline.json`
- **Verification:** `run_all_verification.py`, `scripts/check.sh`, `make verify-quick/extended/full`
- **Conventions:** `AGENTS.md`
- **Project config:** `kilo.json`

**Ready to start at step 1.**
