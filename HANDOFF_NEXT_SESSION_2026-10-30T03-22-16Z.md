# Handoff: Next Agentic Work Session
**Timestamp:** $(date -u +%Y-%m-%dT%H:%M:%SZ)
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Working Dir:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## CLEAR INITIAL TASK (Start Here)
Establish a clean baseline and confirm verification state before making any changes.

### Step 1: Verify baseline integrity (required)
```bash
cd /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
SEED=42 bash scripts/check.sh
```
- Must pass. This runs `check_goldens_clean.py` and `check_golden_baseline.py` (first-class guards).
- If it reports a golden mismatch or stale snapshot, **do not proceed**. Restore first:
  - `SEED=42 python3 run_all_verification.py --restore-only`
  - or `git checkout -- experiments/` (see AGENTS.md for pinned-baseline caveats)

### Step 2: Get oriented
- Read `ledger/RESEARCH_LEDGER.md` (focus recent entries E048–E049: cache coverage + optimizer determinism)
- Skim `AGENTS.md` for constraints (SEED=42, snapshot rules, no re-pinning to silence drift)

### Constraints (critical)
- **Never** leave `run_all_verification.py` half-finished. Snapshots live in `.verify_snapshot/` (gitignored) with `ACTIVE.json` PID tracking.
- **Don't re-pin goldens** to silence numeric drift (E041/E042 show 1-ulp sensitivity; E049 fixed gating but numeric drift remains).
- **Cache coverage is enforced** (`scripts/check_data_coverage.py`) — unpinned inputs fail hard under `QUANT_RESEARCH_OFFLINE=1`.
- **Use `SEED=42`** for all runs.
- **Don't commit verification output**.

### If clean
Proceed with the user's next request. If baseline is dirty/unrecoverable, fix it before any modifications.

---
**Created by:** current session
**Purpose:** Durable handoff for next agentic work session
