# Handoff — Initial Task Message

**Timestamp:** 2026-11-21T00:18:54Z

## Initial Task

Confirm the repository baseline is clean and ready for the next change. No code changes are required for this session — this message IS the durable handoff artifact.

## Context

- Working directory: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
- Project: Quantitative Trading Public Research (reproducible strategy research, 2014–2026 US equities/futures/macro)
- Research phase: E001–E043 complete; surviving strategies documented in `ledger/RESEARCH_LEDGER.md`
- Golden artifacts: `experiments/*.json` are committed and must never be modified by a verification run; recover with `run_all_verification.py --restore-only` if interrupted.
- Offline mode: verification runs with `QUANT_RESEARCH_OFFLINE=1`; unpinned data inputs fail hard (`scripts/check_data_coverage.py`).

## Next Steps (in order)

1. Check git state: `git status --short`. Only `__pycache__/*.pyc` build artifacts should appear. `experiments/`, `ledger/`, and `data/` must be unmodified vs HEAD. Restore if needed:
   `SEED=42 python3 run_all_verification.py --restore-only`
2. Run fast integrity check: `SEED=42 bash scripts/check.sh` (or `make check`).
3. Run quick verification before changes: `SEED=42 python3 run_all_verification.py` (~8 min; `make verify-quick`).
4. Review results; follow `AGENTS.md` guardrails on failures. Do **not** re-pin goldens/data as a side effect of verification.

## Key Pointers

- Ledger: `ledger/RESEARCH_LEDGER.md`
- Golden pin: `ledger/golden_baseline.json`
- Data pin: `ledger/data_baseline.json`
- Conventions: `AGENTS.md`

**Ready to start at step 1.**

(End of file)
