# Handoff — Next Agentic Work Session

**Timestamp:** 2026-11-26T03:22:23Z
**Session ID:** (current session)
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project State

- **Phase:** Research phase complete (E001–E043)
- **Validated strategies:** Documented in `ledger/RESEARCH_LEDGER.md`
- **Golden artifacts:** `experiments/*.json` (canonical baseline, pinned in `ledger/golden_baseline.json`)
- **Data cache:** Pinned vintages in `data/vintages.json` (2026-10-12) and `data/fundamentals_vintages.json` (E029 fundamentals)

## Verification Commands (SEED=42)

```bash
# Fast check (~seconds)
make check

# Quick verification (~8 min)
make verify-quick

# Extended verification (~21 min, structural match)
make verify-extended

# Full verification (~15 min, E042 n_sim=50 + 96-config grid)
make verify-full

# Convention robustness only
make verify
```

## Critical Integrity Notes

1. **Never leave verification half-finished** — it overwrites `experiments/*.json` and restores after. If interrupted:
   - `SEED=42 python3 run_all_verification.py --restore-only`
   - or `git checkout -- experiments/`

2. **Golden baseline protection:** `scripts/check_golden_baseline.py` compares artifacts against SHA-256 in `ledger/golden_baseline.json`. Re-pinning requires deliberate ledger entry.

3. **Data coverage invariant:** All `data.download()` call sites must have committed, SHA-256-pinned cache files (enforced by `scripts/check_data_coverage.py`).

4. **Optimizer determinism (E049/E050):** Tangency QP uses exact KKT active-set enumeration (bit-reproducible). Do not re-pin E041/E042 to silence tolerance — no violation exists.

## Key Files to Review

- `AGENTS.md` — full conventions, commands, reproducibility rules
- `ledger/RESEARCH_LEDGER.md` — experiment dispositions (E001–E050)
- `scripts/check.sh` — convention robustness + golden integrity checks
- `run_all_verification.py` — main verification orchestrator

## Next Steps (if any)

- No pending tasks. Session is clean. Next session can run any verification tier or explore ledger entries.