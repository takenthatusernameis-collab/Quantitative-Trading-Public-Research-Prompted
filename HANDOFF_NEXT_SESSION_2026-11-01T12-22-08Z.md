# DURABLE HANDOFF — Next Agentic Session

**Timestamp (UTC):** 2026-11-01T12-22-08Z
**Repo:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Branch:** main @ HEAD (checkpoint commit)
**State:** Research phase complete (E001–E043). Canonical goldens in `experiments/`, ledger in `ledger/RESEARCH_LEDGER.md`.

## Initial task for next session

1. `pip install -r requirements.txt` if the environment was reset.
2. `SEED=42 bash scripts/check.sh` — expect EXIT 0 with "=== All checks passed ===".
3. `git status --short` — confirm only `__pycache__/*.pyc` modifications remain. If a verification run was interrupted, recover with `SEED=42 python3 run_all_verification.py --restore-only`.
4. Only after steps 1–3 pass cleanly, address the standing open item in `ledger/RESEARCH_LEDGER.md` (E049 tangency QP ill-conditioning). Do not re-pin goldens to silence drift.

## Current state

- **Phase:** Research complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- **Baselines:** `experiments/*.json` are canonical goldens, pinned by `ledger/golden_baseline.json` and `ledger/data_baseline.json`.
- **Snapshot state:** `.verify_snapshot/` should not exist — no recovery needed.
- **Recovery:** `SEED=42 python3 run_all_verification.py --restore-only`.

## Quick references

- `make check` | `make verify-quick` | `make verify-extended` | `make verify-full`
- Ledger: `ledger/RESEARCH_LEDGER.md`
- AGENTS.md — full commands & conventions

(End of file)
