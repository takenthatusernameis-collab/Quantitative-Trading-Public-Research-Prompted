# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-15T07:11:29Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `ee074a41e51cb5dcbea8d415b80123373f4f9a9b` (`chore(kilo): checkpoint agent session`); `origin/main...HEAD` = `0 0` (in sync at session start).
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

---

## INITIAL TASK for the next session

**Default: await explicit user instructions.** Do not invent experiments, run long verification unprompted, change pre-registered gates/outcomes, or modify golden/baseline artifacts without explicit direction.

The standing user instruction for this repository is: *"Leave a timestamped clear initial task message for the next agentic work session in a durable handoff."* That instruction is satisfied by this artifact. Any further work requires a new, explicit user request.

### Before substantive work

1. Run `git status --short --branch` and confirm HEAD/remote alignment; treat `__pycache__/*.pyc` churn as non-canonical build noise (do not commit).
2. Confirm `.verify_snapshot/` is absent. If an interrupted run is pending, run `SEED=42 python3 run_all_verification.py --restore-only` before any other work.
3. If dependencies are needed, use `pip3 install -r requirements.txt` (or `pip3 install --break-system-packages -r requirements.txt` in this environment).
4. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing a substantive change.

### If verification or reproduction is explicitly requested

- Always use `SEED=42`.
- Scopes: `make check` (fast guards); `SEED=42 python3 verify_convention_robustness.py` (read-only); `SEED=42 python3 run_all_verification.py` (quick, ~8 min); `--extended` (~21 min); `--full`.
- Verification overwrites and restores `experiments/*.json`; never leave a run half-finished and never commit verification output over goldens. If interrupted, use `SEED=42 python3 run_all_verification.py --restore-only`.
- Do not re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` to silence drift. Re-pin only with explicit direction, the deliberate update command, and ledger justification.

---

## Current state (verified this session)

- **Research phase:** complete (E001–E051). Authoritative dispositions, surviving validated strategies, and closed/open items are in `ledger/RESEARCH_LEDGER.md`. No actionable open, pending, or blocked research item.
- **Baseline integrity — re-verified this session:** `SEED=42 bash scripts/check.sh` → **exit 0, `=== All checks passed ===`** (py_compile, JSON artifacts parse, goldens clean vs HEAD, pinned golden-baseline match, data coverage, `tests/test_portfolio_opt.py`, convention robustness, template validation, experiment imports).
- **Canonical artifacts:** 107 tracked `experiments/*.json`; `git status` at session start showed no modifications to `experiments/`, `data/`, `ledger/`, source, scripts, or tests — only tracked `__pycache__/*.pyc`. No verification run is active; `.verify_snapshot/` is absent.
- **Working tree:** only tracked `__pycache__/*.pyc` files are modified (generated build noise). Do not commit.
- **Closed — do not reopen:** E049/E050 (optimizer determinism and exact KKT enumeration) and E041/E042 residual ill-conditioned-QP drift (~1-ulp, ~1e-05). Do not re-pin artifacts solely to silence that drift.

## Delta since prior durable handoff

Prior durable handoff: `handoff_2026-11-15T06:21:42Z_INITIAL_TASK.md` (HEAD `805afff6`). Current HEAD `ee074a41` advances from `805afff6` via a single checkpoint commit. `git diff --name-only 805afff6..ee074a41` filtered for research content (`experiments/`, `data/`, `src/`, `scripts/`, `tests/`, `research_state/`) → **0 paths**. The only research-tracked change is `ledger/RESEARCH_LEDGER.md` (the prior session's own E362 handoff-refresh entry); everything else is generic handoff symlink/pointer repointing and `__pycache__/*.pyc` noise. No research substance changed.

---

## Guardrails

- Use `SEED=42` for reproducibility and verification runs.
- Never commit driver verification output over canonical goldens in `experiments/`.
- Never re-pin baselines without explicit instruction and ledger justification.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent; the copyable template is `.github/workflow-templates/verification-gate.yml` and a maintainer must create the actual workflow.
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and a ledger update.
- Never commit or log secrets/keys.

## Key references

- `AGENTS.md` — commands, reproducibility, baseline/guard invariants.
- `ledger/RESEARCH_LEDGER.md` — dispositions and open items.
- `ledger/PRIORITIZATION.md` — ranking procedure.
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints.
- `experiments/*.json` — canonical research artifacts.
- `run_all_verification.py`, `scripts/check.sh`, `scripts/repoint_handoff.py`.

## Handoff provenance

- **Durable artifact:** `handoff_2026-11-15T07:11:29Z_INITIAL_TASK.md` (root; mirrored identically to `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/`).
- **Supersedes operationally:** `handoff_2026-11-15T06:21:42Z_INITIAL_TASK.md` (retained for history).
- This session created this durable handoff and its canonical pointer repoint only; no code, experiments, ledgers, baselines, or canonical research artifacts were modified beyond this handoff and its ledger entry.