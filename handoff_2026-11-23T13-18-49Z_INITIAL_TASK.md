# Handoff — Next Agentic Work Session

**Timestamp:** 2026-11-23T13:23:31Z
**Working Directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Project:** Quantitative Trading Public Research (2014–2026 US equities, futures, macro)
**Research Phase:** Complete (E001–E043) — surviving strategies in `ledger/RESEARCH_LEDGER.md`

---

## Current State

- **Verification suite** is the primary workflow: `make check`, `make verify`, `make verify-quick`, `make verify-extended`, `make verify-full`
- **Canonical artifacts:** `experiments/*.json` (backed up to `.verify_snapshot/` during verification, restored after)
- **Golden baseline integrity:** Pinned in `ledger/golden_baseline.json` (SHA-256); `scripts/check_golden_baseline.py` enforces it
- **Data cache coverage:** Enforced invariant — `scripts/check_data_coverage.py` validates every download site against `ledger/data_baseline.json`
- **Reproducibility:** `SEED=42` always; close-to-close v1.2.3 primary convention

---

## Key Commands Reference

```bash
# Convention robustness only (fast, offline)
SEED=42 make check
# or
SEED=42 python3 scripts/check.sh

# Quick verification (~8 min; 8 drivers + batch + validate + E042 n_sim=2)
SEED=42 make verify-quick
# or
SEED=42 python3 run_all_verification.py

# Extended verification (~21 min; quick + 18 more drivers, structural match)
SEED=42 make verify-extended
# or
SEED=42 python3 run_all_verification.py --extended

# Full verification (~15 min; E042 n_sim=50 + 96-config sensitivity grid)
SEED=42 make verify-full
# or
SEED=42 python3 run_all_verification.py --full

# Recovery after interrupted verification
SEED=42 python3 run_all_verification.py --restore-only
# or
git checkout -- experiments/
```

---

## Important Notes for Next Session

1. **Never leave verification half-finished** — it overwrites `experiments/*.json` and must restore them. Use `--restore-only` if interrupted.
2. **Do not re-pin golden baselines** to silence tolerance violations — only deliberate code changes warrant re-pinning (recorded in ledger).
3. **E041/E042 are bit-reproducible** after E050 exact active-set fix (commit `72dc947`); 0 differences at 2026-11-23T05:17Z measurement.
4. **E029/E030 are offline-reproducible** since 2026-10-20 (pinned fundamentals + 16-ETF panel).
5. **CI workflow cannot be created by agents** — template at `.github/workflow-templates/verification-gate.yml`; maintainer must create via GitHub UI.
6. **No separate linter** — `python3 -m py_compile` on changed files.

---

## Next Steps / Suggested Work

- Run `make check` to validate current state
- Run `make verify-quick` for fast regression check
- If extending research: pre-register new experiment with falsification expectations before execution
- Review `ledger/RESEARCH_LEDGER.md` for surviving strategies and promotion gates

---

*This handoff was created automatically at session start. Update as needed.*