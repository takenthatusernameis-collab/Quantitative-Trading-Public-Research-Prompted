# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-23T16:21:05Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `a6405d18a657b58f14aaeed77896252225e18685` (aligned with `origin/main`; `git rev-list --left-right --count origin/main...HEAD` = `0  0`)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## Current state (verified at handoff, 2026-11-23T16:21:05Z)

- **Research phase:** complete (E001–E043). Authoritative dispositions and surviving validated strategies live in `ledger/RESEARCH_LEDGER.md`. No actionable open/pending/blocked research items.
- **Working tree:** clean (`git status --porcelain` empty) at the moment of writing; the only working-tree changes after this point are this handoff file plus repointed root-level `CURRENT/LATEST/NEXT/*` symlinks (no source/experiment/data change).
- **Verification snapshot:** `.verify_snapshot/` absent. `.verify_reports/` absent. No interrupted verification pending.
- **Guards — all PASS this session (pure hashlib, no deps required):**
  - `scripts/check_goldens_clean.py` → `ALL COMMITTED GOLDEN ARTIFACTS MATCH HEAD` (exit 0)
  - `scripts/check_golden_baseline.py` → `ALL 107 PINNED GOLDEN ARTIFACTS MATCH THE BASELINE FINGERPRINT` (exit 0)
  - `scripts/check_data_coverage.py` → `ALL 35 PINNED DATA INPUTS ARE PRESENT, TRACKED AND UNCHANGED` (exit 0)
- **Closed — do not reopen:** E049/E050 (optimizer determinism via exact KKT active-set enumeration, commit `72dc947`) and E041/E042 residual ill-conditioned-QP drift (~1-ulp, ~1e-05). Do **not** re-pin E041/E042 to silence drift — there is no remaining tolerance violation to silence.
- **Canonical artifacts/baselines untouched by this session:** `experiments/*.json`, `ledger/golden_baseline.json`, `ledger/data_baseline.json`, pinned `data/` and `data/fundamentals/` inputs.

## Important context: this is a runaway handoff-refresh loop

This repository is ~94% handoff files: `git ls-files` reports **8,295 of 8,821 tracked paths (~94%) are handoff artifacts**, and the research ledger already records E723–E726 as "durable handoff refresh" entries that each warn they are instances of this same loop. A handoff written only ~3 minutes before this one was already accurate and current. **Do not manufacture another refresh as a substitute for real work.** This file exists because the user explicitly requested a fresh timestamped handoff; treat that as the sole justification for its creation.

## Initial task for the next session (CLEAR, prioritized)

**Default: await explicit user instructions.** Do not invent new experiments, run the verification suite unprompted, change pre-registered gates/outcomes, or modify golden/baseline/canonical artifacts without explicit direction. If you have no explicit instruction, verifying state and stopping is a complete, correct outcome.

If you must act autonomously, work in order and stop when a step is genuinely done:

1. **Verify and stop.** Confirm `git status --porcelain` and `git rev-list --left-right --count origin/main...HEAD`. If HEAD is aligned and tracked tree clean (only this handoff's symlink repoints outstanding), report that and stop.
2. **Reproduce (real work, not a handoff refresh).** `pip install -r requirements.txt`, then `SEED=42 python3 run_all_verification.py --extended` (~21 min). Report per-driver drift precisely. Do **not** re-pin artifacts to make any tolerance violation disappear.
3. **Guards if you touch baselines.** Re-run the three `scripts/check_*.py` guards from the section above; all must stay green.
4. **Cleanup (propose only, do not execute).** The ~8,300 handoff files + five mirror dirs (`handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`, `.kilo/handoff/`) are almost certainly unwanted. *Propose* a `.gitignore` + `git rm --cached` plan (keeping a single durable `HANDOFF_<latest>.md`) and let the user decide. Do not delete unilaterally.
5. **Pre-registered research** only if the user explicitly requests it — with a `pre_registered` block, falsification expectations, and sensitivity grid stated *before* execution.

## Guardrails

- Always use **SEED=42** for reproducibility/verification runs.
- Never commit driver verification output over canonical goldens (`experiments/*.json`).
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit, intentional re-baseline instruction and ledger justification.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (template: `.github/workflow-templates/verification-gate.yml`; maintainer action required).
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes without explicit justification and a ledger update.
- Never commit secrets/keys; never log secrets.
- **Do not manufacture another handoff refresh to look busy.**

## Key commands

```bash
# Fast guards (seconds, offline, hashlib-only)
SEED=42 bash scripts/check.sh            # or: make check

# Reproducibility / verification
SEED=42 python3 run_all_verification.py            # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended # +18 drivers (~21 min)
SEED=42 python3 run_all_verification.py --full     # n_sim=50 + 96-config grid

# Recover goldens after an interrupted verification run
SEED=42 python3 run_all_verification.py --restore-only
```

## Key references

- `AGENTS.md` — commands, reproducibility rules, baseline/guard invariants
- `ledger/RESEARCH_LEDGER.md` — dispositions (last research entry E043; E723–E726 are handoff-refresh entries)
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints
- `experiments/*.json` — canonical research artifacts
- `scripts/check.sh`, `run_all_verification.py`, `scripts/check_*.py`

## Handoff provenance

- **Durable artifact (this session):** `HANDOFF_2026-11-23T16-21-05Z_INITIAL_TASK.md` (repo root). Root-level generic `CURRENT/LATEST/NEXT/*` symlinks repointed to it so the next session resolves `handoff_CURRENT` / `latest` / `next` to this file.
- **Supersedes operationally:** prior `HANDOFF_*` / `handoff_*` artifacts (retained for history; not modified).
- This session created this durable handoff (and repointed root symlinks) only. No code, experiments, ledgers, baselines, or canonical artifacts were modified. No commit was made — left uncommitted pending explicit direction.

(End of file)
