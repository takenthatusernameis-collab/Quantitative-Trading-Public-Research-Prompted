# Durable Handoff — Initial Task for the Next Agentic Work Session

**Timestamp (UTC):** 2026-11-16T01:50:28Z
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**HEAD:** `879b3896` (`chore(kilo): checkpoint agent session`) on `main`
**Remote:** re-confirm `main` vs `origin/main` before any push.

## Project state (at handoff)

- Research phase **complete (E001–E051)**; pre-registered experiments with fixed gates/falsification. Surviving validated strategies in `ledger/RESEARCH_LEDGER.md`.
- v1.2.3 convention: **close-to-close primary**; overnight decomposition reported alongside.
- `experiments/*.json` are **canonical golden artifacts**. Never capture or commit verification output as a new baseline.
- Working tree: clean of research changes; only pre-existing modified tracked `__pycache__/*.pyc` files are present (`scripts/`, `src/`, `tests/__pycache__/`). **Do not commit .pyc files.**
- No interrupted verification: `.verify_snapshot/` and `.verify_reports/` absent; goldens intact.
- Baseline integrity (re-confirmed this session): `SEED=42 bash scripts/check.sh` → exit 0, `=== All checks passed ===`.
- Prior handoff: `handoff_2026-11-16T01-49-35Z_INITIAL_TASK.md`.

## Initial task for the next agent (do first, in order)

1. **Dependencies (fresh sandbox only):**
   ```bash
   python3 -m pip install --break-system-packages -r requirements.txt
   ```
2. **Confirm baseline integrity (fast, offline):**
   ```bash
   SEED=42 bash scripts/check.sh        # or: make check
   ```
   Expect exit 0 and `=== All checks passed ===`.
3. **If integrity/baseline issues are reported, recover deliberately:**
   - Dirty goldens / stale `.verify_snapshot/` / interrupted run:
     `SEED=42 python3 run_all_verification.py --restore-only`
     (or restore pinned artifacts per `ledger/golden_baseline.json`).
     Never leave a verification run half-finished; never commit captured verification output.
   - Golden fingerprint mismatch: resolve intentionally against `ledger/golden_baseline.json` / `ledger/data_baseline.json`. **Do not re-pin** as a side effect of verification.
   - Re-run `SEED=42 bash scripts/check.sh` after recovery.
4. **Then stop and await explicit user direction.**
   - Do not run long verification (`make verify-quick/extended/full`), invent experiments, modify gates/outcomes, or alter research artifacts unprompted.
   - Do not modify or re-pin `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`, `src/`, `scripts/`, `tests/`, or `data/` without explicit request and justified diff.

## Quick reference

```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 run_all_verification.py                # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended     # +18 drivers (~21 min)
SEED=42 python3 run_all_verification.py --full         # E042 n_sim=50 + 96-config grid
SEED=42 python3 verify_convention_robustness.py
SEED=42 python3 run_all_verification.py --restore-only
```

## Open items (do not resolve silently)

- **E041:** 133 numeric diffs remain (1-ulp QP sensitivity) post optimizer fix; decision REJECTED 3/5 unchanged. **Do not re-pin.** (ledger E049)
- **E042 lead:** PARTIAL (3/5 gates); min-var confirmatory (n_sim=50) passes convention robustness but tangency grid drifts. (ledger E049)
- **CI gate:** only template `.github/workflow-templates/verification-gate.yml` exists; maintainer must create real workflow via GitHub UI.
- **Promotion discipline:** any sensitivity-grid-clearing config requires a dedicated pre-registered confirmatory run with full placebo before promotion.

## Artifact

- **Primary:** `handoff_2026-11-16T01-50-28Z_INITIAL_TASK.md`
- Generic canonical handoff pointers repointed to this file; mirrored to `handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/`.

*Generated 2026-11-16T01:50:28Z. No research artifacts modified.*
