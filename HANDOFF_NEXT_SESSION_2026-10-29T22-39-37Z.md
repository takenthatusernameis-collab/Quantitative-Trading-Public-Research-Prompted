# HANDOFF: Next Agentic Work Session

**Created:** 2026-10-29T22:39:37Z
**Repo:** Quantitative-Trading-Public-Research-Prompted
**State:** Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`. Baseline integrity guards enforced.

## Initial Task (Start Here)

Verify the baseline is clean before any work.

1. Run `SEED=42 bash scripts/check.sh` — all guards must pass with no golden diffs.
2. Run `git status --short` / `git diff --name-only` — confirm clean tree.
3. If interrupted verification left dirty `experiments/*.json`, restore: `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`).

Do not re-pin goldens to silence drift. Keep committed goldens authoritative. Read `AGENTS.md` and `ledger/RESEARCH_LEDGER.md` first.
