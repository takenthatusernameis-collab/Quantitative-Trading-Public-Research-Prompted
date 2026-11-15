# Durable Handoff — Initial Task for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-15T14:05:57Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch / HEAD:** `main` @ `d19681ee1d4decd7b29a663c7ff14755e7ddcb95` (`chore(kilo): checkpoint agent session`)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## State snapshot

- **Research phase complete (E001–E051).** Dispositions, validated survivors, and standing notes: `ledger/RESEARCH_LEDGER.md`. No open research task by default.
- Prior durable handoff superseded (retained): `handoff_2026-11-15T14-04-34Z_INITIAL_TASK.md`.
- No interrupted verification markers observed (`.verify_snapshot/`, `.verify_reports/` absent).
- Observed at handoff creation: tracked `src/__pycache__/cache_keys.cpython-312.pyc` modified (pre-existing environment artifact, not canonical). No intentional changes to `experiments/*.json`, ledgers, pinned baselines, or pinned data snapshots.
- Canonical artifacts/baselines are authoritative: `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`, `data/vintages.json`, `data/fundamentals_vintages.json`.

## Initial task for next session

**Default: await explicit user instructions.** Do not invent experiments, move goalposts, or modify canonical goldens/baselines without explicit direction.

### 1) Baseline & integrity check (before substantive work)
```bash
git status --short --branch
test ! -d .verify_snapshot || echo "STALE SNAPSHOT: SEED=42 python3 run_all_verification.py --restore-only"
# after deps installed (pip install -r requirements.txt):
SEED=42 bash scripts/check.sh   # or: make check
```
- If `.verify_snapshot/` exists, restore first: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned artifacts per `AGENTS.md`).
- If golden/baseline mismatch is reported, restore pinned artifacts before committing; do **not** re-pin to hide drift.

### 2) If verification/reproduction is explicitly requested
Always use **`SEED=42`** and never leave a verification run half-finished.
```bash
make check            # fast guards (~seconds, offline)
make verify           # convention robustness only
make verify-quick     # ~8 min
make verify-extended  # ~21 min
make verify-full      # ~15 min
```
- `run_all_verification.py` overwrites and restores `experiments/*.json`; **never commit verification output** over goldens. Interrupted run: `SEED=42 python3 run_all_verification.py --restore-only`.
- Do **not** re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` to silence known E041/E042 residual 1-ulp optimizer drift.

### 3) If new research work is explicitly requested
- Pre-register objective, gates, falsification expectations, and sensitivity grid **before execution**; use `SEED=42`.
- Preserve data/cache/baseline invariants and offline reproducibility (`QUANT_RESEARCH_OFFLINE=1` in suite). Add data inputs only by committing files and re-pinning (`python3 scripts/check_data_coverage.py --update`).
- Record negative/partial outcomes honestly in `ledger/RESEARCH_LEDGER.md` and artifacts.
- Do not reopen closed findings (E049/E050) or treat residual optimizer drift as a re-pin target.

## Guardrails

- **Seed:** always `SEED=42`.
- **Goldens/baselines:** canonical; never modified or re-pinned as a side effect of verification.
- **Optimizer:** validate solver answers on problem constraints, not solver exit status (E049 / `tests/test_portfolio_opt.py`).
- **CI:** verification workflow cannot be created by automated agents (template: `.github/workflow-templates/verification-gate.yml`).
- **Commits:** only when explicitly requested; never commit secrets.

## Key references

- `AGENTS.md` — commands, verification modes, baseline/integrity rules
- `ledger/RESEARCH_LEDGER.md` — dispositions and standing notes (E001–E051)
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints
- `scripts/check.sh`, `run_all_verification.py` — verification entrypoints

## Provenance

Durable handoff created at `handoff_2026-11-15T14-05-57Z_INITIAL_TASK.md`, mirrored to `handoff/` and `HANDOFFS/`, and generic alias pointers repointed via `scripts/repoint_handoff.py`. Prior timestamped handoffs and aliases retained for continuity. No research code, experiments, ledgers, baselines, or canonical data/artifacts were modified.
