# HANDOFF — 2026-11-03T21:16:49Z

## Repo state (snapshot)
- **Project:** Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data.
- **Git HEAD:** 60ea6eb chore(kilo): checkpoint agent session
- **Branch:** main
- **Working tree:** CLEAN (nothing to commit)
- **Status:** Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- **Canonical artifacts:** `experiments/*.json` are golden baselines. Verification suite backs them up to repo-local gitignored `.verify_snapshot/` (PID in `ACTIVE.json`) and restores afterward — never leave a run half-finished.
- **Guards:** `scripts/check_goldens_clean.py` (working tree vs HEAD), `scripts/check_golden_baseline.py` (committed artifacts vs SHA-256 pins in `ledger/golden_baseline.json`), `scripts/check_data_coverage.py` (all `data.download()` call sites must have git-tracked pinned caches in `ledger/data_baseline.json`).
- **Data:** Cached parquet in `data/` (gitignored except pinned vintages in `data/vintages.json` and `data/fundamentals_vintages.json` with snapshots in `data/fundamentals/`). Runs must be offline-reproducible (`QUANT_RESEARCH_OFFLINE=1`).
- **Known quirks:** Optimizer determinism (E049) — SLSQP status 8 acceptable if feasible/optimal; ill-conditioned QPs can cause numeric drift in E041/E042 grids (do **not** re-pin to silence). E030/E029 now reproduce via pinned caches/snapshots.

## Initial task for the next session
**Primary objective:** Confirm baseline integrity before making any changes; then proceed with the user's requested work.

### Concrete steps (in order)
1. **Check git state:** `git status --short` — ensure no unexpected modifications to `experiments/`, `ledger/`, or `data/`. If `experiments/` differ from HEAD, restore first (`git checkout -- experiments/` or `SEED=42 python3 run_all_verification.py --restore-only`).
2. **Run fast integrity check:** `SEED=42 bash scripts/check.sh` — runs convention-robustness, template validation, py_compile, golden/data coverage checks. Expect exit 0 with `=== All checks passed ===`.
3. **Run quick verification (recommended):** `SEED=42 python3 run_all_verification.py` (or `make verify-quick`). Recover interrupted runs with `--restore-only`.
4. **Review results:** If all pass, repo is clean/reproducible — proceed with requested change. If failures occur, follow `AGENTS.md` guardrails; do **not** re-pin goldens/data as a side effect of verification.

## Constraints & guardrails
- Always use `SEED=42` for verification/runs.
- Never commit verification output. Restore goldens before committing if a run left modifications.
- Golden baseline is authoritative. Replacing artifacts requires explicit re-pinning and shows up in the diff.
- Offline by default in verification. Missing pinned caches must fail hard (do not rely on live downloads).
- CI workflow cannot be created by agents; template at `.github/workflow-templates/verification-gate.yml`, instructions in `VERIFICATION_GATE_TEMPLATE.md`.
- Follow pre-registration, multiple-testing ("reported, not gated"), and negative-result recording if adding experiments.

## Key pointers
- Ledger: `ledger/RESEARCH_LEDGER.md`
- Golden pin: `ledger/golden_baseline.json`
- Data pin: `ledger/data_baseline.json`
- Verification: `run_all_verification.py`, `scripts/check.sh`, `make verify-quick/extended/full`
- Conventions: `AGENTS.md`
- Project config: `kilo.json`

**Ready to start at step 1.**
