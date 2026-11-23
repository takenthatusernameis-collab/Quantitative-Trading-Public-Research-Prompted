# Agentic Work Session Handoff

**Timestamp**: 2026-11-23T00:34:24Z
**Session**: Initial handoff for next agentic work session
**Project**: Quantitative-Trading-Public-Research-Prompted

## Project Status

Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Verification Commands (SEED=42)

```bash
# Fast convention-robustness check + template validation (~seconds, offline)
SEED=42 bash scripts/check.sh
# or
make check

# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py
# or
make verify-quick

# Extended verification (~21 min)
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min)
SEED=42 python3 run_all_verification.py --full
```

## Critical Notes for Next Session

1. **Golden files**: `experiments/*.json` are canonical artifacts. Verification suite backs them up to `.verify_snapshot/` and restores after. Never leave a verification run half-finished.
2. **Baseline integrity**: If `scripts/check.sh` reports golden mismatch, fix before committing. Use `git checkout -- experiments/` to restore, or `python3 run_all_verification.py --restore-only`.
3. **Cache coverage**: Enforced invariant. `scripts/check_data_coverage.py` requires all data inputs pinned in `ledger/data_baseline.json`. Add new data by committing file and re-pinning with `--update`.
4. **Known drifts** (extended verification):
   - E030: 28 numeric diffs on near-zero quantities (reproduces 0 diff since 2026-10-20 with pinned panel)
   - E041: 133 numeric diffs (ill-conditioned QP, 1-ulp sensitivity), 3 structural diffs resolved — **do not re-pin**
5. **Optimizer determinism**: `src/portfolio_opt.py` validates on problem constraints, not solver exit status. Tangency QP remains ill-conditioned.
6. **No uncommitted verification output**: working tree must not hold driver output in place of goldens.

## Next Steps (if any)

- Review `ledger/RESEARCH_LEDGER.md` for surviving strategies and open items
- Run `make check` to verify current state
- Consider any new experiment pre-registrations

---

*This handoff is durable and survives session closure. Next agent should read this file first.*
