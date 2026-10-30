# Durable Handoff — Next Agentic Work Session

**Generated:** 2026-10-30T14-35-18Z (UTC)
**Session:** handoff-only session (no technical work performed)
**Working dir:** /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Branch:** main @ `3b71c87` (HEAD; checkpoint commit)
**Previous handoff:** `HANDOFF_NEXT_SESSION_2026-10-30T14-34-44Z.md`

---

## INITIAL TASK (do first)

**Confirm baseline integrity, then await explicit user direction.**

1. **Confirm repo state before anything else**
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   Expect exit 0: py_compile, goldens clean vs HEAD, pinned baseline match, data coverage, portfolio_opt tests, convention robustness, template validation, experiment-script imports.

2. **If checks fail**
   - **Goldens differ from HEAD** → restore from the commit whose SHA-256 matches `ledger/golden_baseline.json` (or `SEED=42 python3 run_all_verification.py --restore-only`).
   - **Never re-pin to silence drift** — re-pinning requires `python3 scripts/check_golden_baseline.py --update` and must appear in the diff.
   - **Active verification snapshot** → if `.verify_snapshot/ACTIVE.json` exists, recover with `--restore-only` before proceeding.

3. **Then idle awaiting explicit user direction.**
   - Do **NOT** make source changes or commits unless explicitly asked.
   - Do **NOT** modify `experiments/*.json` goldens as a side effect of verification.
   - Do **NOT** re-pin baselines without explicit instruction and justification in the diff.

---

## Current state

- **Research phase complete:** E001–E043. Surviving validated strategies are documented in `ledger/RESEARCH_LEDGER.md`.
- **Working tree:** clean of tracked changes (only gitignored `__pycache__/*`).
- **Verification state:** `.verify_snapshot/` does **NOT** exist — no recovery needed.
- **Goldens:** `experiments/*.json` match HEAD. `ledger/golden_baseline.json` pins 107 tracked artifacts. `ledger/data_baseline.json` enforces cache coverage.
- **Environment:** Python 3.12.3 with deps from `requirements.txt`.

## Known open items (read AGENTS.md before acting)

- **Optimizer determinism (E049):** `src/portfolio_opt.py` validates solver answers on the problem's constraints; tangency QP remains ill-conditioned. Do not re-pin to silence drift. See ledger E049.
- **E041 drift (E049):** 3 structural diffs resolved; 133 numeric diffs remain. Open item in the ledger.
- **Cache coverage enforced (E048):** all data inputs pinned in `ledger/data_baseline.json`.
- **CI gate workflow:** `.github/workflows/verification-gate.yml` requires maintainer action via GitHub UI.

## Key commands

```bash
SEED=42 bash scripts/check.sh
SEED=42 python3 run_all_verification.py
SEED=42 python3 run_all_verification.py --restore-only
python3 scripts/check_golden_baseline.py
python3 scripts/check_data_coverage.py
python3 scripts/check_goldens_clean.py
```
