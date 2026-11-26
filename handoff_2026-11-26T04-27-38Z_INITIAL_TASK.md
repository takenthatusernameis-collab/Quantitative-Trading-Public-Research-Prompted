# Initial Task for Next Agentic Work Session

**Timestamp**: 2026-11-26T04:27:38Z
**Repo**: Quantitative-Trading-Public-Research-Prompted
**Root**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Durable handoff**: `.handoff.md`

## Context
Independent reproducible quantitative-strategy research on 2014–2026 US equities,
futures, and macro data. Research phase complete (E001–E043); surviving validated
strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Git State
- Branch: `main`
- HEAD: `090dcf0df8a92d9377c10cbe72dbbfe707b468b2`
- Working tree: clean apart from tracked build noise `src/__pycache__/cache_keys.cpython-312.pyc`

## Default Initial Task (no explicit user instruction)
Await explicit user instructions. If acting autonomously:

1. Verify working-tree cleanliness against HEAD (`git status`).
2. Run the fast convention-robustness check:
   `SEED=42 bash scripts/check.sh` (or `make check`).
   This validates goldens-clean, golden baseline, data coverage, and optimizer determinism — all offline.
3. If clean, run extended verification and report any drift:
   `SEED=42 python3 run_all_verification.py --extended` (~8–21 min).
   Do NOT re-pin goldens.
4. If a verification run was interrupted, recover first:
   `SEED=42 python3 run_all_verification.py --restore-only` before committing anything.

## Key Conventions
- Always use `SEED=42` for reproducibility (walk-forward + placebo RNG).
- `experiments/*.json` are canonical research artifacts — never commit verification output over them.
- Dependencies are NOT provisioned; run `pip install -r requirements.txt` first.
- Verification enforces `QUANT_RESEARCH_OFFLINE=1`; unpinned inputs fail hard.
- `src/portfolio_opt.py` validates solver answers on constraints, not solver exit status (ledger E049/E050; exact KKT active-set enumeration, commit `72dc947`).
