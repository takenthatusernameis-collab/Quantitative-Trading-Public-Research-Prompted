# Durable Handoff — Initial Task for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-15T11:03:21Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch / HEAD:** `main` @ `d48d94a95f6fdb8e33e1b6d2602d8095dcb12838` ("chore(kilo): checkpoint agent session")
**Sync:** in sync with `origin/main` at handoff time (`git status` showed no ahead/behind)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current state

- **Research phase:** complete (E001–E051). Authoritative dispositions and surviving validated strategies are in `ledger/RESEARCH_LEDGER.md`. No open research task identified.
- **Canonical artifacts:** `experiments/*.json` are pinned goldens; fingerprints/baselines in `ledger/golden_baseline.json` and `ledger/data_baseline.json`. Verification must back up/restore artifacts and must never be left half-finished.
- **Verification markers:** `.verify_snapshot/` and `.verify_reports/` not present at handoff time.
- **Working tree (observed):** 12 tracked `__pycache__/*.pyc` files modified in `scripts/__pycache__/`, `src/__pycache__/`, and `tests/__pycache__/` (incidental bytecode churn; no source edits made in this handoff session). Treat as uncommitted environment noise unless intentionally regenerated — do not commit casually.
- **Known standing note:** E041/E042 tangency-QP drift remains (ill-conditioned QP / ~1-ulp sensitivity, ~1e-05 scale). **Do not re-pin** those goldens to silence numeric drift; see `ledger/RESEARCH_LEDGER.md` and AGENTS.md (E049/E050 closed).

## Clear initial task for the next session

**Default:** await explicit user instructions. Do not invent new experiments, run verification unprompted, move goalposts, or modify canonical baselines/goldens without explicit direction.

### 1) Baseline integrity / environment check (before substantive work)
```bash
git status --short --branch
# Confirm no interrupted verification:
test ! -d .verify_snapshot || echo "STALE SNAPSHOT: SEED=42 python3 run_all_verification.py --restore-only"
SEED=42 bash scripts/check.sh
# or: make check
```
If dependency-bound unit tests fail only due to missing numpy/pandas in the environment, repo-level guard steps (goldens, baseline fingerprints, data coverage, JSON/template/import/convention checks) should still be interpreted per `scripts/check.sh` output.

### 2) If verification/reproduction is explicitly requested
Always use **`SEED=42`**.
```bash
make verify          # convention robustness only (reads JSONs, no writes)
make verify-quick    # ~8 min
make verify-extended # ~21 min
make verify-full     # ~15 min
```
- `run_all_verification.py` overwrites and restores `experiments/*.json`; **never leave a run half-finished** and **never commit verification output** over goldens.
- If interrupted/stale snapshot: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned artifacts per AGENTS.md).
- Do **not** re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` to silence drift. Re-pin only with explicit direction, deliberate update commands, and ledger justification.

### 3) If new research work is explicitly requested
- Pre-register objective, gates, falsification expectations, and sensitivity grid **before execution**.
- Use `SEED=42`; keep data/cache/baseline invariants intact (`QUANT_RESEARCH_OFFLINE=1` expectations, pinned inputs).
- Record negative/partial outcomes honestly in `ledger/RESEARCH_LEDGER.md` and artifacts as appropriate.
- Do not reopen closed E049/E050 or treat E041/E042 residual drift as a re-pin target.

## Guardrails

- Always use **`SEED=42`** for reproducibility/verification.
- Never commit secrets/keys; never log secrets.
- Never commit driver verification output over canonical goldens.
- Do not create `.github/workflows/` CI gates as an automated agent (template: `.github/workflow-templates/verification-gate.yml`; maintainer action required).
- Commit only when explicitly requested and only intentional source/research changes.

## Key references

- `AGENTS.md` — commands, reproducibility, baseline/guard invariants
- `ledger/RESEARCH_LEDGER.md` — dispositions, completed experiments, standing notes
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints
- `data/vintages.json`, `data/fundamentals_vintages.json` — pinned data snapshots
- `experiments/*.json` — canonical research artifacts
- `scripts/check.sh`, `run_all_verification.py` — verification entrypoints

## Provenance

- Created as a durable handoff artifact for continuity; prior `handoff_*` / `HANDOFF_*` files retained for history.
- No research code, experiments, ledgers, baselines, or canonical data/artifacts were modified by this handoff session.
