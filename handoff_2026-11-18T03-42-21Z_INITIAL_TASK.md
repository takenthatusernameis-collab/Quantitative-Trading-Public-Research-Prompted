# Durable Handoff — Initial Task Message (Next Agentic Work Session)

**Timestamp (UTC):** 2026-11-18T03-42-21Z
**HEAD:** `d6624046` (main, 2026-11-18T03:41:40Z) `chore(kilo): checkpoint agent session`
**Branch:** `main` (in sync with `origin/main`)
**Supersedes:** `handoff_2026-11-18T03-40-45Z_INITIAL_TASK.md`

## Repository state (at capture)

- **Research phase:** COMPLETE. Experiments E001–E051 are recorded in `ledger/RESEARCH_LEDGER.md`; ledger tail through E112 consists of durable-handoff/closure refreshes only. No new research in progress.
- **Working tree:** source-clean except 12 modified tracked `__pycache__/*.pyc` files under `scripts/__pycache__/`, `src/__pycache__/`, `tests/__pycache__/` (build artifacts). Do **not** stage or commit them.
- **Golden artifacts:** tracked `experiments/`, `data/`, `ledger/`, `scripts/`, `src/`, `tests/` sources unchanged vs HEAD (no golden/data/ledger drift indicated).
- **Verification state:** no `.verify_snapshot/` and no `.verify_reports/` present; no interrupted verification run to recover.

## Canonical invariants (do not violate)

- Treat `experiments/*.json` as canonical goldens. Verification overwrites during runs and restores afterward — never leave a run half-finished.
- If interrupted or on golden/baseline mismatch: `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/` only when HEAD still holds the pinned baseline). See `AGENTS.md` "Baseline Integrity".
- Re-pin `experiments/` or `data/` baselines only via explicit documented `--update` flows; never as a side effect of verification.
- Always use `SEED=42` for verification/reproduction. Do not commit `__pycache__` artifacts or verification output.
- Generic handoff aliases must resolve to the latest durable timestamped handoff; preserve historical timestamped/special handoff files.

## Known open items (from ledger/AGENTS; not blockers)

- **E049/E050:** E041/E042 grid artifacts remain 1-ulp sensitive under the ill-conditioned tangency QP (optimizer constraint-validation fixed; exact KKT enumeration available). Numeric drift remains in extended comparison — do **not** re-pin to silence it.
- **E048:** data-cache coverage enforced by `scripts/check_data_coverage.py` / `ledger/data_baseline.json`; add inputs only by committing files and re-pinning via `--update`.
- CI verification workflow cannot be pushed by automated agents; maintainer must create it from `.github/workflow-templates/verification-gate.yml` (see `VERIFICATION_GATE_TEMPLATE.md`).

## Initial task for next session

1. **Orient:** read this handoff and `AGENTS.md`; confirm `git status` shows only expected `__pycache__/*.pyc` noise and no `.verify_snapshot/`.
2. **Integrity gate before changes:** run `SEED=42 bash scripts/check.sh` (or `make check`). If golden/baseline/data issues are reported, restore/fix per `AGENTS.md` before proceeding. Escalate to `SEED=42 python3 run_all_verification.py` / `--extended` only when warranted.
3. **Handle user-directed work:** follow project conventions (pre-registration, no goalpost changes, no committing verification output, no golden/data re-pins without deliberate update flow). Research program is closed (E001–E051); avoid speculative new strategy exploration unless explicitly requested and properly pre-registered.
4. **Close-out (if material work performed):** create a new timestamped durable handoff, repoint canonical aliases via `python3 scripts/repoint_handoff.py <new_handoff_file>`, update `ledger/RESEARCH_LEDGER.md` only if appropriate, and leave no `__pycache__`/verification artifacts staged.

_No pending implementation tasks carried forward from this handoff._
