# Handoff — Next Agentic Work Session (Initial Task Message)

**Timestamp:** 2026-11-26T02:18:09Z
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**HEAD:** d69315c9 (`main`, in sync with `origin/main`)
**Durable pointer:** `.handoff.md` → this file

## Project Context

Independent reproducible quantitative-strategy research on 2014–2026 US equities,
futures, and macro data. All experiments are pre-registered with falsification
expectations and promotion gates. **Research phase complete (E001–E043).**
Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

## Git State (this session)

- Branch: `main`, up to date with `origin/main`.
- Working tree: dirty only for tracked build noise
  `src/__pycache__/cache_keys.cpython-312.pyc` (harmless; not research output).
- `.verify_snapshot/` and `.verify_reports/` absent (no interrupted run to recover).
- Last commits: `chore(kilo): checkpoint agent session` (checkpoint noise).

## Quick Commands

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh
#   or
make check

# Quick full verification (~8 min; 8 drivers + batch_run + validate + E042 n_sim=2)
SEED=42 python3 run_all_verification.py
#   or
make verify-quick

# Extended verification (~21 min; quick + 18 more drivers, structural match)
SEED=42 python3 run_all_verification.py --extended
#   or
make verify-extended

# Recover golden artifacts after an interrupted verification run
SEED=42 python3 run_all_verification.py --restore-only
```

## Key Integrity Notes (read before acting)

- `experiments/*.json` are canonical golden artifacts; verification overwrites
  them while re-running drivers and restores afterwards — **never leave a run
  half-finished**.
- Never commit verification output. Recover first with `--restore-only`.
- Golden baseline is pinned in `ledger/golden_baseline.json` (SHA-256); never
  re-pin as a side effect of verification.
- Data coverage is enforced: `scripts/check_data_coverage.py` requires every
  cache file to exist, be tracked, and match `ledger/data_baseline.json`.
- **Always use `SEED=42`.** Dependencies are NOT provisioned: run
  `pip install -r requirements.txt` before any verification (`import numpy`
  currently fails with `ModuleNotFoundError`).
- Optimizer determinism: `src/portfolio_opt.py` validates solver answers on the
  problem's constraints, never on solver exit status (ledger E049/E050 exact
  active-set enumeration; E041/E042 are bit-reproducible under this path).
- CI gate `.github/workflows/verification-gate.yml` cannot be created by agents;
  template at `.github/workflow-templates/verification-gate.yml`.

## Initial Task for Next Session

Default: await explicit user instructions. If acting autonomously:

1. Confirm working-tree cleanliness against HEAD (`git status`).
2. Run `SEED=42 bash scripts/check.sh` (fast, offline). If green, report PASS
   and stop — do not commit verification output and do not extend into new
   research.
3. Only if deps are available and explicitly requested, run
   `SEED=42 python3 run_all_verification.py --extended` and report any drift
   per-driver (numeric vs structural). **Do NOT re-pin goldens** to silence drift.
4. If a verification run was interrupted, recover with
   `SEED=42 python3 run_all_verification.py --restore-only` before committing
   anything.

## Key Files

- `ledger/RESEARCH_LEDGER.md` — surviving validated strategies
- `experiments/*.json` — canonical research artifacts (golden files)
- `data/vintages.json` — pinned data vintage (2026-10-12)
- `data/fundamentals_vintages.json` — pinned fundamentals for E029
- `ledger/golden_baseline.json` — SHA-256 fingerprints of golden artifacts
- `ledger/data_baseline.json` — SHA-256 fingerprints of data files
- `AGENTS.md` — full project conventions and commands
