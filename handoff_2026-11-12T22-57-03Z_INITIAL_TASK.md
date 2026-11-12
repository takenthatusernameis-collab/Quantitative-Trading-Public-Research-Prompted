# Initial Task — Next Agentic Work Session

**Handoff timestamp:** 2026-11-12T22:57:03Z
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`
**Git:** `main` @ `7b0c0da9` (`chore(kilo): checkpoint agent session`), in sync with `origin/main`
**Working tree at handoff:** clean (no tracked/untracked changes). `.verify_snapshot/` absent.

## Project state
- Independent reproducible quantitative-strategy research on 2014–2026 US equities, futures, and macro data (pre-registered, falsification-first). **Research phase complete (E001–E043).**
- Authoritative records: `ledger/RESEARCH_LEDGER.md`. Canonical artifacts: `experiments/*.json` with integrity pinned in `ledger/golden_baseline.json` and data in `ledger/data_baseline.json` (+ pinned vintages/caches).
- Supersedes prior handoff: `handoff_2026-11-12T22-56-30Z_INITIAL_TASK.md` (same repo state).

## Initial task for the next session
1. **Establish baseline integrity before any changes**
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   Confirms golden cleanliness/baselines, data coverage, compile/tests, and conventions. If it reports mismatch, restore/fix before committing — do not re-pin to silence.
2. **If verification/reproduction is explicitly requested**, run with `SEED=42` (see `AGENTS.md`): `make verify-quick` / `make verify-extended` / `make verify-full`. Suites overwrite and restore `experiments/*.json`; never leave a run half-finished. Recover with `SEED=42 python3 run_all_verification.py --restore-only` (or restore pinned artifacts per `AGENTS.md`).
3. **Review context, then take only user-directed work**
   - Read: `AGENTS.md`, `ledger/RESEARCH_LEDGER.md`, and recent durable handoffs.
   - Proceed with maintenance or new research consistent with completed phase and project conventions. Do not invent work, change pre-registered gates/outcomes, or modify golden/baseline artifacts without explicit direction.

## Critical guardrails
- **Reproducibility:** always `SEED=42`; use pinned data vintages/caches (no live-network dependence in verification paths).
- **Goldens/baselines:** never replace `experiments/*.json` or re-pin `ledger/golden_baseline.json`/`ledger/data_baseline.json` as a side effect of verification. Re-pin only for genuine, reviewed changes with ledger justification.
- **Known drift:** E041/E042 grid artifacts have documented 1-ulp optimizer sensitivity (`AGENTS.md`, ledger E049/open item) — do not re-pin to silence.

## Pending work
- No explicit pending tasks recorded. Confirm baseline health, then await/execute user-directed work consistent with project conventions.
