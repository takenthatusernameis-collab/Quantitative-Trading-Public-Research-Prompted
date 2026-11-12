# Handoff — 2026-11-12T08:17:46Z

## Project State
- **Repo**: Quantitative-Trading-Public-Research-Prompted
- **Phase**: Research complete (E001–E043); surviving strategies in `ledger/RESEARCH_LEDGER.md`
- **Working directory**: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Key Commands
```bash
# Quick checks
SEED=42 bash scripts/check.sh           # convention robustness (~seconds)
SEED=42 python3 run_all_verification.py --skip-slow  # convention only

# Verification tiers
SEED=42 python3 run_all_verification.py          # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended # extended (~21 min)
SEED=42 python3 run_all_verification.py --full     # full (~15 min)

# Recovery
SEED=42 python3 run_all_verification.py --restore-only
```

## Critical Reminders
- **Never leave verification half-finished** — it overwrites `experiments/*.json` goldens and restores them after; interrupted runs leave driver output in place
- **Golden integrity**: `scripts/check_goldens_clean.py` (working tree vs HEAD) and `scripts/check_golden_baseline.py` (HEAD vs pinned SHA-256 in `ledger/golden_baseline.json`) are first-class gates
- **Data coverage invariant**: `scripts/check_data_coverage.py` enforces every `data.download()` call site has a committed, SHA-pinned cache file
- **Optimizer determinism**: `src/portfolio_opt.py` validates on constraints, not solver exit status (ledger E049); E041/E042 grid artifacts still drift ~1e-05 — do not re-pin to silence

## Open Items (from ledger)
- E041: 133 numeric differences remain (ill-conditioned QP, 1-ulp sensitivity) — open item, do not re-pin
- E030: Now reproducible (panel committed, golden re-pinned per ledger E048)
- E029: Offline-reproducible since 2026-10-20 (fundamentals pinned in `data/fundamentals/`)

## CI Note
`.github/workflows/verification-gate.yml` cannot be created by agents — maintainer must create via GitHub UI from template at `.github/workflow-templates/verification-gate.yml`