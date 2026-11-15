# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-15T15:06:28Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch / HEAD:** `main` @ `7f7da88f36aefff57412649968944f74bb8f94ac` (`7f7da88f`, `chore(kilo): checkpoint agent session`, 2026-11-15 15:05:53 +0000)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## State snapshot (verified at handoff)

- **Research phase:** complete (E001–E051 per prior handoffs/ledger; `AGENTS.md` text still states E001–E043). **Authoritative dispositions and surviving validated strategies:** `ledger/RESEARCH_LEDGER.md`. No open research task by default.
- **Canonical / do-not-touch without explicit rebaseline:** `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`, `data/vintages.json`, `data/fundamentals_vintages.json`, pinned `data/` and `data/fundamentals/`.
- **Verification state:** `.verify_snapshot/` absent; `.verify_reports/` absent at handoff (no interrupted verification observed).
- **Working tree at handoff:** only `src/__pycache__/cache_keys.cpython-312.pyc` modified (pre-existing environment artifact, not canonical). This handoff session did not intentionally change source, experiments, ledgers, baselines, or pinned data.
- **Closed — do not reopen without explicit user direction:** E049/E050 (optimizer determinism + KKT validation rule). Do **not** re-pin E041/E042 artifacts to silence residual ~1-ulp / ~1e-05 ill-conditioned QP drift.

## Clear initial task for next session

**Default: await explicit user instructions.**

Do not invent experiments, move pre-registered goalposts, run long verification unprompted, or modify canonical goldens/baselines.

### 1) Integrity check before any substantive work

```bash
git status --short --branch
git rev-parse --short HEAD
test ! -d .verify_snapshot || echo "STALE SNAPSHOT: SEED=42 python3 run_all_verification.py --restore-only"
# if deps not installed: pip install -r requirements.txt
SEED=42 bash scripts/check.sh   # or: make check
```

- If `.verify_snapshot/` exists, restore first: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned artifacts per `AGENTS.md`).
- If a golden/baseline mismatch is reported, restore pinned artifacts before committing. **Never re-pin to hide drift.**
- Do not commit `__pycache__` or handoff-pointer churn as research content unless explicitly requested.

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

- **Seed:** always `SEED=42`.
- **Goldens/baselines:** canonical; never modified/re-pinned as a side effect of verification.
- **Optimizer:** validate solver answers on problem constraints, not solver exit status (E049 / `tests/test_portfolio_opt.py`).
- **CI:** `.github/workflows/` verification gate cannot be created by automated agents. Template: `.github/workflow-templates/verification-gate.yml` (maintainer action required).
- **Commits:** only when explicitly requested; never commit secrets.

## Key references

- `AGENTS.md` — commands, verification modes, baseline/integrity rules
- `ledger/RESEARCH_LEDGER.md` — dispositions and standing notes
- `ledger/PRIORITIZATION.md` — ranking procedure (v1.2.x active)
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints
- `experiments/*.json` — canonical research artifacts
- `scripts/check.sh`, `run_all_verification.py` — verification entrypoints
- `scripts/repoint_handoff.py` — generic pointer maintenance

## Provenance

- **Durable artifact (this session):** `handoff_2026-11-15T15-06-28Z_INITIAL_TASK.md` (repo root).
- **Supersedes operationally:** prior `handoff_*` / `HANDOFF_*` initial-task handoffs (retained for history). Most recent prior durable: `handoff_2026-11-15T15-02-34Z_INITIAL_TASK.md` (HEAD `2543c253` at that time).
- No research code, experiments, ledgers, baselines, or canonical data/artifacts were modified by this handoff action.
