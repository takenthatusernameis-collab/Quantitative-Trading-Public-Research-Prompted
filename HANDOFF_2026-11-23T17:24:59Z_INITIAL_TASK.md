# Agentic Work Session Handoff — 2026-11-23T17:24:59Z

**Timestamp**: 2026-11-23T17:24:59Z
**HEAD**: `42184c4599dc877585060c2582b8b9f4ecb3735e` on `main`
**Project**: Quantitative-Trading-Public-Research-Prompted
**Research phase**: COMPLETE (E001–E043). Surviving validated strategies in `ledger/RESEARCH_LEDGER.md`.

---

## Immediate task for the next session

Run the full verification suite (the standing open item). Do NOT treat writing another handoff as the work.

```bash
pip install -r requirements.txt          # deps are not provisioned
SEED=42 python3 run_all_verification.py --extended   # ~21 min
```

- Report drift precisely using `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json` (driver, field, magnitude).
- Do NOT re-pin goldens to silence tolerance violations (none should remain).
- After the run, confirm `git status --porcelain` is clean; use `--restore-only` if the run dies mid-flight.

## Prioritized real-work list (do in order; stop at the first substantive one)

1. Run `SEED=42 python3 run_all_verification.py --extended` (above).
2. If drift persists, address E049/E041/E042 ill-conditioned-QP root cause (do not re-pin).
3. Propose (do NOT execute) the handoff cleanup: `.gitignore` rule for `*_INITIAL_TASK.md` + mirror dirs (`handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/handoff/`), `git rm --cached` the accumulated handoff files/symlinks. Surface to user for approval before executing.
4. Only if 1–3 are done/declined: explicitly-requested pre-registered research. Research phase is closed; do not invent post-hoc experiments.

## Critical invariants

- Baseline integrity: suite overwrites `experiments/*.json` mid-run and restores after; never leave a run half-finished (`--restore-only`).
- Cache coverage: every `data.download()` must have a committed SHA-256-pinned cache file (enforced by `scripts/check_data_coverage.py`).
- Seed always `SEED=42`; optimizer validates on constraints, never solver exit status (ledger E049/E050).
- Close-to-close primary convention; overnight decomposition reported alongside.

## Key file map

| Path | Purpose |
|------|---------|
| `ledger/RESEARCH_LEDGER.md` | Experiment history, dispositions |
| `ledger/golden_baseline.json` | SHA-256 fingerprints of pinned golden artifacts |
| `experiments/*.json` | Canonical research artifacts (goldens) |
| `run_all_verification.py` | Verification orchestrator (`--extended`, `--full`, `--restore-only`) |
| `scripts/check.sh` | Fast offline gate |
| `src/portfolio_opt.py` | Tangency optimizer (E050 exact active-set enumeration) |
| `data/vintages.json`, `data/fundamentals_vintages.json` | Pinned data vintages |

---

*Handoff at 2026-11-23T17:24:59Z. The prior handoff `HANDOFF_2026-11-23T17-24-34Z_INITIAL_TASK.md` exists; this is the current durable copy.*
