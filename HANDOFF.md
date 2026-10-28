# HANDOFF — Next Agentic Work Session

**Timestamp (UTC):** 2026-10-28T12:31:22Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Branch/State:** Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
**Working tree:** Clean baseline expected; verification suite exists but must not leave goldens half-modified.

## Project Snapshot (read first)
- **Ledger (source of truth):** `ledger/RESEARCH_LEDGER.md` — lists completed experiments, REJECTED/PARTIAL/VALIDATED, gates, and open items (notably E049 optimizer determinism / E041 drift).
- **Golden baseline:** `ledger/golden_baseline.json` (SHA-256 fingerprints). `scripts/check_golden_baseline.py` enforces it. Never re-pin as a side effect of verification.
- **Data coverage:** `ledger/data_baseline.json` + `scripts/check_data_coverage.py` enforce cached inputs are committed/pinned (prevents live yfinance non-reproducibility).
- **Verification guards:** `scripts/check_goldens_clean.py` (HEAD vs working tree), snapshot backup in `.verify_snapshot/` with `ACTIVE.json`, recovery via `run_all_verification.py --restore-only`.

## Immediate Priority Task (clear initial task)
**Verify baseline integrity and environment reproducibility before making changes.**

Do this in order:
1. **Check goldens/data coverage** (fast, offline-safe):
   ```bash
   SEED=42 python3 scripts/check_golden_baseline.py
   SEED=42 python3 scripts/check_data_coverage.py
   SEED=42 python3 scripts/check_goldens_clean.py
   ```
2. **Run quick convention check**:
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   (Runs py_compile + tests + goldens clean + golden baseline + data coverage + convention robustness.)
3. **If anything is dirty from a previous interrupted run, recover first:**
   ```bash
   SEED=42 python3 run_all_verification.py --restore-only
   ```
   Only proceed to re-run verification if step 1–2 are clean and you need to validate changes.

## Known Open/Watch Items
- **E049 / E041 drift:** Optimizer determinism fixed in logic but tangency QP remains ill-conditioned; E041 still shows numeric drift (133 diffs) exceeding 1e-4. Do **not** re-pin goldens to silence this — see ledger.
- **Verification runs are destructive to working tree:** `run_all_verification.py` backs up `experiments/` to `.verify_snapshot/` and restores after. Never leave a run interrupted. A live run is marked by `ACTIVE.json`.
- **Data pins:** E029 fundamentals pinned in `data/fundamentals/` + `data/fundamentals_vintages.json`; 2026-10-11/12 vintages pinned. Cache hit is calendar-independent.

## Files to Read First
- `AGENTS.md` (full conventions, verification commands, guards)
- `ledger/RESEARCH_LEDGER.md` (current status and open items)
- `ledger/golden_baseline.json` and `ledger/data_baseline.json` (what's pinned)
- `run_all_verification.py` (understand backup/restore and blocks)
- `scripts/check.sh` (gate order)

## Suggested Next Action (concrete)
Start with steps 1–2 above. If clean, summarize baseline state (golden SHA match, data coverage OK, check.sh PASS) and report to user. If any guard fails, **restore goldens first** (`--restore-only`) before investigating. Do not modify `experiments/*.json` or re-pin baselines without explicit instruction and updating the ledgers via the provided `--update` paths only when justified.

**Handoff complete.** Next session should begin at "Immediate Priority Task" above.