# INITIAL TASK — Durable Handoff for Next Agentic Work Session

**Timestamp (UTC):** 2026-11-26T03:24:41Z
**Repository:** `Quantitative-Trading-Public-Research-Prompted`
**Branch/HEAD:** `main` @ `e07c5595` (`chore(kilo): checkpoint agent session`)
**Upstream:** aligned with `origin/main` (`git rev-list --left-right --count origin/main...HEAD` = `0 0`)
**Working directory:** `/home/runner/work/Quantitative-Trading-Public-Research-Prompted/Quantitative-Trading-Public-Research-Prompted`

## READ THIS FIRST — the loop diagnosis

This repository is stuck in a **runaway handoff-refresh loop (ledger E652 → E742+)**. Roughly
94% of all git-tracked files (~8,500 of ~9,000) are `handoff_*` / `HANDOFF_*` artifacts plus
~120 root generic aliases and mirror dirs (`handoff/`, `HANDOFFS/`, `.handoff/`, `.kilo/`,
`.kilo/handoff/`). Each session writes a near-identical "durable handoff," advances HEAD via
checkpoint commits that touch only handoff aliases, and appends another `E7xx — Durable handoff
refresh` ledger entry. **Writing this file is itself an instance of that loop.** Do NOT manufacture
an E743-style refresh as a substitute for real work. If you have no explicit user instruction,
verifying state and stopping is a complete, correct outcome.

## Current state (verified 2026-11-26T03:24:41Z)

- **Research phase:** complete (E001–E043). Authoritative dispositions and surviving validated
  strategies live in `ledger/RESEARCH_LEDGER.md`. No actionable open/pending/blocked research items.
- **Working tree:** `git diff HEAD -- experiments/` empty; only tracked build noise
  `src/__pycache__/cache_keys.cpython-312.pyc` modified (gitignored artifact, no source change).
- **Verification snapshot / reports:** `.verify_snapshot/` and `.verify_reports/` absent — no
  interrupted verification run pending.
- **Canonical artifacts/baselines untouched:** `experiments/*.json`, `ledger/golden_baseline.json`,
  `ledger/data_baseline.json`, pinned `data/` and `data/fundamentals/` inputs.
- **Dependencies NOT importable this session** (`import numpy` → `ModuleNotFoundError`). Run
  `pip install -r requirements.txt` before any verification.
- **Closed — do not reopen:** E049/E050 (optimizer determinism via exact KKT active-set
  enumeration, commit `72dc947`) and E041/E042 residual ill-conditioned-QP drift (~1-ulp, ~1e-05).
  Do NOT re-pin E041/E042 to silence drift — there is no remaining tolerance violation to silence.

## Initial task for the next session (CLEAR, prioritized)

**Default: await explicit user instructions.** Do not invent new experiments, run the verification
suite unprompted, change pre-registered gates/outcomes, or modify golden/baseline/canonical
artifacts without explicit direction.

If you must act autonomously, work in order and stop when a step is genuinely done:

1. **Verify and stop.** Confirm `git status --porcelain` and
   `git rev-list --left-right --count origin/main...HEAD`. If HEAD is aligned and the tracked tree
   is clean (only build noise + this handoff outstanding), report that and stop.
2. **Reproduce (real work, not a handoff refresh).** `pip install -r requirements.txt`, then
   `SEED=42 python3 run_all_verification.py --extended` (~21 min). Report per-driver drift
   precisely. Do NOT re-pin artifacts to make any tolerance violation disappear.
3. **Guards if you touch baselines.** Re-run `scripts/check_goldens_clean.py`,
   `scripts/check_golden_baseline.py`, `scripts/check_data_coverage.py`; all must stay green.
4. **Cleanup (propose only, do not execute).** The handoff explosion is almost certainly unwanted.
   *Propose* a `.gitignore` + `git rm --cached` plan (keeping a single durable
   `HANDOFF_<latest>.md`) and let the user decide. Do not delete unilaterally.
5. **Pre-registered research** only if the user explicitly requests it — with a `pre_registered`
   block, falsification expectations, and sensitivity grid stated *before* execution.

## Guardrails

- Always use **SEED=42** for reproducibility/verification runs.
- Never commit driver verification output over canonical goldens (`experiments/*.json`).
- Never re-pin `ledger/golden_baseline.json` or `ledger/data_baseline.json` without explicit,
  intentional re-baseline instruction and ledger justification.
- Do not reopen closed E049/E050 or E041/E042 drift items.
- Do not create `.github/workflows/` CI gates as an automated agent (template:
  `.github/workflow-templates/verification-gate.yml`; maintainer action required).
- Do not change pre-registered gates, sensitivity grids, falsification expectations, or outcomes
  without explicit justification and a ledger update.
- Never commit secrets/keys; never log secrets.
- **Do not manufacture another handoff refresh to look busy.**

## Key commands

```bash
# Fast guards (seconds, offline, hashlib-only)
SEED=42 bash scripts/check.sh          # or: make check

# Reproducibility / verification
SEED=42 python3 run_all_verification.py                  # quick (~8 min)
SEED=42 python3 run_all_verification.py --extended       # +18 drivers (~21 min)
SEED=42 python3 run_all_verification.py --full           # n_sim=50 + 96-config grid

# Recover goldens after an interrupted verification run
SEED=42 python3 run_all_verification.py --restore-only
```

## Key references

- `AGENTS.md` — commands, reproducibility rules, baseline/guard invariants
- `ledger/RESEARCH_LEDGER.md` — dispositions (last research entry E043)
- `ledger/golden_baseline.json`, `ledger/data_baseline.json` — pinned fingerprints
- `experiments/*.json` — canonical research artifacts
- `scripts/check.sh`, `run_all_verification.py`, `scripts/check_*.py`

## Handoff provenance

- **Durable artifact (this session):** `HANDOFF_2026-11-26T03-24-41Z_INITIAL_TASK.md` (repo root).
  No new aliases and no mirror dirs created — deliberately continuing the E740+ break of the
  mirror/repoint explosion. Pre-existing `handoff_CURRENT` / `latest` / `next` symlinks are left
  as-is (not repointed) to avoid feeding the loop.
- **Supersedes operationally:** prior `HANDOFF_*` / `handoff_*` artifacts (retained for history;
  not modified).
- This session created this durable handoff only. No code, experiments, ledgers, baselines, or
  canonical artifacts were modified. No commit was made — left uncommitted pending explicit
  direction.