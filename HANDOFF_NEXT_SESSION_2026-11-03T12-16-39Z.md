# DURABLE HANDOFF — Next Agentic Session

**Timestamp (UTC):** 2026-11-03T12:16:39Z
**Repo:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Branch:** main (HEAD 76eb32c, "chore(kilo): checkpoint agent session")
**State:** Working tree clean (no tracked changes). No live verification snapshot (`.verify_snapshot/` absent) — nothing to recover. No open task in the queue.

## Initial task message for the next agentic work session

> **START HERE:** The baseline is verified clean and the repository is closed. There is currently no open task in the queue. Wait for explicit user instructions before taking any action. Do **not** invent new tasks, re-run verification "just to be sure", create additional handoffs unprompted, or re-open closed items (E049/E050 optimizer determinism, E041/E042 drift). Follow all standing constraints in AGENTS.md.

## Standing constraints (must follow)

- Never commit verification output. Restore goldens first if interrupted (`SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`).
- Never re-pin goldens to silence drift. Only re-pin via `python3 scripts/check_golden_baseline.py --update` with explicit ledger justification.
- Honor pinned cache vintages (`data/vintages.json`, `data/fundamentals/` per `data/fundamentals_vintages.json`, `ledger/data_baseline.json`). Offline mode (`QUANT_RESEARCH_OFFLINE=1`) is used by verification; unpinned inputs fail hard.
- Do not change gate logic, sensitivity grids, pre-registered outcomes, or validated constructions without explicit justification and a ledger entry.
- Follow repo conventions in `AGENTS.md` (SEED=42, `python3 -m py_compile` on touched scripts, offline verification).
- The controller checkpoints and CI gate template exist; do not attempt to create/modify GitHub workflows (`.github/workflows/`).

## Quick Start / Verify commands

- Fast check: `SEED=42 bash scripts/check.sh` or `make check`
- Quick verify: `SEED=42 python3 run_all_verification.py` or `make verify-quick`
- Extended: `SEED=42 python3 run_all_verification.py --extended` or `make verify-extended`
- Full: `SEED=42 python3 run_all_verification.py --full` or `make verify-full`
- Restore goldens if interrupted: `SEED=42 python3 run_all_verification.py --restore-only`

## References

- `ledger/RESEARCH_LEDGER.md`
- `AGENTS.md`
- Previous handoff: `HANDOFF_NEXT_SESSION_2026-11-03T04-21-25Z.md`

**Handoff created:** 2026-11-03T12:16:39Z (UTC)
