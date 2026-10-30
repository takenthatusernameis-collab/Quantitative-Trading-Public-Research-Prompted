# HANDOFF: Next Agentic Work Session

**Created:** 2026-10-30T00:31:49Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Branch:** main (verify with `git log --oneline -1`).

## Baseline state — UNVERIFIED THIS SESSION (re-verify before any work)

- `SEED=42 bash scripts/check.sh` expected: exit 0, "=== All checks passed ===". Treat negative-test FAIL lines as expected fixtures.
- Working tree: should be clean of tracked changes (only `__pycache__/*.pyc` gitignored).
- No `.verify_snapshot/` / `ACTIVE.json` → no interrupted verification run to recover.

## Initial Task (Start Here)

Verify the baseline is clean before any work.

1. Run `SEED=42 bash scripts/check.sh` — must exit 0 with "=== All checks passed ===".
2. Run `git status --short` — confirm clean tree (only `__pycache__/*.pyc`).
3. If an interrupted verification left dirty `experiments/*.json`, restore: `SEED=42 python3 run_all_verification.py --restore-only`.

Do not re-pin goldens to silence drift. Keep committed goldens authoritative.

Read `AGENTS.md` and `ledger/RESEARCH_LEDGER.md` first.

## Known Open Items (Do Not "Fix" By Re-Pinning)

- E041 numeric drift ~133 diffs (1-ulp sensitivity of ill-conditioned QP). Do not re-pin.
- E042 grid artifacts: 1-ulp sensitivity; do not re-pin.
- E030 numeric diffs on near-zero quantities. Do not re-pin.
- Data coverage: inputs must stay tracked/pinned in `ledger/data_baseline.json`.
- Pinned fundamentals/vintages canonical.
