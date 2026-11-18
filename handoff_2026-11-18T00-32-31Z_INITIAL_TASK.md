# Durable Handoff — Initial Task Message (Next Agentic Work Session)

**Timestamp (UTC):** 2026-11-18T00:32:31Z
**HEAD:** `703057342fee0c99fa5a0aba7ce9e07de9d23c11` (main, 2026-11-18T00:32:13Z) "chore(kilo): checkpoint agent session"
**Branch:** `main` — `git rev-parse origin/main` == HEAD (in sync, 0 ahead / 0 behind)
**Prior handoff:** `handoff_2026-11-18T00-31-37Z_INITIAL_TASK.md` (HEAD `70e0cd8e`) — superseded by this file.

## Repository state (at capture)

- **Research phase:** COMPLETE. Experiments E001–E051 are recorded in `ledger/RESEARCH_LEDGER.md` and the program is closed. No new research was performed in this session. Ledger tail confirms closure through E473 (2026-11-18T00:31:37Z); E052–E473 are durable-handoff refreshes only.
- **Working tree:** source-clean. `git status` shows only 15 modified tracked `__pycache__/*.pyc` bytecode files (build artifacts, not source — **do not commit**). `git diff --name-only HEAD -- experiments/ data/ ledger/ scripts/ src/ tests/ research_state/` (excluding `__pycache__`) is empty.
- **Golden baseline:** 107 tracked artifacts under `experiments/*.json`, all matching `ledger/golden_baseline.json` and HEAD. No data/golden drift.
- **Verification state:** no `.verify_snapshot/` and no `.verify_reports/` present; no interrupted verification run indicated; nothing to recover.
- **Symlink tree:** generic canonical pointers currently resolve to the prior handoff (`...T00-31-37Z...`). Repoint to this file with `python3 scripts/repoint_handoff.py handoff_2026-11-18T00-32-31Z_INITIAL_TASK.md`.

## Canonical invariants (do not violate)

- `experiments/*.json` are golden artifacts. The verification suite overwrites them during runs and restores them afterward — **never leave a run half-finished**.
- If interrupted or on golden mismatch: `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/` only when HEAD still holds the pinned baseline). See `AGENTS.md` "Baseline Integrity".
- Re-pin `experiments/` or `data/` baselines only via explicit documented `--update` flows (`python3 scripts/check_golden_baseline.py --update`, `python3 scripts/check_data_coverage.py --update`), never as a side effect of running the verification suite.
- Always use `SEED=42` for verification/reproduction commands.
- Do not commit `__pycache__/*.pyc` artifacts or verification output.
- CI verification workflow cannot be pushed by automated agents; maintainer action required per `.github/workflow-templates/verification-gate.yml` and `VERIFICATION_GATE_TEMPLATE.md`.

## Known open items (from ledger; not blockers)

- **E049/E050:** E041/E042 grid artifacts remain 1-ulp sensitive under the ill-conditioned tangency QP (optimizer constraint-validation defect fixed; exact KKT enumeration routes the QP per E050). Numeric drift remains in the extended comparison. Do **not** re-pin to silence drift — the committed golden is the authoritative record.
- **E048:** data-cache coverage is an enforced invariant; `scripts/check_data_coverage.py` guards every `data.download()` call site. To add a data input, commit the file and re-pin via `--update`.
- E029 (offline via pinned fundamentals snapshot), E030 (16-ETF panel pinned), and E041 (optimizer defect fixed, 133 numeric diffs remaining) all reproduce with bounded drift as documented in the ledger. No action required.

## Recommended next actions

1. **Orient:** read this handoff and `AGENTS.md`; confirm `git status` is clean aside from regenerated `__pycache__/*.pyc` noise, HEAD == `origin/main`, and that no `.verify_snapshot/` exists.
2. **Integrity check (before any new work):** run `SEED=42 bash scripts/check.sh` (or `make check`). If a golden/baseline mismatch is reported, restore per `AGENTS.md` before proceeding. Escalate to `SEED=42 python3 run_all_verification.py` / `--extended` / `--full` only if explicitly required.
3. **Handle user requests:** follow project conventions (pre-registration, no post-hoc goalpost changes, no committing verification output, no golden/data re-pins without deliberate `--update` flow). The research program is closed (E001–E051); avoid speculative new strategy exploration unless explicitly directed and properly pre-registered with a full placebo/falsification plan.
4. **Session close-out (if material work is done):** create a new timestamped durable handoff, mirror it to `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/`, repoint canonical handoff aliases via `python3 scripts/repoint_handoff.py <new_handoff_file>`, append a ledger entry, and do not commit `__pycache__` artifacts.

## Reproduction / verification quick reference

```bash
SEED=42 bash scripts/check.sh                 # fast convention + template + guards (~seconds)
SEED=42 python3 run_all_verification.py       # quick full (~8 min)
SEED=42 python3 run_all_verification.py --extended   # +18 committed drivers (~21 min)
SEED=42 python3 run_all_verification.py --full       # E042 n_sim=50 + 96-config grid (~15 min)
SEED=42 python3 run_all_verification.py --restore-only   # recover goldens after an interrupted run
```

_No pending implementation tasks carried forward from this handoff._