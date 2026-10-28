# HANDOFF - Next Agentic Work Session
Timestamp: 2026-10-28T00:47:07Z
Repo: Quantitative-Trading-Public-Research-Prompted
Branch: main (HEAD 5dcd64e)

## Current State
- Research phase complete (E001–E043). Surviving validated strategies documented in ledger/RESEARCH_LEDGER.md.
- All goldens are the committed baselines (experiments/*.json). Verification suite backs up/restores them.
- Recent checkpoints from agent sessions (5dcd64e, e72e763, 9cb265c, 1f70e9f, 55412e8).

## Immediate Priority Task (CLEAR INITIAL TASK)
1. **Run baseline verification to confirm repo is clean.**
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   Or run quick verify:
   ```bash
   SEED=42 python3 run_all_verification.py
   ```
   Ensure `scripts/check_goldens_clean.py` and `scripts/check_golden_baseline.py` pass with no baseline drift.

2. **Review ledger for open items** - Look at `ledger/RESEARCH_LEDGER.md` for any "open", "TODO", or incomplete items (notably related to E041/E042 drift tolerance discussed in AGENTS.md).

3. **Do NOT re-pin baselines** unless explicitly fixing a known data issue following the documented procedure. The golden baseline is authoritative.

## Quick Commands
- Fast check: `SEED=42 bash scripts/check.sh` or `make check`
- Quick verify (8 drivers): `SEED=42 python3 run_all_verification.py` or `make verify-quick`
- Extended: `SEED=42 python3 run_all_verification.py --extended` or `make verify-extended`
- Full: `SEED=42 python3 run_all_verification.py --full` or `make verify-full`
- Convention robustness: `SEED=42 python3 verify_convention_robustness.py` or `make verify`

## Important Guardrails (from AGENTS.md)
- Never leave verification half-finished - snapshot in `.verify_snapshot/` with ACTIVE.json; if killed, recover with `--restore-only`
- `check_goldens_clean.py` fails if tracked artifacts differ from HEAD or stale snapshot pending (live run reported, not failed)
- `check_golden_baseline.py` compares against SHA-256 in `ledger/golden_baseline.json` - re-pinning requires explicit `--update` and must be intentional
- If interrupted, restore with `SEED=42 python3 run_all_verification.py --restore-only` or `git checkout -- experiments/`
- E041/E042 have known optimizer-determinism numeric drift (ill-conditioned QP) - do NOT re-pin to silence; see ledger
- E029/E030 offline-reproducible after pinning; cache coverage enforced by `check_data_coverage.py`

## Files to Read First
- `AGENTS.md` - full project conventions and verification procedures
- `ledger/RESEARCH_LEDGER.md` - research history, decisions, open items
- `run_all_verification.py` - verification orchestration
- `scripts/check.sh` - fast convention checks

## Session Goal
Confirm clean baseline state. If clean, review ledger for any concrete open research items to tackle. If there are issues, follow recovery procedures before making changes.
