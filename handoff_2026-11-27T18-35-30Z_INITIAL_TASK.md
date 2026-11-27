# Durable Handoff — Initial Task Message

**Created (UTC):** 2026-11-27T18:35:30Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**Working directory:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Branch / HEAD:** main — `fda4d565aaffddf38d3f6f17246c2a4be62baaa5` (== origin/main)
**Working tree:** clean for canonical artifacts (`experiments/`, `data/`); no `.verify_snapshot/`; no pending recovery.

## Initial task for the next agentic work session

**CLEAR INITIAL TASK:** *Leave a timestamped, clear initial task message for the
next agentic work session in a durable handoff.*

Concretely, the next session should:

1. Re-verify live state before writing anything:
   - `git rev-parse HEAD` and `git rev-parse origin/main` (must match),
   - `git status --short` (clean for `experiments/` and `data/`),
   - confirm `.verify_snapshot/` is absent (no half-finished verification run).
2. Create a new file `handoff_<ISO-8601-UTC>_INITIAL_TASK.md` (pattern
   `handoff_YYYY-MM-DDTHH-MM-SSZ_INITIAL_TASK.md`) containing a clear initial
   task message for the session after it, with the guardrails below.
3. Repoint the `handoff_CURRENT` symlink to the new file so it is discoverable.
4. Do **not** run the verification suite, modify `experiments/*.json`, re-pin
   baselines, or take any research action unless the user explicitly asks.

## Guardrails (read before acting)

- Always run with `SEED=42`.
- `experiments/*.json` are canonical goldens — never commit verification output.
- A verification run must never be left half-finished; recover with
  `SEED=42 python3 run_all_verification.py --restore-only` (or
  `git checkout <commit> -- experiments/<file>` if HEAD already carries a
  captured run — see `ledger/golden_baseline.json`).
- Cache coverage is an enforced invariant: every `data.download()` call site
  must have a pinned, git-tracked cache entry (`ledger/data_baseline.json`).
- Golden baseline is pinned in `ledger/golden_baseline.json`; never re-pin as a
  side effect of running verification — record any deliberate change in
  `ledger/RESEARCH_LEDGER.md` first.
- Run `python3 -m py_compile` on any changed Python file (no separate linter).
- `cvxpy`/`cvxopt` are optional; the optimizer falls back to `scipy.optimize`.

## Context / state

- Research phase complete (E001–E043); surviving validated strategies are in
  `ledger/RESEARCH_LEDGER.md`.
- E050 exact active-set enumeration fix applied (bit-reproducible optimizer).
- Data caches pinned (2026-10-11 / 2026-10-12 vintages); E029 fundamentals
  pinned in `data/fundamentals/`; E030 16-ETF panel committed.
- Optional sanity check (read-only, fast, offline): `SEED=42 bash scripts/check.sh`.
- Note: the repo root has accumulated many historical `handoff_*` files and
  alias symlinks from prior sessions. This file is the authoritative current
  handoff; do not delete prior handoffs or baselines as part of this task.

---
*This handoff was created at session initialization to carry the initial task
message forward to the next agentic work session.*