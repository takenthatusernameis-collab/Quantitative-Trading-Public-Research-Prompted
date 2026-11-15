# Durable Handoff — Initial Task for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-15T14:57:00Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch / HEAD:** `main` @ `64f30e6f361c3cfcb11987af631a3050384fa741` (`64f30e6f`)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## State snapshot

- **Research phase complete (E001–E051).** Authoritative dispositions and surviving validated strategies: `ledger/RESEARCH_LEDGER.md`. No open research task by default.
- **Canonical artifacts/baselines authoritative (do not modify without explicit re-baseline):** `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`, `data/vintages.json`, `data/fundamentals_vintages.json`, pinned `data/` and `data/fundamentals/`.
- **No interrupted verification observed at handoff:** `.verify_snapshot/` absent, `.verify_reports/` absent.
- **Working tree at handoff:** tracked `src/__pycache__/cache_keys.cpython-312.pyc` modified (pre-existing environment artifact, not canonical). No intentional changes to source, experiments, ledgers, baselines, or pinned data in this handoff action.
- **Delta vs prior durable handoff (`handoff_2026-11-15T14-52-54Z_INITIAL_TASK.md`, HEAD `2d1e116a` → `64f30e6f`):** `git diff --name-only 2d1e116a..64f30e6f` filtered to research content (`experiments/`, `data/`, `src/`, `scripts/`, `tests/`, `research_state/`, excl `__pycache__`/`*.pyc`) → **0 paths**. Only checkpoint commits, generic handoff symlink/pointer files, `ledger/RESEARCH_LEDGER.md` (this entry), and `__pycache__/*.pyc` changed. No research substance changed.
- **Supersedes operationally:** prior `handoff_*` / `HANDOFF_*` initial-task handoffs (retained for history). Most recent prior: `handoff_2026-11-15T14-52-54Z_INITIAL_TASK.md` (SHA-256 `fd4fec07ce93fb99c92e94c7ed098a5032719b24f7d82f7e9764621afb531bd9`).

## Clear initial task for next session

**Default: await explicit user instructions.** Do not invent experiments, move goalposts, run long verification unprompted, or modify canonical goldens/baselines.

### 1) Baseline & integrity check (before any substantive work)
```bash
git status --short --branch
git rev-parse --short HEAD
test ! -d .verify_snapshot || echo "STALE SNAPSHOT: SEED=42 python3 run_all_verification.py --restore-only"
# after deps installed (pip install -r requirements.txt):
SEED=42 bash scripts/check.sh   # or: make check
```
- If `.verify_snapshot/` exists, restore first: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned artifacts per `AGENTS.md`).
- If golden/baseline mismatch is reported, restore pinned artifacts before committing; **never re-pin to hide drift**.

### 2) If verification/reproduction is explicitly requested
Always use **`SEED=42`** and never leave a verification run half-finished.
```bash
make check            # fast guards (~seconds, offline)
make verify           # convention robustness only (read-only)
make verify-quick     # ~8 min
make verify-extended  # ~21 min
make verify-full      # ~15 min
```
- `run_all_verification.py` overwrites and restores `experiments/*.json`; **never commit verification output** over goldens.
- Interrupted run recovery: `SEED=42 python3 run_all_verification.py --restore-only`.

### 3) If new research work is explicitly requested
- Pre-register objective, gates, falsification expectations, and sensitivity grid **before execution**; use `SEED=42`.
- Preserve data/cache/baseline invariants and offline reproducibility (`QUANT_RESEARCH_OFFLINE=1` in suite). Add data inputs only by committing files and re-pinning (`python3 scripts/check_data_coverage.py --update`) with ledger justification.
- Record negative/partial outcomes honestly in `ledger/RESEARCH_LEDGER.md` and artifacts.
- Do not reopen closed findings (E049/E050) or re-pin E041/E042 artifacts to silence residual 1-ulp optimizer drift.

## Guardrails

- **Seed:** always `SEED=42` for reproducibility/verification.
- **Goldens/baselines:** canonical; never modified/re-pinned as a side effect of verification. Re-pin only with explicit direction + `--update` commands + ledger justification.
- **Optimizer:** validate solver answers on problem constraints, not solver exit status (E049 / `tests/test_portfolio_opt.py`).
- **CI:** `.github/workflows/` verification gate cannot be created by automated agents (template: `.github/workflow-templates/verification-gate.yml`).
- **Commits:** only when explicitly requested; never commit secrets; never change pre-registered gates/outcomes without justification.

## Key references

- `AGENTS.md` — commands, verification modes, baseline/integrity rules
- `ledger/RESEARCH_LEDGER.md` — dispositions and standing notes (E001–E051)
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints
- `scripts/check.sh`, `run_all_verification.py` — verification entrypoints

## Provenance

Durable handoff created at `handoff_2026-11-15T14-57-00Z_INITIAL_TASK.md`. No research code, experiments, ledgers, baselines, or canonical data/artifacts were modified by this handoff action.