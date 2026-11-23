# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-23T13-18-49Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `a945039b76f1ba8a803f3bb54af21384783be325`
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

> This file was written at the user's explicit request: *"Leave a timestamped clear
> initial task message for the next agentic work session in a durable handoff!"*
> It exists to hand off **real state**, including a regression the previous handoff
> (`handoff_2026-11-23T10-31-06Z_INITIAL_TASK.md`, HEAD `b2476872`) could not have
> seen because it landed *after* that handoff was written. Read the regression
> section first; it is the single most important item below.

---

## 0. CRITICAL — the golden baseline is currently VIOLATED (action required)

`SEED=42 python3 scripts/check_golden_baseline.py` **FAILS** this session with
**18 pinned artifacts differing from the pinned baseline**. This is a real
regression, not a tolerance issue:

- **Symptom:** `check_goldens_clean.py` still PASSES (`ALL COMMITTED GOLDEN
  ARTIFACTS MATCH HEAD`), but `check_golden_baseline.py` FAILS (`FAIL 18 pinned
  artifact(s) differ from the pinned baseline`). A clean working tree + a passing
  clean-guard + a failing baseline-guard means the *committed* artifacts were
  replaced — exactly the failure mode `AGENTS.md` documents.
- **Culprit commit:** `195c4029  chore(kilo): checkpoint agent session` — it
  overwrote 18 canonical `experiments/*.json` with verification-run output
  (`git show 195c4029 --stat` = 18 files, 164 insertions / 164 deletions,
  symmetric = regenerated timestamps/floats, not deliberate research).
- **Last good state:** `b2476872` (prior handoff HEAD) and its child `193a5c67`
  (immediate parent of the culprit) match the pinned SHA-256 for **all 18**
  artifacts (verified byte-for-byte this session). HEAD `a945039b` itself only
  adds `research_state/workflow_run_diagnostics.jsonl` and does **not** touch
  `experiments/`.
- **Affected artifacts (18):**
  `e011_regime_blend`, `e012_market_neutral`, `e013_validate_lowbeta`,
  `e015_blend_optimization`, `e016_futures_tsm_carry`, `e017_extended_futures`,
  `e018_carry_validation`, `e019_cross_asset_portfolio`, `e020_robustness`,
  `e021_pairs_trading`, `e022_macro_momentum`, `e023_economic_trend`,
  `e027_ivol_anomaly`, `e035_illiquidity`, `e037_portfolio`,
  `e039_extended_macro`, `e042_lead_config_confirmatory`, `validation_summary`.

### Recovery (do this FIRST — verified, and it is NOT a re-pin)

The pinned fingerprints in `ledger/golden_baseline.json` are authoritative; the
fix is to **restore the committed artifacts to their last-good content**, not to
re-pin. Both `193a5c67` and `b2476872` were verified to match the pin for all 18.

```bash
# Restore the canonical artifacts from the last known-good commit.
git checkout 193a5c67 -- experiments/          # or: b2476872 -- experiments/

# Confirm the baseline guard now passes.
SEED=42 python3 scripts/check_golden_baseline.py   # expect: ALL 107 PINNED ... MATCH ...

# If (and only if) it passes, commit the restore so the fix is durable.
# Do NOT commit anything else over experiments/. Suggested message:
#   restore(experiments): revert accidental verification overwrite in 195c4029
```

- **Do NOT** "fix" this by running `scripts/check_golden_baseline.py --update`
  (that re-pins the corrupted state). The ledger's standing disposition is that
  the committed golden is authoritative, not the latest re-run.
- After restoring, the three guards should all PASS again; then this handoff's
  "Verify and stop" step applies.

---

## 1. Read this first — the handoff-refresh loop (be honest about it)

This repo is in a **runaway handoff-refresh loop** (ledger E652–E726+; this
session would be ~E727). Of ~8,800 git-tracked files, the large majority are
handoff artifacts (`handoff_*` / `HANDOFF*` / generic-alias symlinks). Writing
yet another near-identical handoff is *the loop*, not work. This file exists
**only because the user explicitly asked for a timestamped handoff.** Do NOT
manufacture an E727-style refresh as a substitute for real work, and do not
repoint all ~500 mirror aliases to look busy — the root aliases below are the
canonical entry points.

---

## 2. Current state (verified at handoff, 2026-11-23T13:18Z)

- **Research phase:** complete (E001–E043 core; handoff refreshes logged through
  E726). Authoritative dispositions live in `ledger/RESEARCH_LEDGER.md`. No
  actionable open/pending research items.
- **HEAD:** `main` @ `a945039b`; `git rev-list --left-right --count
  origin/main...HEAD` = `0  0` (in sync with origin/main).
- **Working tree:** clean (`git status --porcelain` empty) apart from tracked
  `__pycache__/*.pyc` build noise (15 .pyc files, not research output).
