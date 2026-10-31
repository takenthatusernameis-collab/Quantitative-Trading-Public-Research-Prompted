# Durable Handoff — Next Agentic Work Session

**Timestamp:** 2026-10-31T07:12:43Z (UTC)
**Branch:** `main`
**HEAD:** `9d7bf67` (chore(kilo): checkpoint agent session)
**Working tree:** clean of tracked changes. Only `__pycache__/*.pyc` artifacts (gitignored; ignore them).
**Verification snapshot:** none active (`.verify_snapshot/` absent). No run in progress; nothing to recover.

---

## INITIAL TASK (do first)

**Confirm baseline integrity, then await explicit user direction.**

Before making any changes or running verification:

1. **Confirm repo state**
   ```bash
   SEED=42 bash scripts/check.sh
   ```
   Expect exit 0. Runs convention robustness, template validation, goldens guards, data coverage, golden baseline checks, and experiment-script imports.

2. **If checks fail**
   - **Goldens differ from HEAD** → restore from the commit whose SHA-256 matches `ledger/golden_baseline.json` (or `SEED=42 python3 run_all_verification.py --restore-only`, or `git checkout -- experiments/`).
   - **Never re-pin to silence drift** — re-pinning requires `python3 scripts/check_golden_baseline.py --update` and must appear in the diff with justification.
   - **Active verification snapshot** → if `.verify_snapshot/ACTIVE.json` exists, recover with `--restore-only` before proceeding.
   - **Cache coverage failure** → ensure pinned data in `ledger/data_baseline.json` exists and is git-tracked. To add inputs, commit files and re-pin with `python3 scripts/check_data_coverage.py --update`.

3. **Then idle awaiting explicit user direction.**
   - Do **NOT** make source changes or commits unless explicitly asked.
   - Do **NOT** modify `experiments/*.json` goldens as a side effect of verification.
   - Do **NOT** re-pin baselines without explicit instruction and justification in the diff.
   - Do **NOT** run extended/full verification suites without explicit instruction.

---

## Current state

- **Research phase complete:** E001–E043. Surviving validated strategies documented in `ledger/RESEARCH_LEDGER.md`.
- **Working tree:** `git status --short` is empty (only gitignored `__pycache__/*.pyc`). `experiments/` is clean vs HEAD.
- **Verification state:** No active verification snapshot in `.verify_snapshot/`.
- **Goldens:** `experiments/*.json` match HEAD. `ledger/golden_baseline.json` pins tracked artifacts. `ledger/data_baseline.json` enforces cache coverage.
- **Environment:** Python 3.12.3 with deps from `requirements.txt`. If reset, run `pip3 install --break-system-packages -r requirements.txt` first.

---

## Known open items (read AGENTS.md before acting)

- **Optimizer determinism (E049):** `src/portfolio_opt.py` validates solver answers on the problem's constraints; pinned by `tests/test_portfolio_opt.py`. The tangency QP remains ill-conditioned. **Do not re-pin to silence this.** See ledger E049.
- **E041 drift (E049):** 3 structural diffs resolved; 133 numeric diffs remain (1-ulp QP sensitivity). Open item in the ledger. Do **not** re-pin.
- **E030 drift:** numeric diffs on near-zero quantities (documented). Do not re-pin.
- **Cache coverage enforced (E048):** `scripts/check_data_coverage.py` validates all data inputs pinned in `ledger/data_baseline.json`.
- **CI gate workflow:** `.github/workflows/verification-gate.yml` still requires maintainer action via GitHub UI (template at `.github/workflow-templates/verification-gate.yml`).

---

## Key commands

```bash
# Baseline integrity (required first)
SEED=42 bash scripts/check.sh

# Quick/full verification (only if explicitly requested)
SEED=42 python3 run_all_verification.py        # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended  # (~21 min)
SEED=42 python3 run_all_verification.py --full      # (~15 min)

# Recovery after interrupted run
SEED=42 python3 run_all_verification.py --restore-only

# Guards
python3 scripts/check_golden_baseline.py
python3 scripts/check_data_coverage.py
python3 scripts/check_goldens_clean.py
```

(End of handoff)
