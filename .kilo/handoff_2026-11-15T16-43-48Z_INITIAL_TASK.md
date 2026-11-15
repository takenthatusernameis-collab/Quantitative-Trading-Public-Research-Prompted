# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-15T16:43:48Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch / HEAD:** `main` @ `e3c096c3` (`e3c096c3`, `chore(kilo): checkpoint agent session`)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## State snapshot (verified at handoff)

- **Research phase:** complete (E001–E051 per ledger; `AGENTS.md` text still says E001–E043). Authoritative dispositions and surviving validated strategies: `ledger/RESEARCH_LEDGER.md`. **No open research task by default.** Latest ledger entry at handoff: **E383**; this handoff action records E384. Research/handoff refreshes run through E384 with all items COMPLETE/CLOSED.
- **Sync status:** `main` in sync with `origin/main` (`git rev-list --left-right --count origin/main...HEAD` → `0 0`).
- **Canonical / do-not-touch-without-explicit-rebaseline:** `experiments/*.json` (107 tracked), `ledger/golden_baseline.json`, `ledger/data_baseline.json`, `data/vintages.json`, `data/fundamentals_vintages.json`, pinned `data/` and `data/fundamentals/`.
- **Verification state:** `.verify_snapshot/` absent; `.verify_reports/` absent. No interrupted verification observed at handoff.
- **Working tree at handoff:** only the pre-existing `src/__pycache__/cache_keys.cpython-312.pyc` modification plus the expected symlink/pointer and ledger/handoff deliverable changes from this handoff action. No source, experiments, ledgers, baselines, or pinned data were intentionally modified by this session. Do not commit the `__pycache__` change or handoff pointer churn as research content.
- **Delta since prior durable handoff:** prior durable artifact `handoff_2026-11-15T16-27-57Z_INITIAL_TASK.md` was taken at HEAD `ed722217`; `git diff --name-only ed722217..e3c096c3` filtered to research content (`experiments/`, `data/`, `src/`, `scripts/`, `tests/`, `research_state/`, excluding `__pycache__`/`*.pyc`) → **0 paths**. Only checkpoint commits, handoff/pointer files, the ledger entry, and `__pycache__/*.pyc` changed.
- **Closed — do not reopen without explicit user direction:** E049/E050 (optimizer determinism + KKT validation rule). Do **not** re-pin E041/E042 artifacts to silence residual ~1-ulp / ~1e-05 ill-conditioned QP drift.

## Clear initial task for next session

**Default: await explicit user instructions.**

Do not invent experiments, move pre-registered goalposts, run long verification unprompted, or modify canonical goldens/baselines.

### 1) Integrity check before any substantive work

```bash
git status --short --branch
git rev-parse --short HEAD
test ! -d .verify_snapshot || echo "STALE SNAPSHOT: SEED=42 python3 run_all_verification.py --restore-only"
pip install -r requirements.txt        # this sandbox is missing pandas/numpy/pytest
SEED=42 bash scripts/check.sh          # or: make check
```

- If `.verify_snapshot/` exists, restore first: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned artifacts per `AGENTS.md`).
- If a golden/baseline mismatch is reported, restore pinned artifacts before committing. **Never re-pin to hide drift.**
- Repo-level guards verified green in this sandbox (all exit 0): `check_json_artifacts.py` (114 JSON artifacts parse), `check_goldens_clean.py` (goldens match HEAD), `check_golden_baseline.py` (all 107 pinned goldens match), `check_data_coverage.py` (all 35 pinned data inputs present/tracked/unchanged), `verify_convention_robustness.py` (all strategy blocks PASS), `validate_template.py`, `check_experiment_imports.py`. Unit tests fail **only** on missing `numpy`/`pandas`/`pytest`, not on repo content.

### 2) If verification / reproduction is explicitly requested

Always use **`SEED=42`**. Never leave a verification run half-finished.

```bash
make check            # fast guards (~seconds, offline)
make verify           # convention robustness only (read-only)
make verify-quick     # ~8 min
make verify-extended  # ~21 min
make verify-full      # ~15 min
```

- `run_all_verification.py` overwrites and restores `experiments/*.json`. **Never commit verification output** over goldens.
- Interrupted run recovery: `SEED=42 python3 run_all_verification.py --restore-only`.
- Re-pin baselines only with explicit direction, deliberate `--update` commands, and ledger justification.

### 3) If new research work is explicitly requested

- Pre-register objective, gates, falsification expectations, and sensitivity grid **before execution**; use `SEED=42`.
- Verify handoff premises against artifacts before relying on them (ledger v1.2.1 rule).
- Preserve offline reproducibility (`QUANT_RESEARCH_OFFLINE=1` in suite). Add data inputs only by committing files and re-pinning (`python3 scripts/check_data_coverage.py --update`) with ledger justification.
- Record negative/partial outcomes honestly in `ledger/RESEARCH_LEDGER.md` and artifacts.
- Do not change pre-registered gates/outcomes without explicit justification and a ledger update.

## Guardrails

- **Seed:** always `SEED=42` for reproducibility/verification.
- **Goldens/baselines:** canonical; never modified/re-pinned as a side effect of verification.
- **Optimizer:** validate solver answers on problem constraints, not solver exit status (E049 / `tests/test_portfolio_opt.py`).
- **CI:** `.github/workflows/` verification gate cannot be created by automated agents. Template: `.github/workflow-templates/verification-gate.yml` (maintainer action required).
- **Commits:** only when explicitly requested; never commit secrets; never change pre-registered gates/outcomes without justification.

## Key references

- `AGENTS.md` — commands, verification modes, baseline/integrity rules
- `ledger/RESEARCH_LEDGER.md` — dispositions and standing notes (through E384)
- `ledger/PRIORITIZATION.md` — ranking procedure (v1.2.x active)
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints
- `experiments/*.json` — canonical research artifacts
- `scripts/check.sh`, `run_all_verification.py` — verification entrypoints
- `scripts/repoint_handoff.py` — generic pointer maintenance

## Provenance

- **Durable artifact (this session):** `handoff_2026-11-15T16-43-48Z_INITIAL_TASK.md` (repo root).
- **Supersedes operationally:** prior `handoff_*` / `HANDOFF_*` initial-task handoffs (retained for history). Most recent prior durable: `handoff_2026-11-15T16-27-57Z_INITIAL_TASK.md` (SHA-256 `8fb9fecba419c9ee76c99cb23dd7cd3133d7edcf02390ffc09bf265e4d12bf56`, HEAD `ed722217`).
- No research code, experiments, ledgers, baselines, or canonical data/artifacts were modified by this handoff action.