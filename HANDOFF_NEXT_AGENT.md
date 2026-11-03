# HANDOFF — Timestamped for next agentic work session

- Timestamp (UTC): 2026-11-03T05:21:57Z
- Repo: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
- Branch: (unknown from env; see git log below)
- Last commits: a56427e, 2f404e5, 4e47425, 79c3c63, 153b49b (chore(kilo): checkpoint agent session)

## Current state
- Working tree clean (git status short empty).
- No active `.verify_snapshot/` (no verification run in progress).
- Research phase complete (E001–E043). Surviving validated strategies in `ledger/RESEARCH_LEDGER.md`.
- Canonical artifacts: `experiments/*.json` committed; verification suite backs up/restores them. Do NOT re-pin goldens via suite runs.

## Immediate context (important constraints)
- Always use `SEED=42`.
- Baseline integrity guards are strict: `scripts/check_goldens_clean.py` (HEAD vs tree), `scripts/check_golden_baseline.py` (tree vs `ledger/golden_baseline.json` SHA-256). Never replace baselines via verification runs; to re-pin require explicit `--update` with justification recorded.
- `QUANT_RESEARCH_OFFLINE=1` is enforced during verification for driver re-runs; missing data cache entries fail hard (`scripts/check_data_coverage.py`).
- E029/E030 offline reproducible via pinned data/fundamentals; E041/E042 have known QP 1-ulp drift (environment/solver dependent) — do not silence by re-pinning.
- No GitHub workflow can be created by agents (`.github/workflows/` restored/cleaned by controller).

## Clear initial task message for next agent
**TASK:** Verify repo integrity and pick up from a clean baseline before making changes.

### Steps
1. **Sanity checks (must pass):**
   - `SEED=42 bash scripts/check.sh` (convention-robustness + template validation + goldens clean + golden baseline + tests).
   - If anything fails, do NOT modify experiments/ or ledger pins unless the failure is a genuine bug you can fix without contaminating baselines; read `AGENTS.md` "Baseline Integrity" first.

2. **Understand current research state:**
   - Read `ledger/RESEARCH_LEDGER.md` (E001–E043 summary, gates, decisions REJECTED/PARTIAL/VALIDATED).
   - Skim `README.md` and `AGENTS.md` for reproduction/verification expectations.

3. **Choose next concrete action (pick ONE):**
   - **Option A (safe):** If `scripts/check.sh` passes, run a quick verification to confirm reproducibility: `SEED=42 python3 run_all_verification.py` (quick). Review summary; do not commit artifacts if working tree becomes dirty due to run.
   - **Option B (targeted):** Address any open items noted in ledger (look for "open item", TODO, or E049 notes). Only change code/data with pre-registered rationale and tests.
   - **Option C (exploratory):** If asked for new experiment, follow pre-registration discipline (gates/falsification/sensitivity) and never move goalposts.

### Rules for next agent
- Do **not** run verification in background while leaving snapshots unattended; if interrupted, recover with `run_all_verification.py --restore-only`.
- Do **not** commit `experiments/*.json` produced by a live verification run. Restore first.
- Follow all instructions in `AGENTS.md`. Use tools directly; avoid conversational preamble.
- If uncertain about baseline vs regenerated artifacts, consult `ledger/golden_baseline.json` and `ledger/data_baseline.json`.

## Quick commands
```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 run_all_verification.py  # quick
SEED=42 python3 run_all_verification.py --restore-only  # if dirty from interrupted run
```
