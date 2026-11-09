# Agentic Work Session Handoff

**Timestamp:** 2026-11-09T03:28:14Z
**Session ID:** Initial handoff for next agentic session
**Project:** Quantitative-Trading-Public-Research-Prompted
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

---

## Project Status Summary

**Research Phase:** COMPLETE (Experiments E001–E043)
**Surviving Validated Strategies:** Documented in `ledger/RESEARCH_LEDGER.md`
**Current Baseline:** Golden artifacts in `experiments/*.json` (canonical research artifacts)

---

## Key Context for Next Session

### Verification Suite Status
- **Fast check** (`make check` / `SEED=42 bash scripts/check.sh`): Convention-robustness + template validation (~seconds, offline)
- **Quick verification** (`make verify-quick`): 8 experiment drivers + batch_run + validate + E042 n_sim=2 (~8 min)
- **Extended verification** (`make verify-extended`): +18 committed drivers, structural match (~21 min)
- **Full verification** (`make verify-full`): E042 n_sim=50 + 96-config sensitivity grid (~15 min)

### Critical Integrity Notes
1. **Golden artifacts** in `experiments/` are overwritten during verification and restored afterward — **never leave a verification run half-finished**
2. **Recovery:** `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
3. **Baseline protection:** `scripts/check_golden_baseline.py` compares tracked artifacts with SHA-256 fingerprints in `ledger/golden_baseline.json` — re-pinning requires explicit `--update` flag
4. **Data cache coverage enforced:** `scripts/check_data_coverage.py` requires every `data.download()` call site to have a committed, SHA-256-pinned cache file

### Known Drift Items (Reporting Only, Not Failures)
- **E030:** 28 numeric diffs on near-zero quantities (ETF panel now pinned, reproduces with 0 diffs since 2026-10-20)
- **E041:** 133 numeric differences (1-ulp sensitivity of ill-conditioned QP in optimizer) — **do not re-pin to silence** (open ledger item E049)
- Extended drift report written to `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json` (gitignored)

### Reproducibility Requirements
- **Seed:** Always `SEED=42` (walk-forward + placebo RNG)
- **Convention:** Close-to-close v1.2.3 primary; overnight decomposition reported alongside
- **Data vintage:** 2026-10-12 pinned in `data/vintages.json`; 2026-10-11 committed for specific experiments
- **E029 fundamentals:** Pinned in `data/fundamentals/` per `data/fundamentals_vintages.json` (offline-reproducible)

---

## Immediate Next Steps / Priorities

1. **Run fast convention check** to verify working tree integrity:
   ```bash
   SEED=42 bash scripts/check.sh
   ```

2. **If check passes**, consider quick verification to validate current state:
   ```bash
   SEED=42 python3 run_all_verification.py
   ```

3. **Review ledger** for open items:
   - `ledger/RESEARCH_LEDGER.md` — surviving strategies and dispositions
   - Open item: E041/E042 optimizer determinism (ill-conditioned QP, 1-ulp sensitivity)

---

## Important Files to Reference

| File | Purpose |
|------|---------|
| `ledger/RESEARCH_LEDGER.md` | Complete experiment log with gates, decisions, evidence |
| `ledger/golden_baseline.json` | SHA-256 fingerprints of canonical experiment artifacts |
| `ledger/data_baseline.json` | SHA-256 fingerprints of pinned data cache files |
| `data/vintages.json` | Pinned data vintage (2026-10-12) |
| `data/fundamentals_vintages.json` | Pinned fundamentals snapshot for E029 |
| `scripts/check_golden_baseline.py` | Baseline integrity guard |
| `scripts/check_data_coverage.py` | Cache coverage enforcement |
| `AGENTS.md` | Project commands, conventions, and verification protocols |

---

## Session Startup Checklist for Next Agent

- [ ] Read `AGENTS.md` for current commands and conventions
- [ ] Run `SEED=42 bash scripts/check.sh` to verify working tree integrity
- [ ] Check `ledger/RESEARCH_LEDGER.md` for latest dispositions
- [ ] Verify no stale `.verify_snapshot/` or interrupted verification runs
- [ ] Confirm `SEED=42` is set for all experiment runs

---

**Note:** This handoff is durable and timestamped. The next agentic session should read this file first to establish context before proceeding with any work.