# HANDOFF - Next Agentic Work Session
Timestamp (UTC): 2026-10-28T17-21-09Z
Repo: Quantitative-Trading-Public-Research-Prompted
Branch: main
HEAD: f63f133 chore(kilo): checkpoint agent session
Working dir: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted

## Current State
- Research phase complete (E001–E043). Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- All goldens are the committed baselines (`experiments/*.json`). Verification suite backs up/restores them.
- Working tree is clean of tracked changes (only `__pycache__/*.pyc` may show as modified).
- No active `.verify_snapshot/` — nothing to recover.
- Pinned data: `data/vintages.json` (2026-10-12 primary, 2026-10-11 committed), fundamentals pinned in `data/fundamentals/` per `data/fundamentals_vintages.json`. Cache coverage enforced by `scripts/check_data_coverage.py`.

## Clear Initial Task (Execute in Order)

Treat any failure as a blocker. Follow recovery procedures before making changes.

### 1) Confirm clean baseline
```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 scripts/check_golden_baseline.py
SEED=42 python3 scripts/check_data_coverage.py
python3 -m unittest tests.test_portfolio_opt
```
All checks must pass. `scripts/check.sh` runs py_compile, JSON validation, `check_goldens_clean.py`, `check_golden_baseline.py`, `check_data_coverage.py`, experiment imports, and portfolio_opt tests.

### 2) Run quick verification (~8-10 min)
```bash
SEED=42 python3 run_all_verification.py
```
If interrupted, recover:
```bash
SEED=42 python3 run_all_verification.py --restore-only
```
Or restore from git if needed: `git checkout -- experiments/` (use pinned commit if HEAD already contains a captured run).

### 3) Review open items & context
- Read `ledger/RESEARCH_LEDGER.md` (focus: E049, E041, E042-lead, E042 primary, E048, E045–E048)
- Review `ledger/golden_baseline.json` and `ledger/data_baseline.json` before any intentional re-pinning
- Read `AGENTS.md` for full verification/recovery procedures

### 4) Optional extended verification
```bash
SEED=42 python3 run_all_verification.py --extended
```
Writes `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json` (gitignored). Note known drift:
- **E041**: ~133 numeric diffs from ill-conditioned tangency QP in `src/portfolio_opt.py` (1-ulp sensitivity). Decision REJECTED 3/5 unchanged. **Do NOT re-pin to silence.**
- **E042-lead**: solver fix in place (validates on problem constraints, not solver exit status). Tangency QP remains ill-conditioned with residual drift. **Do NOT re-pin to silence.**
- Structural changes in extended comparison are not acceptable.

## Guardrails (Critical)
- **Always use `SEED=42`.**
- **Never leave verification half-finished.** Snapshot lives in `.verify_snapshot/` with `ACTIVE.json`. If killed, recover with `--restore-only`. Suite refuses to start if another live run owns the snapshot.
- **Never re-pin baselines as a side effect of verification.** Re-pinning requires explicit `python3 scripts/check_golden_baseline.py --update`, must be intentional, and must be recorded in the ledger.
- **If `scripts/check.sh` reports golden mismatch:** fix before committing. Recover from pinned commit: `git checkout <pinned-commit> -- experiments/<file>`, never by re-pinning.
- **Offline enforcement:** `QUANT_RESEARCH_OFFLINE=1` is used by verification. Missing pinned caches fail hard (see `scripts/check_data_coverage.py`).
- **Optimizer determinism:** SLSQP status 8 can occur at constrained optimum; gating on exit status is incorrect (fixed per E049). See `tests/test_portfolio_opt.py`.
- **CI workflow:** Cannot be created by agents. Template at `.github/workflow-templates/verification-gate.yml`. Use local equivalents: `make check`, `make verify-quick`, `make verify-extended`, `make verify-full`.

## Quick Commands
```bash
git status --short
git log -1 --oneline
SEED=42 bash scripts/check.sh
```

## Handoff Notes
- This supersedes previous timestamped handoffs as the clear initial task for the next agentic session.
- If recovery is needed after interruption: `SEED=42 python3 run_all_verification.py --restore-only` → if artifacts still mismatch pin, `git checkout <pinned-commit> -- experiments/<file>` → commit recovery.
- Dependencies may need installation in fresh sessions: `pip install -r requirements.txt`. Use `python3 -m unittest` (pytest may not be installed).
