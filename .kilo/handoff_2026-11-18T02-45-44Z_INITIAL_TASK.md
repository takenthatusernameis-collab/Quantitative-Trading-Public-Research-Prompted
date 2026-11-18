# Durable Handoff — Initial Task Message (Next Agentic Work Session)

**Timestamp (UTC):** 2026-11-18T02:45:44Z
**HEAD:** `f966c04d3a67ef53173fc4651ea865a2dcc36bc5` (`main`, 2026-11-18T02:45:37Z) — "chore(kilo): checkpoint agent session"
**Branch:** `main` — `origin/main` == HEAD (in sync, 0 ahead / 0 behind)
**Prior handoff:** `handoff_2026-11-18T02-44-52Z_INITIAL_TASK.md` (HEAD `e5ab1144` at capture) — superseded by this file.

## Repository state (at capture)

- **Research phase:** COMPLETE. Experiments E001–E051 are recorded in `ledger/RESEARCH_LEDGER.md`; the program is closed. Ledger tail is through E479 (durable-handoff refreshes only). No new research performed in this session.
- **Working tree:** source-clean aside from regenerated `__pycache__/*.pyc` bytecode files (build artifacts). `git diff --name-only HEAD -- experiments/ data/ ledger/ scripts/ src/ tests/ research_state/` (excluding `__pycache__`) is empty. **Do not commit `__pycache__` artifacts.**
- **Golden baseline:** 107 tracked artifacts under `experiments/*.json` present; `ledger/golden_baseline.json` records 107 pinned files (`n_files=107`). No `experiments/`, `data/`, or ledger baseline drift indicated in working tree.
- **Verification state:** `.verify_snapshot/` and `.verify_reports/` are absent; no interrupted verification run indicated.
- **Handoff pointers:** canonical generic aliases will be repointed to this file via `python3 scripts/repoint_handoff.py handoff_2026-11-18T02-45-44Z_INITIAL_TASK.md`.

## Canonical invariants (do not violate)

- `experiments/*.json` are golden artifacts. The verification suite overwrites them during runs and restores them afterward — **never leave a run half-finished**.
- If interrupted or on golden mismatch: `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/` only when HEAD still holds the pinned baseline). See `AGENTS.md` "Baseline Integrity".
- Re-pin `experiments/` or `data/` baselines only via explicit documented `--update` flows (`python3 scripts/check_golden_baseline.py --update`, `python3 scripts/check_data_coverage.py --update`), never as a side effect of running the verification suite.
- Always use `SEED=42` for verification/reproduction commands.
- Do not commit verification output or `__pycache__/*.pyc` artifacts.
- CI verification workflow cannot be pushed by automated agents; maintainer action required per `.github/workflow-templates/verification-gate.yml` and `VERIFICATION_GATE_TEMPLATE.md`.

## Known open items (from ledger; not blockers)

- **E049/E050:** E041/E042 grid artifacts remain 1-ulp sensitive under the ill-conditioned tangency QP (optimizer constraint-validation defect fixed; exact KKT enumeration routes the QP per E050). Numeric drift remains in extended comparison — **do not re-pin** to silence drift; the committed golden is the authoritative record.
- **E048:** data-cache coverage is an enforced invariant; `scripts/check_data_coverage.py` guards every `data.download()` call site. To add a data input, commit the file and re-pin via `--update`.
- **Environment caveat (carried forward):** recent sessions reported `python3` on this runner may lack pandas/numpy/scipy/pyarrow/statsmodels/yfinance, causing `scripts/check.sh` / full verification to fail with missing-dependency errors. Before full gates, run `python3 -m pip install -r requirements.txt` if dependencies are absent.

## Recommended next actions

1. **Orient:** read this handoff and `AGENTS.md`; confirm `git status` is clean aside from regenerated `__pycache__/*.pyc` noise, `HEAD == origin/main`, and no `.verify_snapshot/` exists.
2. **Integrity check (before material changes):** run `SEED=42 bash scripts/check.sh` (or `make check`). If a golden/baseline mismatch is reported, restore per `AGENTS.md` before proceeding. Escalate to `SEED=42 python3 run_all_verification.py` / `--extended` / `--full` only if explicitly required.
3. **Handle user requests:** follow project conventions (pre-registration, no post-hoc goalpost changes, no committing verification output, no golden/data re-pins without deliberate `--update` flow). The research program is closed (E001–E051); avoid speculative new strategy exploration unless explicitly directed and properly pre-registered with full placebo/falsification plan.
4. **Session close-out (if material work is done):** create a new timestamped durable handoff, mirror it to `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/`, repoint canonical handoff aliases via `python3 scripts/repoint_handoff.py <new_handoff_file>` (and run `python3 scripts/repair_broken_handoff.py <new_handoff_file>` if broken historical pointers remain), append a ledger entry as appropriate, and do not commit `__pycache__` artifacts.

## Reproduction / verification quick reference

```bash
SEED=42 bash scripts/check.sh                 # fast convention + template + guards (~seconds)
SEED=42 python3 run_all_verification.py       # quick full (~8 min)
SEED=42 python3 run_all_verification.py --extended   # +18 committed drivers (~21 min)
SEED=42 python3 run_all_verification.py --full       # E042 n_sim=50 + 96-config grid (~15 min)
SEED=42 python3 run_all_verification.py --restore-only   # recover goldens after interrupted run
```

_No pending implementation tasks carried forward from this handoff._
