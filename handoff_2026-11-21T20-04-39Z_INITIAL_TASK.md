# Agentic Work Session Handoff — Initial Task

**Timestamp**: 2026-11-21T20:04:39Z
**Session ID**: Initial handoff for next agentic work session
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Project Context

Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data. Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.

Canonical artifacts: `experiments/*.json` are committed golden baselines. The verification suite backs them up before re-running and restores them afterward — never leave a verification run half-finished.

## Initial Task for Next Session

**Primary objective:** Verify repository integrity and establish a clean baseline before making any changes.

### Concrete steps (in order)

1. **Check git state**
   ```bash
   git status --short
   ```
   Ensure no unexpected modifications to `experiments/`, `ledger/`, or `data/`. If `experiments/` differ from HEAD, restore first:
   ```bash
   git checkout -- experiments/
   ```

2. **Run fast integrity check**
   ```bash
   SEED=42 bash scripts/check.sh
   # or
   make check
   ```

3. **Run quick verification (recommended)**
   ```bash
   SEED=42 python3 run_all_verification.py
   # or
   make verify-quick
   ```
   If interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only`.

4. **Review results**
   - If all checks pass: repo is clean and reproducible. Await the user's next requested change.
   - If failures occur: follow `AGENTS.md` guardrails. Do **not** re-pin goldens/data as a side effect of verification.

## Key Constraints & Guardrails

- **Always use `SEED=42`** for verification/runs.
- **Never commit verification output.** Restore `experiments/` before committing.
- **Golden baseline is authoritative.** Replacing artifacts requires explicit re-pinning (`scripts/check_golden_baseline.py --update`).
- **Offline by default in verification** (`QUANT_RESEARCH_OFFLINE=1`). Missing pinned caches must fail hard.
- **CI workflow:** Cannot be created by agents. Template at `.github/workflow-templates/verification-gate.yml`.

## Key Pointers

- Ledger: `ledger/RESEARCH_LEDGER.md`
- Golden pin: `ledger/golden_baseline.json`
- Data pin: `ledger/data_baseline.json`
- Verification: `run_all_verification.py`, `scripts/check.sh`, `make verify-quick/extended/full`
- Conventions: `AGENTS.md`

**Ready to start at step 1.**
