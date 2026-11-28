# INITIAL TASK — Durable Handoff for the Next Agentic Work Session

**Timestamp (UTC): 2026-11-28T00:44:02Z**
**Repository:** Quantitative-Trading-Public-Research-Prompted
**Branch/HEAD:** main — e13b724b3d2e9796427573257cc56972bfe6607a (2026-11-28 00:43:55 +0000) == origin/main
**Working Directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Working Tree:** clean except `src/__pycache__/cache_keys.cpython-312.pyc` (ignored pyc, not a canonical artifact). No `.verify_snapshot/`.

Supersedes `HANDOFF_2026-11-27T23-42-48Z_INITIAL_TASK.md`. This file is the authoritative initial-task message for the next session.

---

## CLEAR INITIAL TASK (do these in order, then stop)

Do **not** re-pin artifacts, overwrite goldens, run the full verification suite unprompted, or write another handoff as a side effect.

1. **Confirm canonical state** — `git log -1 --format="%H"`, `git status --short experiments/ data/ ledger/`, confirm HEAD == origin/main (`e13b724b`), confirm no `.verify_snapshot/` exists (no interrupted run to recover).
2. **Verify goldens and data coverage** —
   `SEED=42 python3 scripts/check_goldens_clean.py` and
   `SEED=42 python3 scripts/check_golden_baseline.py` and
   `SEED=42 python3 scripts/check_data_coverage.py`.
3. **Read `ledger/RESEARCH_LEDGER.md`** — surviving validated strategies (research phase closed E001–E043) and open items.
4. **Fast sanity check (only if directed)** — `SEED=42 bash scripts/check.sh` (offline, seconds).
5. **If this session hands off** — create its own timestamped durable handoff following this pattern (`HANDOFF_YYYY-MM-DDTHH-MM-SSZ_INITIAL_TASK.md` at repo root).

## Key Constraints (from AGENTS.md)

- `experiments/*.json` are committed goldens — verification backs them up and restores them; never commit verification output or leave a run half-finished.
- Golden baseline enforced by `scripts/check_golden_baseline.py` vs `ledger/golden_baseline.json`; data coverage by `scripts/check_data_coverage.py` vs `ledger/data_baseline.json`.
- Optimizer: validate on problem constraints, not solver exit status (`tests/test_portfolio_opt.py`, ledger E049/E050 — closed; E041/E042 drift closed).
- Always use `SEED=42`. Close-to-close is the v1.2.3 primary convention.
- CI workflow cannot be created by automated agents; use local `make check/verify/*`.
- Never re-pin artifacts to silence drift unless following the re-pinning process; the committed golden is authoritative.

## Handoff provenance

Supersedes `HANDOFF_2026-11-27T23-42-48Z_INITIAL_TASK.md`. This file is the authoritative initial-task message for the next session. Written by agent at 2026-11-28T00:44:02Z.
