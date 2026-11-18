# Durable Handoff — Next Agentic Work Session

**Created:** 2026-11-18T11:27:06Z
**Working tree:** clean (no uncommitted changes)
**Branch:** current HEAD

## Open task

None assigned yet. The next agentic session should begin by checking for pending work:
1. `git status --short` — confirm clean tree.
2. `git log --oneline -10` — recent commits.
3. `SEED=42 bash scripts/check.sh` — convention robustness check (~seconds, offline).
4. If the verification suite was interrupted, run `SEED=42 python3 run_all_verification.py --restore-only` to recover golden artifacts under `experiments/`.

## Project context

Quantitative-strategy research (US equities/futures/macro, 2014–2026). Research phase complete (E001–E043); surviving strategies documented in `ledger/RESEARCH_LEDGER.md`. Canonical artifacts live in `experiments/*.json` and are guarded by `ledger/golden_baseline.json` — do not let a verification run overwrite them.

Key conventions:
- Always run with `SEED=42`.
- `QUANT_RESEARCH_OFFLINE=1` during verification (no live yfinance downloads).
- Do not commit verification output.

Commands:
- `make check` / `make verify` / `make verify-quick` / `make verify-extended` / `make verify-full`
- Individual drivers: `experiments/run_e0XX.py`

<details>
See AGENTS.md for full baseline-integrity, reproducibility, and lint conventions.
</details>
