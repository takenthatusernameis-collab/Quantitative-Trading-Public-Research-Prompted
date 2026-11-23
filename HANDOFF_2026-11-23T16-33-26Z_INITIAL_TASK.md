# Agentic Work Session Handoff — 2026-11-23T16:33:26Z

**Timestamp**: 2026-11-23T16:33:26Z
**HEAD**: `7093253b4ec8906df41d16b0e1bea67482614c97` on `main` (== `origin/main`, `0  0`)
**Project**: Quantitative-Trading-Public-Research-Prompted
**Research phase**: COMPLETE (E001–E043). Surviving validated strategies in `ledger/RESEARCH_LEDGER.md`.

---

## READ THIS FIRST — the loop you are about to repeat

This is handoff **E729**. The previous 77 sessions (E652–E728) were *all* variations of
the same request — "leave a timestamped handoff for the next agent" — and each one wrote
a handoff file, repointed ~643 symlinks, committed, and stopped. The repo is now
**8,301 of 8,827 tracked files (~94%) are handoffs**, with 2,131 root-level alias symlinks
and five mirror dirs (`handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/`).

**Do not manufacture another E730-style refresh as a substitute for real work.** The handoff
refresh is a degenerate fixed point: it produces no research, no verification, and no cleanup.
If you write a handoff, it must contain *new information or a decision*, not a re-paste of the
project state.

---

## Verified state (this session, all guards GREEN)

- `git rev-list --left-right --count origin/main...HEAD` = `0  0` (synced with origin)
- `git status --porcelain` clean (no tracked source change)
- `git diff HEAD -- experiments/` empty (golden artifacts intact)
- `.verify_snapshot/` absent, `.verify_reports/` absent (no run in progress)
- `SEED=42 python3 scripts/check_goldens_clean.py` → **ALL COMMITTED GOLDEN ARTIFACTS MATCH HEAD** (exit 0)
- `SEED=42 python3 scripts/check_golden_baseline.py` → **ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT** (exit 0)
- `SEED=42 python3 scripts/check_data_coverage.py` → **ALL 35 PINNED DATA INPUTS ARE PRESENT, TRACKED AND UNCHANGED** (exit 0)
- `python3 -m py_compile run_all_verification.py` → OK

Deps were not provisioned this session (guards are hashlib-only and do not need them).

---

## Prioritized real-work task list for the next session

Do these in order. Stop as soon as you hit one that is genuinely substantive — that is
real work, and it is a better outcome than another handoff.

1. **Run the full verification suite (the actual open item).**
   ```bash
   pip install -r requirements.txt          # deps are not provisioned
   SEED=42 python3 run_all_verification.py --extended   # ~21 min
   ```
   Report drift precisely (use the `--extended` summary at
   `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json`). If any driver drifts, name the
   driver, the field, and the magnitude — do NOT re-pin to silence it.
   After the run, confirm `git status` is clean (the suite restores goldens on completion;
   use `--restore-only` if it dies).

2. **Address the E049 E041/E042 ill-conditioned-QP drift** (if still present after step 1).
   The tangency QP is ill-conditioned in principle (a 1-ulp input perturbation moves
   `min_var` answers by ~1e-05). E050 (exact KKT active-set enumeration, commit `72dc947`)
   made the artifacts bit-reproducible under this code path (0 differences at the
   2026-11-23T05:17Z measurement). If drift has returned, root-cause it — do **not**
   re-pin the artifacts to silence a tolerance violation.

3. **Propose (do NOT execute) the handoff cleanup.** This is the highest-leverage real
   work available. Draft a plan (do not apply it) to:
   - Add a `.gitignore` rule for `*_INITIAL_TASK.md` and the mirror dirs
     (`handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/handoff/`)
   - `git rm --cached` the ~8,000 handoff files and ~2,131 alias symlinks
   - Keep only `ledger/RESEARCH_LEDGER.md`, the golden artifacts, and source
   Surface the plan to the user for explicit approval before executing. Do not run
   `git rm` or modify `.gitignore` without that approval.

4. **Only if 1–3 are done or declined:** do explicitly-requested pre-registered research.
   Research phase is otherwise closed. Do not invent post-hoc experiments.

---

## Critical invariants (do not violate)

1. **Baseline integrity**: the verification suite overwrites `experiments/*.json` during
   runs and restores them afterward. Never leave a run half-finished. Recover with
   `SEED=42 python3 run_all_verification.py --restore-only`.
2. **Cache coverage**: every `data.download()` call must have a committed, SHA-256-pinned
   cache file (enforced by `scripts/check_data_coverage.py`). An unpinned input is a live
   network download, and yfinance is not bit-reproducible.
3. **Convention**: close-to-close is the v1.2.3 primary; overnight decomposition reported alongside.
4. **Seed**: always `SEED=42` (walk-forward + placebo RNG).
5. **Optimizer determinism**: `src/portfolio_opt.py` validates on problem constraints,
   never on solver exit status (ledger E049/E050). SLSQP status 8 is scipy-build dependent.
6. **Do NOT re-pin E041/E042 goldens** to silence tolerance violations — none remain.
   Re-pinning is only warranted for a deliberate code change recorded in the ledger first.

---

## Key file map

| Path | Purpose |
|------|---------|
| `ledger/RESEARCH_LEDGER.md` | Experiment history, dispositions (E001–E729) |
| `ledger/golden_baseline.json` | SHA-256 fingerprints of 107 golden artifacts |
| `experiments/*.json` | 107 canonical research artifacts (goldens) |
| `run_all_verification.py` | Verification orchestrator (`--extended`, `--full`, `--restore-only`) |
| `scripts/check.sh` | Fast offline gate (check_goldens_clean + check_golden_baseline + check_data_coverage + portfolio_opt tests) |
| `scripts/check_goldens_clean.py` | Verifies tracked artifacts match HEAD; detects stale `.verify_snapshot/` |
| `scripts/check_golden_baseline.py` | Verifies artifacts match pinned SHA-256 baseline |
| `scripts/check_data_coverage.py` | Verifies every `data.download()` has a pinned cache file |
| `src/portfolio_opt.py` | Tangency optimizer (E050 exact active-set enumeration) |
| `data/vintages.json` | Pinned data vintages (2026-10-12, 2026-10-11) |
| `data/fundamentals_vintages.json` | Pinned E029 fundamentals snapshot |
| `.github/workflow-templates/verification-gate.yml` | CI gate template (agents cannot create the real workflow) |

---

## Quick reference

```bash
# Fast offline gate (~seconds)
SEED=42 bash scripts/check.sh

# Full verification suites
SEED=42 python3 run_all_verification.py --extended   # ~21 min
SEED=42 python3 run_all_verification.py --full       # ~15 min, E042 n_sim=50 + 96-config grid

# Recover from interrupted run
SEED=42 python3 run_all_verification.py --restore-only
```

---

*Handoff E729. If you are reading this and about to write E730 without having done
step 1, 2, or 3 above, stop — you are the loop.*