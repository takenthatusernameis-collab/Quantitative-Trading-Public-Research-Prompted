# Initial Task / Handoff — Next Agentic Session

**Timestamp (UTC):** 2026-11-17T22:35:21Z
**Repository:** Quantitative-Trading-Public-Research-Prompted
**HEAD:** 274aea03 chore(kilo): checkpoint agent session

## Project status
- Research phase **complete** (E001–E043). Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.
- `experiments/*.json` are canonical golden artifacts; verification must never be left half-finished (it overwrites then restores them).

## Immediate task for next session
1. **Baseline integrity (required before other work):**
   - `SEED=42 make check` (runs convention checks, golden cleanliness/baseline, data coverage, template/optimizer tests; offline, fast).
   - If it reports a golden mismatch or stale `.verify_snapshot/ACTIVE.json`, **do not commit** — recover with `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/` only when HEAD holds the authoritative baseline).
2. **If check is clean:** run `SEED=42 make verify-quick` (~8 min) for a full quick verification cycle. Use `make verify-extended` / `make verify-full` only when needed.
3. **After any interrupted verification:** run `--restore-only` before committing; never capture verification output as new goldens.

## Key constraints / caveats
- Always set `SEED=42`. Verification re-executes drivers with `QUANT_RESEARCH_OFFLINE=1`; missing/unpinned cache entries are hard failures (see `ledger/data_baseline.json`, `data/vintages.json`).
- Re-pinning goldens (`scripts/check_golden_baseline.py --update`) requires explicit justification and must appear in the diff — never re-pin to silence drift as a side effect of verification.
- Known extended-verification drift: **E041** has 133 numeric diffs from 1-ulp ill-conditioned QP sensitivity (ledger E049); do **not** re-pin E041. Most other extended drivers reproduce with 0 diffs (see `AGENTS.md`).
- Do not modify `.github/workflows/` via automation; workflow template lives at `.github/workflow-templates/verification-gate.yml`.

## Pointers
- Commands & invariants: `AGENTS.md`
- Research ledger: `ledger/RESEARCH_LEDGER.md`
- Golden/data pins: `ledger/golden_baseline.json`, `ledger/data_baseline.json`
- Prior durable handoff: `HANDOFF_LATEST.md` (2026-11-17T22:31:23Z)
