# Agent Handoff — 2026-11-22T21:52:55Z

## Project State
- **Repository**: Quantitative-Trading-Public-Research-Prompted
- **Phase**: Research complete (E001–E043), surviving strategies documented in `ledger/RESEARCH_LEDGER.md`
- **Verification baseline**: Committed goldens in `experiments/*.json` pinned to `ledger/golden_baseline.json`

## Key Context
- Golden artifacts are **authoritative** — never re-pin as side effect of verification runs
- `scripts/check.sh` / `make check` validates convention robustness + template + golden integrity
- `run_all_verification.py` backs up goldens to `.verify_snapshot/` before re-running, restores after
- If verification interrupted: `SEED=42 python3 run_all_verification.py --restore-only`

## Current Status
No active verification run. Working tree clean (goldens match HEAD and golden_baseline.json).

## Next Session Entry Points
| Goal | Command |
|------|---------|
| Fast convention check | `SEED=42 make check` |
| Quick verification (8 min) | `SEED=42 make verify-quick` |
| Extended verification (21 min) | `SEED=42 make verify-extended` |
| Full verification (15 min + sensitivity) | `SEED=42 make verify-full` |
| Individual experiment | `SEED=42 python3 experiments/run_e042.py --n-sim 50` |

## Open Items (from ledger)
- E041: 133 numeric diffs remain (ill-conditioned QP, 1-ulp sensitivity) — **do not re-pin**
- E042 grid artifacts drift similarly — **do not re-pin**
- Cache coverage invariant enforced by `scripts/check_data_coverage.py`

## Data Vintages
- Primary: `data/vintages.json` (2026-10-12)
- Legacy: `data/vintages.json` (2026-10-11) for E026/E028/E029/E030/E034/E036/E037
- Fundamentals: `data/fundamentals_vintages.json` (E029 offline-reproducible)

---
*Generated for durable handoff to next agentic session*