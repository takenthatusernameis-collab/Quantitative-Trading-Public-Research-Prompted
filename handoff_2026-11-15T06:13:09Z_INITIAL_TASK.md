# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-15T06:13:09Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `722c66943ff4fdd3013afab4421738d8fc53d4b3` (`chore(kilo): checkpoint agent session`); `origin/main...HEAD` = `0 0` (in sync)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current state

- **Research phase:** complete (E001–E051). Authoritative dispositions and surviving validated strategies are in `ledger/RESEARCH_LEDGER.md`. No actionable open, pending, or blocked research item.
- **Delta since prior durable handoff:** `handoff_2026-11-15T06:11:41Z_INITIAL_TASK.md` is the immediate predecessor. Since `7e137a2a`, the only committed change is checkpoint `722c6694`; no files under `experiments/`, `data/`, `src/`, `scripts/`, `tests/`, `ledger/`, or `research_state/` changed.
- **Baseline integrity:** verified this session with `SEED=42 bash scripts/check.sh`; it reached `=== All checks passed ===`. The check confirmed 107 pinned golden artifacts match both HEAD and `ledger/golden_baseline.json`, and 35 pinned data inputs are present, tracked, and unchanged. The expected malformed-fixture failures printed by the JSON guard are test fixtures, not repository findings.
- **Canonical artifacts:** `git diff` and `git status` show no modifications to `experiments/`, `data/`, `ledger/`, source, scripts, or tests. No verification run is active and `.verify_snapshot/` is absent.
- **Working tree:** only tracked `__pycache__/*.pyc` files are modified. Treat this as generated noise; do not commit it.
- **Closed — do not reopen:** E049/E050 (optimizer determinism and exact KKT enumeration) and E041/E042 residual ill-conditioned-QP drift (~1-ulp, ~1e-05). Do not re-pin artifacts solely to silence that drift.

## INITIAL TASK for the next session

**Default: await explicit user instructions.** Do not invent experiments, run long verification unprompted, change pre-registered gates/outcomes, or modify golden/baseline artifacts without explicit direction.

### Before substantive work

1. Run `git status --short --branch` and confirm HEAD/remote alignment; ignore `__pycache__/*.pyc` churn.
2. Confirm `.verify_snapshot/` is absent. If an interrupted run is pending, run `SEED=42 python3 run_all_verification.py --restore-only` before any other work.
3. If dependencies are needed, use `pip3 install -r requirements.txt` (or `pip3 install --break-system-packages -r requirements.txt` in this environment).
4. Run `SEED=42 bash scripts/check.sh` (or `make check`) before committing a substantive change.

### If verification or reproduction is explicitly requested

- Always use `SEED=42`.
- Scopes: `make check` (fast guards); `SEED=42 python3 verify_convention_robustness.py` (read-only); `SEED=42 python3 run_all_verification.py` (quick, about 8 minutes); `--extended` (about 21 minutes); `--full`.
- Verification overwrites and restores `experiments/*.json`; never leave a run half-finished and never commit verification output over goldens. If interrupted, use `SEED=42 python3 run_all_verification.py --restore-only`.
- Do not re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` to silence drift. Re-pin only with explicit direction, the deliberate update command, and ledger justification.

## Guardrails

- Use `SEED=42` for reproducibility and verification runs.
- Never commit driver output over canonical goldens in `experiments/`.
- Never re-pin baselines without explicit instruction and ledger justification.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent; the copyable template is `.github/workflow-templates/verification-gate.yml` and a maintainer must create the actual workflow.
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and a ledger update.
- Never commit or log secrets/keys.

## Key references

- `AGENTS.md` — commands, reproducibility, baseline/guard invariants.
- `ledger/RESEARCH_LEDGER.md` — dispositions and open items.
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints.
- `experiments/*.json` — canonical research artifacts.
- `run_all_verification.py`, `scripts/check.sh`, `scripts/repoint_handoff.py`.

## Handoff provenance

- **Durable artifact:** `handoff_2026-11-15T06:13:09Z_INITIAL_TASK.md`
- **Supersedes operationally:** `handoff_2026-11-15T06:11:41Z_INITIAL_TASK.md` (retained for history)
- This session created this durable handoff only; no code, experiments, ledgers, baselines, or canonical research artifacts were modified.