# Agentic Work Session Handoff

**Timestamp:** 2026-11-10T09:24:19Z
**Project:** Quantitative-Trading-Public-Research-Prompted
**Workspace:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

---

## Initial Task for Next Session

**Objective:** Continue quantitative strategy research on 2014–2026 US equities, futures, and macro data. All experiments are pre-registered with falsification expectations and promotion gates. Research phase complete (E001–E043). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.

**Next Steps:**
1. Run verification suite to ensure reproducibility: `SEED=42 python3 run_all_verification.py --extended`
2. Review `ledger/RESEARCH_LEDGER.md` for surviving validated strategies
3. Consider new experiment designs with pre-registration
4. Check `scripts/check.sh` passes before committing any changes

**Key Commands:**
- Fast check: `make check` or `SEED=42 bash scripts/check.sh`
- Quick verification: `make verify-quick`
- Extended verification: `make verify-extended`
- Full verification: `make verify-full`

**Important Notes:**
- Golden files in `experiments/*.json` are canonical artifacts - never commit verification output
- Use `SEED=42` for all runs
- Data cached in `data/` (gitignored except pinned vintages)
- If verification interrupted: `SEED=42 python3 run_all_verification.py --restore-only`