# HANDOFF - Timestamped for Next Agentic Session

**Handoff Created:** 2026-10-29T11:37:44Z
**Session:** checkpoint de0f191 (chore(kilo): checkpoint agent session)
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Branch:** main
**Working Dir:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

---

## Current State

- **Research phase:** Complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`
- **Baseline integrity:** Critical. `experiments/*.json` are canonical goldens. Never leave verification half-finished.
- **Git status:** Clean working tree (recent commits are kilo checkpoints)
- **Last checkpoint:** de0f191

---

## INITIAL TASK FOR NEXT SESSION (CLEAR & ACTIONABLE)

**Priority 1: Verify clean baseline state**
```bash
SEED=42 bash scripts/check.sh
```
This runs convention-robustness check + template validation + golden integrity checks. Must pass with no failures.

**If check.sh reports golden mismatch or stale snapshot:**
```bash
# Recover goldens from HEAD
SEED=42 python3 run_all_verification.py --restore-only
# Or manually: git checkout -- experiments/
```
**Do NOT re-pin goldens** as side effect of verification. Only re-pin if you have explicit justification and follow `ledger/golden_baseline.json` process via `scripts/check_golden_baseline.py --update`.

**Priority 2: Understand current research state**
- Read `ledger/RESEARCH_LEDGER.md` for E001-E043 outcomes and open items
- Review `AGENTS.md` "Baseline Integrity" and "Reproducibility" sections (critical gotchas)
- Note: E041 has known optimizer-determinism drift (133 numeric diffs) - do NOT silence by re-pinning

**Priority 3: Determine next work**
Based on ledger, identify if there are open follow-ups (E044+). If none obvious, confirm repo is in clean reproducible state. Do not start new experiments without pre-registration.

---

## Important Constraints & Reminders

- **Always use SEED=42** for reproducibility
- **Verification overwrites experiments/** temporarily - backup/restore is automatic but must complete
- **Offline mode:** `QUANT_RESEARCH_OFFLINE=1` enforced in verification; cached data required (see `ledger/data_baseline.json`)
- **Convention:** close-to-close v1.2.3 primary; overnight decomposition reported
- **No commits of verification output** - restore first
- **CI workflow cannot be created by agents** - template exists at `.github/workflow-templates/verification-gate.yml`

---

## Quick Commands Reference

```bash
# Fast check
SEED=42 make check

# Full verification (if needed)
SEED=42 make verify-full

# Individual experiment
SEED=42 python3 experiments/run_e042.py --n-sim 50

# Check data coverage
python3 scripts/check_data_coverage.py
```

**Handoff complete. Start with Priority 1 above.**
