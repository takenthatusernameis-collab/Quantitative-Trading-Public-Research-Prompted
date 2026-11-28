# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-28T14:11:21Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` — `0f736513750a97e3d8f7ce22d60c3370cc8021a2` (`chore(kilo): checkpoint agent session`; main...origin/main)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current State (verified at handoff creation, 2026-11-28T14:11:21Z)

- `git status --short --branch`: clean except tracked `src/__pycache__/cache_keys.cpython-312.pyc` (ignored bytecode noise).
- `python3 scripts/check_goldens_clean.py`: **PASS** — working tree equals HEAD (no dirty tracked artifacts).
- `python3 scripts/check_golden_baseline.py`: **FAIL** — 5 pinned artifacts differ from `ledger/golden_baseline.json`. This is a committed verification-run capture (last-digit float drift only — no structural/string/gate-flag changes), the checkpoint-capture failure mode AGENTS.md warns about:
  - `experiments/cointegration_large_liquid.json`
  - `experiments/dollar_neutral_lowbeta_large_liquid.json`
  - `experiments/e037_portfolio.json`
  - `experiments/e042_lead_config_confirmatory.json`
  - `experiments/pairs_large_liquid.json`
  Recovery source: `c5038332` (ancestor of HEAD; its blobs hash to the exact pinned SHA-256s). **Do not re-pin.**
- `python3 scripts/check_data_coverage.py`: **PASS** — all 35 pinned data inputs present, tracked, unchanged.
- `.verify_snapshot/` and `.verify_reports/`: absent — no interrupted/pending verification run, no live owner.
- Research phase complete (**E001–E043**). Dispositions in `ledger/RESEARCH_LEDGER.md`.
- Closed/resolved: **do not reopen** E049/E050 or E041/E042 residual ill-conditioned QP drift; **do not re-pin** E041/E042 artifacts to silence drift.

## Initial Task for Next Session (CLEAR)

**Default action: wait for explicit user instructions.** Do not invent experiments, run verification unprompted, change promotion gates/outcomes, or modify golden/baseline artifacts without direction.

**Real task (fix real state, then stop):**

1. **Confirm no active verification run** — `.verify_snapshot/` must not exist. If a live `ACTIVE.json` owner exists, recover with `SEED=42 python3 run_all_verification.py --restore-only`; do NOT delete a live snapshot.
2. **Reproduce the baseline failure** — `SEED=42 python3 scripts/check_golden_baseline.py` (expect FAIL on the 5 files above).
3. **Recover the canonical baseline (surgical, 5 files):**
   ```bash
   git checkout c5038332 -- \
     experiments/cointegration_large_liquid.json \
     experiments/dollar_neutral_lowbeta_large_liquid.json \
     experiments/e037_portfolio.json \
     experiments/e042_lead_config_confirmatory.json \
     experiments/pairs_large_liquid.json
   ```
   Safe broad equivalent (only these 5 differ): `git checkout c5038332 -- experiments/`
4. **Re-verify the baseline** — `SEED=42 python3 scripts/check_golden_baseline.py` → expect "ALL 107 PINNED GOLDEN ARTIFACTS MATCH".
5. **Confirm data coverage** — `SEED=42 python3 scripts/check_data_coverage.py` (passes).
6. **Fast sanity check** — `SEED=42 bash scripts/check.sh` (offline, seconds).
7. **Surface the diff to the user and commit ONLY if asked.** After step 3 the working tree holds the clean baseline while HEAD still holds the capture, so `check_goldens_clean.py` will report a working-tree-vs-HEAD difference until the recovery is committed. Commit the 5 restored files (message noting it reverts a verification-run capture, per AGENTS.md) only on explicit user approval; then `check_goldens_clean.py` returns to PASS.

**Do not** re-pin artifacts, run `check_golden_baseline.py --update`, overwrite goldens, or write another handoff as a side effect. Do not commit unless the user explicitly asks.

## Guardrails

- Never commit driver verification output over canonical goldens.
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (template/manual maintainer path per repo docs).
- Do not change pre-registered gates, sensitivity grids, or outcomes without explicit justification and a ledger update.
- Always `SEED=42`. Close-to-close is the v1.2.3 primary convention (overnight reported alongside).

## Verification Commands (only if explicitly requested)

```bash
SEED=42 bash scripts/check.sh                        # fast guards
SEED=42 python3 scripts/check_golden_baseline.py     # 107 artifacts vs pinned baseline
SEED=42 python3 scripts/check_goldens_clean.py       # working tree == HEAD
SEED=42 python3 scripts/check_data_coverage.py       # 35 pinned inputs
SEED=42 python3 run_all_verification.py --restore-only
SEED=42 python3 verify_convention_robustness.py      # reads JSONs, no writes
```

## Handoff Provenance

- **Supersedes (recent):** `handoff_2026-11-28T10-42-49Z_INITIAL_TASK.md`, `handoff_2026-11-28T09-43-08Z_INITIAL_TASK.md`, `HANDOFF_2026-11-28T09-43-08Z_INITIAL_TASK.md`.
- **Durable copies:** `handoff_2026-11-28T14-11-21Z_INITIAL_TASK.md` (root), `handoff/handoff_2026-11-28T14-11-21Z_INITIAL_TASK.md`.
- **Canonical pointers repointed:** `handoff.md`, `NEXT_HANDOFF.md`, `initial_task.md`, `handoff_next_session.md`, `next_session.md`, `next_handoff.md` → this artifact.

(End of file)
