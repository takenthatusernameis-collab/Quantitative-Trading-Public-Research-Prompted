# DURABLE HANDOFF — Next Agentic Session

**Timestamp (UTC):** 2026-11-01T12-22-32Z
**Repo:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Branch:** main @ HEAD (checkpoint commit)
**State:** Research phase complete (E001–E043). Canonical goldens in `experiments/`, ledger in `ledger/RESEARCH_LEDGER.md`.

## Initial task for next session

1. `pip install -r requirements.txt` if the environment was reset.
2. Recover the stale/left-behind verification snapshot: `.verify_snapshot/` exists with `ACTIVE.json` owning pid 37032 (NOT running — interrupted at ~2026-11-01T11:25Z). Run `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`) to restore canonical goldens before anything else.
3. `SEED=42 bash scripts/check.sh` — expect EXIT 0 with "=== All checks passed ===". This includes `check_goldens_clean.py` (fails if `experiments/` differs from HEAD or a stale snapshot is pending) and `check_golden_baseline.py`.
4. `git status --short` — confirm only `__pycache__/*.pyc` modifications remain. Do NOT commit verification output.
5. Only after steps 1–4 pass cleanly, address the standing open item in `ledger/RESEARCH_LEDGER.md` (E049 tangency QP ill-conditioning). Do not re-pin goldens to silence drift.

## Current state

- **Phase:** Research complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- **Baselines:** `experiments/*.json` are canonical goldens, pinned by `ledger/golden_baseline.json` and `ledger/data_baseline.json`.
- **Snapshot state:** `.verify_snapshot/ACTIVE.json` exists but owner pid 37032 is dead — recovery required before running `scripts/check.sh` (it will fail on the stale snapshot otherwise).
- **Recovery:** `SEED=42 python3 run_all_verification.py --restore-only`.

## Quick references

- `make check` | `make verify-quick` | `make verify-extended` | `make verify-full`
- Ledger: `ledger/RESEARCH_LEDGER.md`
- AGENTS.md — full commands & conventions

## Durable links

- `handoff.md` → this file (latest)
- `handoff_next_session.md` → this file

(End of file)
