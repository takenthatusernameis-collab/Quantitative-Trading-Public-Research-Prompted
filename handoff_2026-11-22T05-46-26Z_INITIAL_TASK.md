# Agent Handoff — 2026-11-22T05:46:26Z

## Initial Task for Next Session
No specific task assigned yet. Next agentic session should begin by checking baseline integrity (`git status --short --branch`, confirm `.verify_snapshot/` is absent; if stale/interrupted run `SEED=42 python3 run_all_verification.py --restore-only`), then run `SEED=42 bash scripts/check.sh`, and await explicit user instructions before any substantive work.

Default: wait for explicit user instructions. Do not invent experiments, run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts without explicit direction.

## Session Context
- **Project**: Quantitative Trading Public Research (2014–2026 US equities, futures, macro)
- **Phase**: Research complete (E001–E043); surviving strategies in `ledger/RESEARCH_LEDGER.md`
- **Branch/HEAD**: `main` @ `0070e81f` (`chore(kilo): checkpoint agent session`)
- **Working Directory**: `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
- **Working tree**: `__pycache__/` bytecode modified (gitignored cache); tracked files otherwise clean — confirm with `git status --short --branch`
- **Seed**: always `SEED=42`

## Key Artifacts
- **Golden baseline**: `experiments/*.json` (canonical, SHA-256 pinned in `ledger/golden_baseline.json`)
- **Data cache**: `data/` (gitignored except pinned vintages 2026-10-11, 2026-10-12); coverage enforced per `ledger/data_baseline.json`, `QUANT_RESEARCH_OFFLINE=1`
- **Fundamentals**: `data/fundamentals/` pinned per `data/fundamentals_vintages.json`
- **Verification snapshot**: `.verify_snapshot/` (gitignored; `ACTIVE.json` tracks live run) — recover with `--restore-only`

## Quick Commands
```bash
SEED=42 bash scripts/check.sh                # fast convention + golden diff + baseline + optimizer test
SEED=42 python3 run_all_verification.py      # quick full verification (~8 min)
SEED=42 python3 run_all_verification.py --extended   # extended (~21 min)
SEED=42 python3 run_all_verification.py --restore-only
SEED=42 python3 -m py_compile <changed file>
```

## Integrity Guards
- `scripts/check.sh` → `make check` (convention + golden diff + baseline SHA-256 + `tests/test_portfolio_opt.py`)
- Never commit verification output over `experiments/*.json`; restore goldens before committing.
- Never re-pin goldens to silence drift (open item: E041/E042 grid artifacts, 29–133 numeric diffs from ill-conditioned tangency QP).
- Do not create `.github/workflows/` CI gates as an automated agent (maintainer template at `.github/workflow-templates/verification-gate.yml`).

## Open Items (from ledger)
- **E041/E042 grid artifacts**: residual 1-ulp QP sensitivity drift. Do not re-pin.
- **E049**: Optimizer determinism fixed (validate on constraints, not solver exit status); residual drift remains.
- **E048**: Cache coverage enforced (every `data.download()` call site must have a pinned cache entry).

---
*Generated at 2026-11-22T05:46:26Z. Update this file before ending work.*
