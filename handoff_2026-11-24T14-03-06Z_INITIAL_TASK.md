# Agentic Work Session Handoff

**Timestamp**: 2026-11-24T14:03:06Z
**Session ID**: Initial handoff created at session start
**Project**: Quantitative-Trading-Public-Research-Prompted
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Status

**Research Phase**: COMPLETE (E001–E043)
**Surviving Validated Strategies**: Documented in `ledger/RESEARCH_LEDGER.md`
**Verification Suite**: Available via `make verify-quick`, `make verify-extended`, `make verify-full`

## Initial Task for Next Session

Run the fast convention-robustness check + template validation to confirm current state:

```bash
SEED=42 bash scripts/check.sh
#   or
make check
```

This runs `py_compile` on changed files, `scripts/check_goldens_clean.py` (working tree vs HEAD), `scripts/check_golden_baseline.py` (committed artifacts vs pinned SHA-256), `tests/test_portfolio_opt.py`, and `scripts/check_data_coverage.py`. All steps must pass before any further work.

## Critical Integrity Notes

1. **Golden Files**: `experiments/*.json` are canonical research artifacts. The verification suite overwrites them during re-run and restores afterward. **Never leave a verification run half-finished**.
2. **Recovery**: If interrupted, use `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`.
3. **Baseline Protection**: Do **not** re-pin E041/E042 to "silence" tolerance violations — none remain per ledger E050. Re-pinning only for deliberate code changes altering published numbers, recorded in the ledger first.
4. **Offline Mode**: Verification suite runs with `QUANT_RESEARCH_OFFLINE=1`; missing cache entries fail hard.
5. **No Commits**: Do not commit verification output. Do not commit unless explicitly asked.

## Further Verification (after `make check` passes)

```bash
# Quick full verification (~8 min)
SEED=42 python3 run_all_verification.py
#   or
make verify-quick
```

## References

- `ledger/RESEARCH_LEDGER.md` — surviving strategies and key fixes (E049, E050, E048, E045)
- `AGENTS.md` — project commands, conventions, reproducibility rules

---

*This handoff was created automatically at session initialization. Update as work progresses.*
