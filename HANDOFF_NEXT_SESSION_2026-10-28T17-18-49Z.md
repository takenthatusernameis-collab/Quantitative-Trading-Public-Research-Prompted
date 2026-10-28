# Handoff — Timestamped clear initial task for next agentic session

Timestamp (UTC): ${TS}
Repo: Quantitative-Trading-Public-Research-Prompted
Branch: main
HEAD: ae9d05c chore(kilo): checkpoint agent session
Working dir: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Current state (verified this session)

- Research phase complete (E001–E043). Surviving validated strategies in `ledger/RESEARCH_LEDGER.md`.
- **Baseline is clean and committed.** Verified this session:
  - `SEED=42 bash scripts/check.sh` → ALL CHECKS PASSED (py_compile, JSON parse, goldens match HEAD, golden baseline pin, data coverage, experiment imports, portfolio_opt tests).
  - `SEED=42 python3 scripts/check_golden_baseline.py` → ALL 107 PINNED GOLDEN ARTIFACTS MATCH.
  - `SEED=42 python3 scripts/check_data_coverage.py` → ALL 35 PINNED DATA INPUTS PRESENT, TRACKED, UNCHANGED.
  - `python3 -m unittest tests.test_portfolio_opt` → 8 tests OK.
- Working tree clean of tracked changes. Only gitignored `__pycache__/*.pyc` show as modified.
- No `.verify_snapshot/` — nothing to recover.

## Open items (unchanged, do not re-pin to silence)

- **E041 numeric drift (~133 diffs)** from the ill-conditioned tangency QP in `src/portfolio_opt.py` (1-ulp sensitivity of SLSQP). E041 decision REJECTED 3/5 unchanged. Do NOT re-pin.
- **E042-lead** solver fix in place (ledger E049): optimizer validates answers on problem constraints, never on solver exit status. Tangency QP remains ill-conditioned — residual drift documented, not fixed.
- **E042 primary** (`run_e042.py --n-sim 50`) reproduces both goldens byte-for-byte (0 diffs) under pinned 2026-10-12 cache vintage and `SEED=42`.

## Clear initial task for next session

Execute in order. Treat failures as blockers to fix before proceeding.

### 1) Confirm clean baseline (re-verify)
```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 scripts/check_golden_baseline.py
SEED=42 python3 scripts/check_data_coverage.py
```

### 2) Run quick verification (~8-10 min)
```bash
SEED=42 python3 run_all_verification.py
```
If interrupted, recover:
```bash
SEED=42 python3 run_all_verification.py --restore-only
```

### 3) Optional extended verification
```bash
SEED=42 python3 run_all_verification.py --extended
```
Writes `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json` (gitignored). E041 may show bounded numeric drift; structural changes are not acceptable. Do not re-pin.

### 4) Review before making changes
- Read `ledger/RESEARCH_LEDGER.md` (focus E049, E041, E048/E042-lead, E045–E048)
- Review `ledger/golden_baseline.json` and `ledger/data_baseline.json` before intentional re-pinning.

## Constraints / reminders
- Always use `SEED=42`.
- Never leave a verification run half-finished; if unsure run `--restore-only`.
- Never re-pin goldens as side effect of verification. Re-pinning is deliberate (`python3 scripts/check_golden_baseline.py --update`) and must be recorded in the ledger.
- If `scripts/check.sh` reports golden mismatch, fix before committing — recover from pinned commit (`git checkout <commit> -- experiments/<file>`), never by re-pinning.
- Pinned vintages: `data/vintages.json` (2026-10-12 primary, 2026-10-11 committed), E029 fundamentals pinned in `data/fundamentals/` per `data/fundamentals_vintages.json`. Missing caches fail under offline verification.
- CI workflow cannot be created by agents; template at `.github/workflow-templates/verification-gate.yml`. Local equivalents: `make check`, `make verify`, `make verify-quick`, `make verify-extended`, `make verify-full`.
- Follow `AGENTS.md` conventions.
- `__pycache__/*.pyc` tracked but ignored in effect — not a baseline concern.
- Dependencies installed at `/home/runner/work/_temp/kilo-home/.local`; fresh session may need `pip install -r requirements.txt`. Use `python3 -m unittest tests.test_portfolio_opt` (pytest not installed).

## Suggested first commands
```bash
git status --short
git log -1 --oneline
SEED=42 bash scripts/check.sh
```

## Handoff notes
- This handoff supersedes previous timestamped handoffs as the clear initial task message for the next agentic session.
- Recovery: stale snapshot → `--restore-only` → if artifacts still mismatch pin, `git checkout <pinned-commit> -- experiments/<file>` → commit recovery.

(End of file)
