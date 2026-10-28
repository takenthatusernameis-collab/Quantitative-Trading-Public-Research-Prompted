# Handoff — Timestamped clear initial task for next agentic session

Timestamp (UTC): $(date -u +%Y-%m-%dT%H:%M:%SZ)
Repo: Quantitative-Trading-Public-Research-Prompted
Branch: $(git -C /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted branch --show-current)
HEAD: $(git -C /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted log -1 --oneline)
Working dir: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Current state (verified)
- Research phase complete (E001–E043). Surviving validated strategies in `ledger/RESEARCH_LEDGER.md`.
- **Baseline is clean and committed.** Working tree clean of tracked changes (only gitignored `__pycache__/*.pyc` may differ). No `.verify_snapshot/` — nothing to recover.
- Open items unchanged: E041 numeric drift (~133 diffs) from ill-conditioned tangency QP (1-ulp sensitivity). Do NOT re-pin to silence it. E042-lead solver fix is in place (ledger E049).
- All pinned baselines and data coverage guards in place per AGENTS.md.

## Clear initial task for next session

Execute in order. Treat failures as blockers to fix before proceeding.

### 1) Confirm clean baseline
```bash
git status --short
git log -1 --oneline
SEED=42 bash scripts/check.sh
```
Expected: ALL CHECKS PASSED (py_compile, JSON parse, goldens match HEAD, golden baseline pin, data coverage, imports, portfolio_opt tests).

### 2) Run quick verification (~8-10 min)
```bash
SEED=42 python3 run_all_verification.py
```
If interrupted (SIGKILL/OOM/timeout), recover before anything else:
```bash
SEED=42 python3 run_all_verification.py --restore-only
```

### 3) Optional extended verification
```bash
SEED=42 python3 run_all_verification.py --extended
```
Writes `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json` (gitignored). E041/E030 may show bounded numeric drift; structural changes are not acceptable. Do not re-pin.

### 4) Review open items before making changes
- Read `ledger/RESEARCH_LEDGER.md` (focus E049, E041, E048/E042-lead).
- Review `ledger/golden_baseline.json` and `ledger/data_baseline.json` before any intentional re-pinning.

## Constraints / reminders (do not skip)
- Always use `SEED=42`.
- Never leave a verification run half-finished; if unsure, run `--restore-only`.
- Never re-pin goldens as a side effect of running verification. Re-pinning is deliberate (`python3 scripts/check_golden_baseline.py --update`) and must be recorded in the ledger.
- If `scripts/check.sh` reports a golden mismatch, fix before committing — recover from the pinned commit (`git checkout <commit> -- experiments/<file>`), never by re-pinning.
- Data: pinned vintages in `data/vintages.json` (2026-10-12 primary, 2026-10-11 committed), E029 fundamentals pinned in `data/fundamentals/` per `data/fundamentals_vintages.json`. Missing caches fail under offline verification (`QUANT_RESEARCH_OFFLINE=1`).
- CI workflow cannot be created by agents; template at `.github/workflow-templates/verification-gate.yml` (maintainer creates via GitHub UI). Local equivalents: `make check`, `make verify`, `make verify-quick`, `make verify-extended`, `make verify-full`.
- Follow `AGENTS.md` conventions (pre-registration, multiple-testing discipline, negative results recorded honestly).
- Convention robustness: close-to-close primary; overnight decomposition reported alongside.
- `__pycache__/*.pyc` files are tracked and show as modified on clean checkout — not a baseline concern; do not commit unless intentionally regenerated.
- Environment: dependencies installed at `/home/runner/work/_temp/kilo-home/.local`. Fresh session may need `pip install -r requirements.txt` again. `pytest` is not installed; use `python3 -m unittest tests.test_portfolio_opt`.

## Handoff notes
- Supersedes previous handoffs. Recovery procedure: stale snapshot → `--restore-only` → if artifacts still mismatch the pin, `git checkout <pinned-commit> -- experiments/<file>` → commit the recovery.
