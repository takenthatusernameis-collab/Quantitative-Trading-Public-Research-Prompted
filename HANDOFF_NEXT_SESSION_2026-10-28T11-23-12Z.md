# HANDOFF_NEXT_SESSION_2026-10-28T11-23-12Z

**Created:** 2026-10-28T11-23-12Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Working tree:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**State:** Research phase complete (E001–E043). Surviving strategies documented in `ledger/RESEARCH_LEDGER.md`.

## Initial Task (do this first)

Verify baseline integrity. Do **not** re-run experiments to "refresh" goldens unless explicitly asked.

### 1) Run the convention-robust fast check (required)

```bash
SEED=42 bash scripts/check.sh
# or
make check
```

Expected: all checks pass (py_compile, `scripts/check_goldens_clean.py`, `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`, portfolio opt tests).

If any guard fails, **stop and recover**. See AGENTS.md "Baseline Integrity". Never re-pin as a side effect of verification. Recovery:
- Stale snapshot / half-finished run: `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`).
- Goldens differ from `ledger/golden_baseline.json`: do **not** re-pin via the suite; only `python3 scripts/check_golden_baseline.py --update` if explicitly justified and documented.
- Data coverage fails: commit missing files and re-pin with `python3 scripts/check_data_coverage.py --update`.

### 2) Sanity-check verification path (optional, recommended)

```bash
SEED=42 python3 run_all_verification.py           # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended # extended (~21 min)
```

Do **not** commit verification output. If interrupted, recover with `--restore-only`.

## Known Open Items

- **E041 numeric drift (ledger E049):** optimizer now validates on constraints (not solver status); structural drift fixed. Remaining ~133 numeric diffs are 1-ulp sensitivity of an ill-conditioned tangency QP (> 1e-4 tolerance). Do **not** silence by re-pinning.
- **CI workflow:** `.github/workflows/verification-gate.yml` cannot be created by agents. Use `.github/workflow-templates/verification-gate.yml` as template; a maintainer must create the actual workflow.

## Read First

- `AGENTS.md` — full commands, guards, reproducibility notes
- `ledger/RESEARCH_LEDGER.md` — research state and open items
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints
- `scripts/check.sh` — the gate to satisfy

## If No Explicit Task Beyond This Handoff

Run step (1) above and report status only. Do **not** make speculative changes. Treat committed `experiments/*.json` as the authoritative record.

**End of handoff.**