- **Experiments diff vs HEAD:** empty (`git diff HEAD -- experiments/` empty) —
  *but* see §0: the committed artifacts themselves were replaced in `195c4029`.
- **Verification snapshot:** `.verify_snapshot/` absent; `.verify_reports/`
  absent. No interrupted verification; no verification process running.
- **Guards (this session):**
  - `scripts/check_goldens_clean.py` → **PASS** (ALL COMMITTED GOLDEN ARTIFACTS MATCH HEAD)
  - `scripts/check_golden_baseline.py` → **FAIL — 18 artifacts differ from pinned baseline (see §0)**
  - `scripts/check_data_coverage.py` → **PASS** (ALL 35 PINNED DATA INPUTS PRESENT, TRACKED, UNCHANGED)
- **Deps:** NOT provisioned (numpy/pandas/scipy/pyarrow/statsmodels/yfinance
  absent; the three guards are hashlib-only and run offline). The CI
  "Kilo General Agent Loop" (`.github/workflows/main.yml`, runs on schedule)
  fails with `ModuleNotFoundError: No module named 'pandas'` because deps are
  not installed — this is an environment limitation, not a repo defect.

---

## 3. Initial task for the next session (CLEAR, prioritized)

**Default: await explicit user instructions.** Do not invent experiments, run
verification unprompted, move pre-registered gates, or touch golden/baseline
artifacts without explicit direction.

If you must act autonomously, work the following in order and **stop when a step
is done**:

1. **Fix the baseline regression (§0) and stop.** Restore the 18 artifacts from
   `193a5c67`/`b2476872`, confirm `check_golden_baseline.py` PASSES, and commit
   the restore. That is a complete, correct, high-value outcome.
2. **Verify and stop.** After §1, confirm HEAD/cleanliness (guards in §2). If
   clean, report state and stop.
3. **Reproduce (real work, not a refresh).** `pip install -r requirements.txt`,
   then `SEED=42 python3 run_all_verification.py --extended` (~21 min). Report
   per-driver drift precisely; **do not** re-pin artifacts to make a tolerance
   violation disappear. `.verify_reports/VERIFICATION_EXTENDED_SUMMARY.json` is
   the reporting-only drift summary (gitignored).
4. **E041/E042 residual ill-conditioned-QP drift (~1e-05).** Already root-caused
   and fixed via the E050 exact KKT active-set enumeration (ledger E049/E050).
   Only revisit if step 3 shows a *new* structural difference; never "fix" it by
   re-pinning.
5. **Cleanup (propose only).** If the ~8,000 handoff files are a problem,
   *propose* (do not execute) a `.gitignore` + `git rm --cached` cleanup plan and
   let the user decide.
6. **Pre-registered research** only if the user explicitly requests it — with a
   `pre_registered` block, falsification expectations, and sensitivity grid stated
   *before* execution.

---

## 4. Guardrails

- Always use **SEED=42** for reproducibility/verification.
- Never commit driver verification output over canonical goldens
  (`experiments/*.json`). A checkpoint commit that captures a re-run silently
  replaces the baseline (this just happened in `195c4029`).
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json`
  without explicit, intentional re-baseline instruction and ledger justification.
  Restoring a committed artifact to its pinned content is *not* a re-pin.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (template:
  `.github/workflow-templates/verification-gate.yml`; maintainer action required).
- Never commit secrets/keys; never log secrets.
- Do not manufacture another handoff refresh to look busy.

---

## 5. Key references

- `AGENTS.md` — commands, reproducibility, baseline/guard invariants
- `ledger/RESEARCH_LEDGER.md` — dispositions (E001–E043 research; E652–E726+ handoff log)
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints
- `experiments/*.json` — canonical research artifacts
- `scripts/check.sh`, `run_all_verification.py`
- `scripts/check_golden_baseline.py` (baseline fingerprint guard; `--update` re-pins deliberately)
- `scripts/repoint_handoff.py` — repoints the generic alias symlinks to the latest handoff artifact

---

## 6. Handoff provenance

- **Durable artifact (this session):** `handoff_2026-11-23T13-18-49Z_INITIAL_TASK.md`
  (repo root). The root generic aliases (`next.md`, `next_handoff.md`,
  `next_session.md`, `INITIAL_TASK.md`, `handoff.md`, `HANDOFF.md`, `next`, etc.)
  were repointed to this file so the next session discovers it first.
- **Supersedes operationally:** prior `HANDOFF_*` / `handoff_*` artifacts
  (retained for history). The prior handoff (`...10-31-06Z...`) predates the
  `195c4029` baseline regression and does not mention it.
- This session created this durable handoff and repointed the root aliases only.
  **No code, experiments, ledgers, baselines, or canonical artifacts were
  modified, and no commit was made** (left uncommitted pending explicit
  direction). The §0 recovery is described for the next session to execute.