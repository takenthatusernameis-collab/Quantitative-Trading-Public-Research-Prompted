# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-23T19:02:10Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `b4de5f5a chore(kilo): checkpoint agent session` (in sync with `origin/main`: `git rev-list --left-right --count origin/main...HEAD` = `0  0`)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## READ THIS FIRST — a verification run is LIVE right now

**The single most important fact, carried forward and re-verified at this timestamp.** A `run_all_verification.py --extended` run is in progress and actively writing driver output into `experiments/`:

- **PID 114354** — `python3 run_all_verification.py --extended` (started ~18:26:48Z, still alive at handoff; elapsed ~36m).
- **Progress at handoff time:** extended driver block in flight; `.verify_snapshot/ACTIVE.json` is PRESENT and LIVE (`pid: 114354`, alive). `.verify_snapshot/experiments/` holds the pristine copies of all 107 golden artifacts.
- `.verify_reports/` is **absent** — it will only be written (gitignored, outside `experiments/`) if `--extended` completes successfully.
- `scripts/check_goldens_clean.py` correctly reports the run in progress and exits 0.
- Working tree currently shows no `experiments/` diff (only tracked `__pycache__/*.pyc` build noise); in-flight driver output may appear mid-write — do not read it as final state.

**Therefore, do NOT:**
1. **Do NOT start another verification run** — the suite refuses to start while a live run owns the snapshot; forcing it risks corrupting the snapshot/goldens.
2. **Do NOT kill PID 114354** or its child drivers — let it finish; on success it restores all goldens from the snapshot and removes `.verify_snapshot/`.
3. **Do NOT commit any `experiments/*.json`** — that replaces a canonical golden with partial driver output (the failure mode behind reverted commits `d6042b0`/`9f20def`/`1623923`/`701ed78`, per `AGENTS.md`).
4. **Do NOT run `check_golden_baseline.py` and treat a mismatch as a regression** while the run is live — it compares `experiments/` against the pinned fingerprint and will *correctly* fail on in-flight drivers. Run the full guard set only *after* the run completes and restores, or after recovery (below).

**Recovery if the run's process tree dies before finishing** (SIGKILL/OOM/idle-timeout of its owning session): a killed run leaves the snapshot recoverable by design.
- Preferred: `SEED=42 python3 run_all_verification.py --restore-only` (restores goldens from `.verify_snapshot/`, clears the marker).
- Alternative: `git checkout b4de5f5a -- experiments/` (HEAD holds the last committed goldens).
- Then confirm `.verify_snapshot/` is gone and `git status --porcelain` shows no `experiments/` diff before doing anything else.

## Current state (verified at handoff, 2026-11-23T19:02Z)

- **Research phase:** complete (E001–E043 core; handoff refreshes logged through E728+). Authoritative dispositions in `ledger/RESEARCH_LEDGER.md`. No actionable open/pending research items.
- **HEAD:** `b4de5f5a` on `main`, == `origin/main` (`0  0`).
- **Working tree:** tracked `__pycache__/*.pyc` build noise plus potential live-run in-flight `experiments/` writes (none currently diffed). No source/data/research_state change.
- **Deps:** provisioned (`numpy 2.5.4`). The live run is doing the full suite; this session did not.
- **Verify snapshot:** `.verify_snapshot/` PRESENT and LIVE (see top). `.verify_reports/` absent (written by `--extended` on success).

## Initial task for the next session (CLEAR, prioritized)

**Default: await explicit user instructions.** Do not invent experiments, move pre-registered gates, or touch golden/baseline/canonical artifacts without explicit direction.

If you must act autonomously, work the following in order and stop when a step is done:

1. **Wait for the live run to finish, then verify and stop.** Poll `ps -p 114354`. When it is gone and `.verify_snapshot/` no longer exists, run the full guard set:
   - `SEED=42 python3 scripts/check_goldens_clean.py`
   - `SEED=42 python3 scripts/check_golden_baseline.py`
   - `SEED=42 python3 scripts/check_data_coverage.py`
   If all three pass and `git status --porcelain` shows no `experiments/` diff, report state and stop — that is a complete, correct outcome. If the run died before finishing, follow **Recovery** above first.
2. **Report the `--extended` drift precisely.** On success `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json` (gitignored, outside `experiments/`) records per-driver numeric vs structural differences and worst drift as a multiple of tolerance. Expected (per `AGENTS.md`, numpy 2.5.4 / scipy 1.18.1): 0 differences across all 18 extended drivers. **Do NOT** re-pin any artifact to make a tolerance violation disappear; only a *deliberate* code change that alters a published number warrants re-pinning, and it must be ledgered first (E050 precedent).
3. **E041/E042 residual ill-conditioned-QP drift (~1e-05):** already root-caused and closed by the E050 exact KKT active-set enumeration (ledger E049/E050). Only revisit if step 2 shows a *new* structural difference; never "fix" it by re-pinning.
4. **Cleanup (propose only).** If the ~94% handoff-file bloat is a problem, *propose* (do not execute) a `.gitignore` + `git rm --cached` cleanup plan and let the user decide.
5. **Pre-registered research** only if the user explicitly requests it — with a `pre_registered` block, falsification expectations, and sensitivity grid stated *before* execution.

## Guardrails

- Always use **SEED=42** for reproducibility/verification.
- Never commit driver verification output over canonical goldens (`experiments/*.json`); never leave a verification run half-finished.
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction and ledger justification.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (template: `.github/workflow-templates/verification-gate.yml`; maintainer action required).
- Never commit secrets/keys; never log secrets.
- Do not manufacture another handoff refresh to look busy.

## Key references

- `AGENTS.md` — commands, reproducibility, baseline/guard invariants, snapshot recovery
- `ledger/RESEARCH_LEDGER.md` — dispositions (E001–E043 research; E652–E728+ handoff log)
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints
- `experiments/*.json` — canonical research artifacts
- `scripts/check.sh`, `run_all_verification.py`
- `scripts/repoint_handoff.py` — repoints generic alias symlinks to the latest handoff artifact

## Handoff provenance

- **Durable artifact (this session):** `handoff_2026-11-23T19-02-10Z_INITIAL_TASK.md` (repo root), reachable through the repointed generic alias symlinks (`CURRENT`, `LATEST`, `NEXT_SESSION`, etc.).
- **Supersedes operationally:** prior `HANDOFF_*` / `handoff_*` artifacts (retained for history).
- This session created this durable handoff and repointed the generic symlinks to it. **No code, experiments, ledgers, baselines, or canonical artifacts were modified. No commit was made** (left uncommitted pending explicit direction). The live verification run (PID 114354) was left undisturbed to complete on its own.
(End of file)
