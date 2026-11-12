# Initial Task — Next Agentic Work Session

**Handoff timestamp:** 2026-11-12T22:55:44Z
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Git HEAD:** `63b581af50255fc57d27cad7a098b9b9818cec64` (2026-11-12 22:01:26 +0000, "chore(kilo): checkpoint agent session") on `main`, in sync with `origin/main`
**Working tree at handoff:** clean (0 tracked modifications / 0 untracked). `.verify_snapshot/` absent — no interrupted verification run to recover.

## Project state
- Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data.
- **Research phase complete (E001–E043).** Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.
- Canonical artifacts: `experiments/*.json` (138 tracked: 107 pinned goldens + 31 drivers). Integrity pinned in `ledger/golden_baseline.json` (107) and `ledger/data_baseline.json` (35 data inputs).
- Supersedes prior durable handoff: `handoff_2026-11-12T22-54-35Z_INITIAL_TASK.md` (same HEAD).

## Initial task for the next session
1. **Confirm baseline integrity before any changes:**
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   This runs golden cleanliness, golden baseline fingerprints, data coverage, py_compile/tests, and convention checks. **Do not commit if it reports mismatches.**
2. **If reproduction/verification is requested:** run
   - `SEED=42 python3 run_all_verification.py` (`make verify-quick`, ~8 min), or
   - `SEED=42 python3 run_all_verification.py --extended` / `--full` as needed (see `AGENTS.md`).
   The suite overwrites `experiments/*.json` during runs and restores them; **never leave a run half-finished**. Recovery: `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned artifacts per `AGENTS.md`).
3. **Read context before proposing work:** `AGENTS.md`, `ledger/RESEARCH_LEDGER.md`, and recent handoffs in repo root. Proceed only with user-directed research or maintenance consistent with the completed research phase and project conventions.

## Critical conventions / guardrails
- **Reproducibility:** always `SEED=42`. Use pinned data vintages/caches; no live network dependence in verification paths.
- **Goldens/baselines:** do not replace/refresh `experiments/*.json` or re-pin `ledger/golden_baseline.json` as a side effect of verification. Genuine, reviewed changes only (`python3 scripts/check_golden_baseline.py --update`). New data inputs require commit + `python3 scripts/check_data_coverage.py --update`.
- **Pre-registration:** new experiments must state gates, falsification expectations, and sensitivity handling before execution; sensitivity grids are reported, not gated. Record negative results honestly (REJECTED/PARTIAL).
- **Known drift:** E041/E042 grid artifacts have documented 1-ulp/ill-conditioned optimizer sensitivity (`AGENTS.md`, ledger E049/open item) — **do not re-pin to silence**.

## Pending work
- No explicit pending tasks recorded in this handoff. Confirm baseline health, then take user-directed work consistent with project conventions.
