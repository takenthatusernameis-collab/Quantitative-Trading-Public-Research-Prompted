# Agentic Work Session Handoff

**Timestamp**: 2026-11-23T01:44:35Z
**Working Directory**: /home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted
**Project**: Quantitative Trading Public Research (2014–2026 US equities, futures, macro)
**HEAD**: `cd4cf5e7baeae4d0d8cdd1dff6c37eabe202dbb2` on `main` (== `origin/main`; `git rev-list --left-right --count origin/main...HEAD` = `0  0`)

---

## Initial Task (read this first)

You are the next agentic work session. The project's **research phase is
complete (E001–E043)**; surviving validated strategies are in
`ledger/RESEARCH_LEDGER.md`.

**Do NOT turn a handoff refresh into your deliverable.** This repository is in
a runaway handoff-refresh loop: ledger entries **E652–E719** are all
"Durable handoff refresh" with no real work, and there are **8,162 git-tracked
handoff files**. Each refresh adds one more file and one more ledger entry,
which makes the problem worse. This handoff exists only because the user
explicitly asked for a durable initial task message. **Your job is to do real
work, not add another handoff refresh.**

### What "real work" means here

The environment *can* provision dependencies (`pypi.org` reachable;
`python3 -m pip` present), so the only blocker to a full verification run is
installation. Pick the highest-value item below and execute it:

1. **Run the real verification suite** (first time in many sessions):
   ```bash
   pip install -r requirements.txt
   SEED=42 bash scripts/check.sh                       # fast (seconds), expect PASS
   SEED=42 python3 run_all_verification.py             # quick (~8 min, 8 drivers)
   # then, if time allows:
   SEED=42 python3 run_all_verification.py --extended  # + 18 drivers (~21 min)
   ```
   Report PASS/FAIL and any drift precisely (numeric vs structural, worst
   drift as a multiple of tolerance).

2. **Address the open E049 item**: the E041/E042 ill-conditioned-QP drift.
   `src/portfolio_opt.py` already validates on the problem's constraints (not
   the solver exit status), but the tangency QP is still ill-conditioned —
   1-ulp input perturbations move `min_var` answers by ~1e-05, so the E041/E042
   grid artifacts still drift by 29–133 differences beyond the 1e-4
   tolerance. **Do NOT re-pin to silence it.** Either improve conditioning, or
   document a principled tolerance relaxation with a pre-registered rationale.

3. **Do explicitly-requested pre-registered research** only.

4. **Failing all of the above**, propose (do NOT execute) a `.gitignore` +
   `git rm --cached` cleanup of the historical handoff clutter — this needs
   user approval and is out of scope for an unprompted session.

Report results and **then stop**. Do not manufacture E720 or another handoff
refresh as a substitute for real work.

## Integrity rules (do not violate)

- `experiments/*.json` are canonical; never commit verification output over them.
- Always `SEED=42`.
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json`
  to silence drift.
- Do not commit unless the user explicitly asks.

## Verified state at handoff creation (2026-11-23T01:44:35Z)

- HEAD `cd4cf5e7baeae4d0d8cdd1dff6c37eabe202dbb2` on `main` == `origin/main`.
- `git diff HEAD -- experiments/` empty; `.verify_snapshot/` and
  `.verify_reports/` absent.
- `scripts/check_goldens_clean.py` -> ALL COMMITTED GOLDEN ARTIFACTS MATCH HEAD (exit 0).
- `scripts/check_golden_baseline.py` -> ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT (exit 0).
- `scripts/check_data_coverage.py` -> ALL 35 PINNED DATA INPUTS ARE PRESENT, TRACKED AND UNCHANGED (exit 0).
- Deps not provisioned (guards are hashlib-only); full verification suite not run.

(End of file)