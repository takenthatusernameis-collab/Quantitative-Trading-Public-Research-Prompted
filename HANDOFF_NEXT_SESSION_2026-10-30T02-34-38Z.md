# HANDOFF — Next Agentic Work Session
Timestamp: 2026-10-30T02:34:38Z
Project: Quantitative-Trading-Public-Research-Prompted
Branch/Repo: git repo (see AGENTS.md)
Working tree: clean baseline state expected unless mid-run

## Initial Task (clear, actionable)
**Primary objective:** Maintain baseline integrity and keep verification green. Treat `experiments/*.json` as canonical; never silently re-pin from a verification run.

Before making changes:
1. **Verify baseline clean**: `SEED=42 bash scripts/check.sh` (convention-robustness + template validation + golden guards). If it fails on goldens, restore first.
2. **Know the guardrails**: `scripts/check_goldens_clean.py` (HEAD vs working tree), `scripts/check_golden_baseline.py` (vs pinned SHA-256 in `ledger/golden_baseline.json`), `scripts/check_data_coverage.py` (all data inputs pinned/tracked).
3. **If verification was interrupted**: recover with `SEED=42 python3 run_all_verification.py --restore-only` (or `git checkout -- experiments/`). Do not commit partial driver outputs.

## Current State (from repo)
- Research phase complete (E001–E043). Surviving strategies in `ledger/RESEARCH_LEDGER.md`.
- Verification suite exists: `run_all_verification.py` with `--quick`, `--extended`, `--full`, `--skip-slow`, `--restore-only`.
- Golden baseline pinned in `ledger/golden_baseline.json`. Data coverage enforced in `ledger/data_baseline.json`.
- Optimizer determinism fix noted (E049): solver status gating removed; tangency QP ill-conditioned (numeric drift possible) — do not re-pin to silence.
- E029/E030 pinned inputs committed for offline reproducibility.

## Suggested First Actions for Next Session
- [ ] Run `SEED=42 bash scripts/check.sh` and confirm all checks pass.
- [ ] Skim `ledger/RESEARCH_LEDGER.md` for any open items needing follow-up (especially E049 numeric drift / any new entries).
- [ ] If changes are requested, follow AGENTS.md: seed 42, respect pre-registration, multiple-testing discipline, never commit verification outputs.
- [ ] After changes, run relevant verification (`verify-quick` or targeted driver) and ensure goldens unchanged unless explicitly re-pinned via the guard scripts with justification.

## Quick Commands
```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 run_all_verification.py --quick
SEED=42 python3 verify_convention_robustness.py
SEED=42 python3 run_all_verification.py --restore-only
```

## Notes
- CI workflow cannot be created by agents (controller restores .github/workflows). Template at `.github/workflow-templates/verification-gate.yml`.
- Put new Kilo commands/agents in `.kilo/` (not `.kilocode/` or `.opencode/`).
